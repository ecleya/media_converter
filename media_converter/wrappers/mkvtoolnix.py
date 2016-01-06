from media_converter.utils import fileutil, processutil


def mux(mediafile, *args):
    mkv_path = fileutil.generate_temporary_file_path('.mkv')
    cmd = ['/usr/local/bin/mkvmerge', '-o', mkv_path, mediafile]
    cmd.extend(args)
    processutil.call(cmd)

    return mkv_path


def concat(mediafile, *args):
    mkv_path = fileutil.generate_temporary_file_path('.mkv')
    cmd = ['/usr/local/bin/mkvmerge', '-o', mkv_path, '--no-chapters', '--no-subtitles', mediafile]
    for arg in args:
        cmd.extend(['--no-chapters', '--no-subtitles', '+%s' % arg])
    processutil.call(cmd)

    return mkv_path
