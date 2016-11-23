import importlib

from chardet.universaldetector import UniversalDetector
from media_converter.utils import processutil
from media_converter.mixins import TemporaryFileMixin

from media_converter.wrappers.ffmpeg.ffmpeg_streams import AudioOutstream, VideoOutstream


class FFmpeg(TemporaryFileMixin):
    def __init__(self, outstreams, container, analyze_duration=None, probe_size=None):
        TemporaryFileMixin.__init__(self)

        self._outstreams = outstreams
        self._container = container
        self._analyze_duration = analyze_duration
        self._probe_size = probe_size
        self._duration = None
        self._frame_rate = None
        self._start_at = None
        self._stop_at = None

        self._infiles = None
        self._command = None

    def change_container(self, src, container):
        dst = self._new_tmp_filepath(container.extension)
        processutil.call(['/usr/local/bin/ffmpeg', '-y', '-i', src, '-map', '0', '-c', 'copy', dst])

        return dst

    @staticmethod
    def get_mean_volume(src):
        ret, out, err = processutil.call(['/usr/local/bin/ffmpeg', '-i', src,
                                          '-af', 'volumedetect', '-f', 'null', '/dev/null'])
        vol_info = err
        vol_info = vol_info[vol_info.find('mean_volume:'):]
        vol_info = vol_info[:vol_info.find('\n')]

        return float(vol_info.split(' ')[1])

    def smi_to_srt(self, sub_path):
        def _detect(file_path):
            detector = UniversalDetector()
            fp = open(file_path, 'rb')
            for line in fp:
                line = line.replace(b'\r', b'')
                detector.feed(line)
                if detector.done:
                    break

            fp.close()
            detector.close()

            return detector.result['encoding']

        srt_path = self._new_tmp_filepath('.srt')
        tmp_sub_path = self._new_tmp_filepath('.smi')

        char_type = _detect(sub_path)
        context = open(sub_path, 'r', encoding=char_type, errors='ignore').read()
        open(tmp_sub_path, 'w', encoding='utf8').write(context)
        sub_path = tmp_sub_path

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-i', sub_path,
               srt_path]

        processutil.call(cmd)
        return srt_path

    def set_duration(self, duration):
        self._duration = duration

    def set_frame_rate(self, frame_rate):
        self._frame_rate = frame_rate

    def set_start_at(self, seconds):
        self._start_at = seconds

    def set_stop_at(self, seconds):
        self._stop_at = seconds

    def execute(self):
        processutil.call(self.command)

        return self.command[-1]

    @property
    def infiles(self):
        if self._infiles is None:
            self._infiles = []
            for outstream in self._outstreams:
                if outstream.instream.infile not in self._infiles:
                    self._infiles.append(outstream.instream.infile)

                for effect in outstream.effects:
                    if effect['instream'] is None or effect['instream'].infile in self._infiles:
                        continue

                    self._infiles.append(effect['instream'].infile)

        return self._infiles

    @property
    def command(self):
        if self._command is None:
            self._init_command()
            self._add_analyze_options()
            self._add_infiles_options()
            self._add_stream_options()
            self._add_duration_option()
            self._add_framerate_options()
            self._command.extend(['-threads', '0', self._new_tmp_filepath(self._container.extension)])

        return self._command

    def _init_command(self):
        self._command = ['/usr/local/bin/ffmpeg', '-y']

    def _add_analyze_options(self):
        if self._analyze_duration is not None:
            self._command.extend(['-analyzeduration', str(self._analyze_duration)])
        if self._probe_size is not None:
            self._command.extend(['-probesize', str(self._probe_size)])

    def _add_infiles_options(self):
        for ffmpeg_infile in self.infiles:
            self._command.extend(ffmpeg_infile.get_ffmpeg_options())

    def _add_stream_options(self):
        for outstream in self._outstreams:
            self._command.extend(self._get_stream_options(outstream))

    def _get_stream_options(self, outstream):
        if len(outstream.effects) == 0:
            instream = outstream.instream

            return ['-map', '%d:%s:%s' % (self.infiles.index(instream.infile), instream.stream_type,
                                          str(instream.stream_index))] + \
                outstream.target_codec.get_ffmpeg_options(self._get_outstream_index(outstream))

        if type(outstream) is VideoOutstream:
            instream = outstream.instream
            video_in = '%d:v' % self.infiles.index(instream.infile)
            options = []
            idx = 0
            for effect in outstream.effects:
                module = importlib.import_module('media_converter.wrappers.ffmpeg.ffmpeg_filters')
                stream_specifier = self._get_stream_specifier(effect['instream'])
                if stream_specifier is not None:
                    effect['args']['stream_specifier'] = stream_specifier

                video_filter = getattr(module, effect['effect_name'].title().replace('_', ''))(**effect['args'])

                video_out = 'vf%d_out' % idx
                options.append('[%s]%s[%s]' % (video_in, video_filter.get_ffmpeg_filter_option(), video_out))
                video_in = video_out
                idx += 1

            return ['-filter_complex', ','.join(options), '-map', '[%s]' % video_in] +\
                outstream.target_codec.get_ffmpeg_options(self._get_outstream_index(outstream))

        if type(outstream) is AudioOutstream:
            instream = outstream.instream
            effect = outstream.effects[0]
            module = importlib.import_module('wrappers.ffmpeg.ffmpeg_filters')
            audio_filter = getattr(module, effect['effect_name'].title())(**effect['args'])

            return ['-map', '%d:%s:%s' % (self.infiles.index(instream.infile_path), instream.stream_type,
                                          str(instream.stream_index))] + \
                outstream.target_codec.get_ffmpeg_options(self._get_outstream_index(outstream)) +\
                ['-af', audio_filter.get_ffmpeg_filter_option()]

    def _get_stream_specifier(self, instream):
        if instream is None:
            return None

        return '%d:%s:%d' % (self._infiles.index(instream.infile), instream.stream_type, instream.stream_index)

    def _get_outstream_index(self, target_outstream):
        idx = 0
        for ffmpeg_outstream in self._outstreams:
            if ffmpeg_outstream == target_outstream:
                return idx

            if ffmpeg_outstream.stream_type == target_outstream.stream_type:
                idx += 1

        return -1

    def _add_duration_option(self):
        if self._start_at is not None:
            self._command.extend(['-ss', str(self._start_at)])
        if self._stop_at is not None:
            self._command.extend(['-to', str(self._stop_at)])
        if self._duration is not None:
            self._command.extend(['-t', str(self._duration)])

    def _add_framerate_options(self):
        if self._frame_rate is not None:
            self._command.extend(['-r', str(self._frame_rate)])
