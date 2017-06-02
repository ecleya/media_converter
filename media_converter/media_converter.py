import subprocess
from pyfileinfo import PyFileInfo
from media_converter.codecs import VideoCodec, AudioCodec, H264, AAC
from media_converter.tracks import Track, AudioTrack, VideoTrack, SubtitleTrack


class MediaConverter:
    def __init__(self, tracks, dst):
        if not isinstance(tracks, list):
            tracks = [tracks]

        self._tracks = tracks
        self._dst = PyFileInfo(dst)
        self._command = None
        self._infiles = None
        self._start = None
        self._duration = None

    def convert(self, start=None, end=None, duration=None):
        self._start = start
        self._end = end
        self._duration = duration

        self._create_command()

        subprocess.call(self._command)

    @property
    def tracks(self):
        for track in self._tracks:
            if isinstance(track, Track):
                yield track
                continue

            for codec in self._get_default_codecs():
                if isinstance(codec, VideoCodec):
                    yield VideoTrack(track, codec)
                elif isinstance(codec, AudioCodec):
                    yield AudioTrack(track, codec)

    def _create_command(self):
        self._init_command()
        self._append_instreams()
        self._append_tracks()
        self._append_metadata()
        self._append_time_options()
        self._append_dst()

    def _init_command(self):
        self._command = ['/usr/local/bin/ffmpeg', '-y']
        self._infiles = []

    def _append_instreams(self):
        for track in self.tracks:
            for instream in track.outstream.instreams:
                if instream.as_ffmpeg_instream() in self._infiles:
                    continue

                self._infiles.append(instream.as_ffmpeg_instream())
                self._command.extend(instream.as_ffmpeg_instream())

    def _append_tracks(self):
        for track in self.tracks:
            self._append_outstream_options_with_filter(track.outstream)
            self._command.extend(track.codec.options_for_ffmpeg(self._get_track_index(track)))

    def _get_track_index(self, target_track):
        index = 0
        for track in self._tracks:
            if track == target_track:
                break

            if type(track) is type(target_track):
                index += 1

        return index

    def _append_metadata(self):
        self._append_default_info('v', self.video_tracks)
        self._append_default_info('a', self.audio_tracks)
        self._append_default_info('s', self.subtitle_tracks)

        self._append_language_info('v', self.video_tracks)
        self._append_language_info('a', self.audio_tracks)
        self._append_language_info('s', self.subtitle_tracks)

    def _append_default_info(self, identifier, tracks):
        has_default_track = any([track.default for track in tracks])
        is_default = not has_default_track
        track_index = 0
        for track in tracks:
            self._command.extend([f'-disposition:{identifier}:{track_index}',
                                  'default' if is_default or track.default else '0'])
            is_default = False
            track_index += 1

    def _append_language_info(self, identifier, tracks):
        track_index = 0
        for track in tracks:
            if track.language is not None:
                self._command.extend([f'-metadata:s:{identifier}:{track_index}', track.language])

            track_index += 1

    @property
    def video_tracks(self):
        for track in self.tracks:
            if isinstance(track, VideoTrack):
                yield track

    @property
    def audio_tracks(self):
        for track in self.tracks:
            if isinstance(track, AudioTrack):
                yield track

    @property
    def subtitle_tracks(self):
        for track in self.tracks:
            if isinstance(track, SubtitleTrack):
                yield track

    def _append_outstream_options_with_filter(self, outstream):
        idx = 0
        instream = outstream.instreams[0]
        infile_index = self._infiles.index(instream.as_ffmpeg_instream())
        instream_id = f'[{infile_index}:{instream.track_type}:{instream.track_index}]'
        outstream_id = f'[vout{idx}]'
        filters = []

        for instream, filter_option in outstream.filters:
            if instream is None:
                filters.append(f'{instream_id}{filter_option}{outstream_id}')
            else:
                infile_index = self._infiles.index(instream.as_ffmpeg_instream())
                additional_instream_id = f'[{infile_index}:{instream.track_type}:{instream.track_index}]'
                filters.append(f'{instream_id}{additional_instream_id}{filter_option}{outstream_id}')
            instream_id = outstream_id
            idx += 1
            outstream_id = f'[vout{idx}]'

        if len(filters) == 0:
            self._command.extend(['-map', f'{infile_index}:{instream.track_type}:{instream.track_index}'])
        else:
            self._command.extend(['-filter_complex', ';'.join(filters), '-map', instream_id])

    def _append_time_options(self):
        options = []
        if self._start is not None:
            options.extend(['-ss', str(self._start)])

        if self._duration is not None:
            options.extend(['-t', str(self._duration)])
        elif self._end is not None:
            options.extend(['-to', str(self._end)])

        if len(options) == 0 and self._has_not_timed_blank_instream():
            self._command.append('-shortest')
        else:
            self._command.extend(options)

    def _has_not_timed_blank_instream(self):
        for track in self.tracks:
            for instream in track.outstream.instreams:
                if instream.is_blank() and instream.duration is None:
                    return True

        return False

    def _append_dst(self):
        self._command.extend(['-threads', '0', self._dst.path])

    def _get_default_codecs(self):
        default_codecs = {
            '.mkv': [H264, AAC],
            '.mp4': [H264, AAC],
            '.m4v': [H264],
            '.m4a': [AAC],
        }

        for codec in default_codecs[self._dst.extension.lower()]:
            yield codec()
