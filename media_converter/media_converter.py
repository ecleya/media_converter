import subprocess
from pyfileinfo import PyFileInfo
from media_converter.tracks import AudioTrack, VideoTrack
from media_converter.streams import VideoOutstream, AudioOutstream
from media_converter.mixins import TemporaryFileMixin


class MediaConverter(TemporaryFileMixin):
    def __init__(self, tracks, dst):
        TemporaryFileMixin.__init__(self)

        if not isinstance(tracks, list):
            tracks = [tracks]

        self._tracks = tracks
        self._dst = dst
        self._command = None

    def convert(self):
        subprocess.call(self.command)

    @property
    def command(self):
        self._init_command()
        self._append_infiles()
        self._append_codecs()
        self._append_dst()

        return self._command

    def _init_command(self):
        self._command = ['/usr/local/bin/ffmpeg', '-y']

    def _append_infiles(self):
        for track in self._tracks:
            if isinstance(track, str):
                self._command.extend(['-i', track])
            if isinstance(track, AudioTrack):
                self._command.extend(['-i', track.outstream])

    def _append_codecs(self):
        for track in self._tracks:
            if isinstance(track, VideoTrack):
                codec = track.codec
                self._command.extend(['-c:v', 'mpeg', '-b:v', str(codec.bitrate), '-aspect', str(codec.aspect_ratio), '-r', str(codec.frame_rate)])
            if isinstance(track, AudioTrack):
                codec = track.codec
                self._command.extend(['-c:a', 'aac', '-b:a', str(codec.bitrate), '-ac', str(codec.channels), '-ar', str(codec.sampling_rate)])

    def _append_dst(self):
        self._command.append(self._dst)
