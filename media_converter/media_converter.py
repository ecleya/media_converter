import subprocess
from pyfileinfo import PyFileInfo
from media_converter.mixins import TemporaryFileMixin


class MediaConverter(TemporaryFileMixin):
    def __init__(self, src=None, dst=None):
        TemporaryFileMixin.__init__(self)

        self._srcs = []
        if src is not None:
            self._append_source(src)

        self._dst = dst

    def convert(self):
        subprocess.call(self._command())

    def _command(self):
        return ['/usr/local/bin/ffmpeg', '-i', self._srcs[0].path, self._dst]

    def _append_source(self, src):
        if isinstance(src, str):
            src = PyFileInfo(src)

        self._srcs.append(src)
