import subprocess
from pyfileinfo import PyFileInfo
from media_converter.streams import AudioOutstream
from media_converter.mixins import TemporaryFileMixin


class MediaConverter(TemporaryFileMixin):
    def __init__(self, outstreams, dst):
        TemporaryFileMixin.__init__(self)

        if not isinstance(outstreams, list):
            outstreams = [outstreams]

        self._outstreams = outstreams
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
        for outstream in self._outstreams:
            if isinstance(outstream, str):
                self._command.extend(['-i', outstream])
            if isinstance(outstream, AudioOutstream):
                self._command.extend(['-i', outstream.instream])

    def _append_codecs(self):
        for outstream in self._outstreams:
            if isinstance(outstream, AudioOutstream):
                codec = outstream.codec
                self._command.extend(['-c:a', 'aac', '-b:a', str(codec.bitrate), '-ac', str(codec.channels), '-ar', str(codec.sampling_rate)])

    def _append_dst(self):
        self._command.append(self._dst)
