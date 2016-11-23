from media_converter.utils import processutil
from media_converter.mixins import TemporaryFileMixin


class MKVToolnix(TemporaryFileMixin):
    def mux(self, mediafile, *args):
        mkv_path = self._new_tmp_filepath('.mkv')
        cmd = ['/usr/local/bin/mkvmerge', '-o', mkv_path, mediafile]
        cmd.extend(args)
        processutil.call(cmd)

        return mkv_path

    def concat(self, mediafile, *args):
        mkv_path = self._new_tmp_filepath('.mkv')
        cmd = ['/usr/local/bin/mkvmerge', '-o', mkv_path, '--no-chapters', '--no-subtitles', mediafile]
        for arg in args:
            cmd.extend(['--no-chapters', '--no-subtitles', '+%s' % arg])
        processutil.call(cmd)

        return mkv_path
