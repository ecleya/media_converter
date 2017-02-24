import shutil
import subprocess
from pyfileinfo import PyFileInfo
from media_converter.codecs import VideoCodec, AudioCodec, H264, AAC
from media_converter.tracks import Track, AudioTrack, VideoTrack
from media_converter.mixins import TemporaryFileMixin


class MediaConverter(TemporaryFileMixin):
    def __init__(self, tracks, dst):
        TemporaryFileMixin.__init__(self)

        if not isinstance(tracks, list):
            tracks = [tracks]

        self._tracks = tracks
        self._dst = PyFileInfo(dst)
        self._command = None
        self._infiles = None

    def convert(self):
        subprocess.call(self.command)

        shutil.move(self.command[-1], self._dst.path)

    @property
    def command(self):
        if self._command is None:
            self._init_command()
            self._append_instreams()
            self._append_tracks()
            self._append_dst()

        return self._command

    def _init_command(self):
        self._command = ['/usr/local/bin/ffmpeg', '-y']
        self._infiles = []

    @property
    def tracks(self):
        for track in self._tracks:
            if isinstance(track, Track):
                yield track
            elif isinstance(track, str):
                for codec in self._get_default_codecs():
                    if isinstance(codec, VideoCodec):
                        yield VideoTrack(track, codec)
                    elif isinstance(codec, AudioCodec):
                        yield AudioTrack(track, codec)

    def _append_instreams(self):
        for track in self.tracks:
            instream = track.outstream.instream
            if instream.as_ffmpeg_instream() in self._infiles:
                continue

            self._infiles.append(instream.as_ffmpeg_instream())
            self._command.extend(instream.as_ffmpeg_instream())

    def _append_tracks(self):
        for track in self.tracks:
            instream = track.outstream.instream
            infile_index = self._infiles.index(instream.as_ffmpeg_instream())
            filter = track.outstream.filter_options_for_ffmpeg(infile_index)
            if len(filter) == 0:
                self._command.extend(['-map', f'{infile_index}:{instream.track_type}:{instream.track_index}'])
            else:
                self._command.extend(['-filter_complex', filter, '-map', '[vout0]'])

            self._command.extend(track.codec.options_for_ffmpeg())

    def _append_dst(self):
        self._command.append(self._new_tmp_filepath(self._dst.extension))

    def _get_default_codecs(self):
        default_codecs = {
            '.mkv': [H264, AAC]
        }

        for codec in default_codecs[self._dst.extension.lower()]:
            yield codec()
