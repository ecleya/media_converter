import os
import re
import shutil
import stat
import tempfile
import unicodedata
from datetime import datetime
from time import time

from media_converter.utils import logutil


def files_in(target_folder, recursive=False):
    if not os.path.exists(target_folder):
        return []

    if recursive:
        files = []
        for file in files_in(target_folder):
            filename = os.path.split(file)[1]
            if filename[0] == '.':
                continue

            if os.path.isdir(file):
                files.extend(files_in(file, True))
            else:
                files.append(file)
    else:
        files = [os.path.join(target_folder, filename) for filename in os.listdir(target_folder) if filename[0] != '.']

    files = [unicodedata.normalize('NFC', file) for file in files]
    return sorted(files, key=path_to_sort_key)


def path_to_sort_key(file_path):
    def to_int_if_possible(c):
        try:
            return int(c)
        except:
            return c.lower()

    return [to_int_if_possible(c) for c in re.split('([0-9]+)', file_path)]


def is_extension(file_path, ext):
    return is_extension_in(file_path, [ext])


def is_extension_in(file_path, extensions):
    return os.path.splitext(file_path)[1].lower() in [ext.lower() for ext in extensions]


def is_hidden(file_path):
    return file_path[0] == '.' or file_path[0] == '@'


def makedirs(body):
    if os.path.exists(body):
        return

    parent, _ = os.path.split(body)
    if parent == '/Volumes':
        return

    makedirs(parent)
    os.mkdir(body)
    os.chmod(body, os.stat(body).st_mode | stat.S_IWOTH)


def replace_unusable_char(file_name):
    invalid_chars = '\\/:*?<>|"'
    for invalid_char in invalid_chars:
        file_name = file_name.replace(invalid_char, '_')

    if file_name[0] == '.':
        file_name = '_' + file_name[1:]

    return file_name


def generate_temporary_file_path(extension):
    result = os.path.join(tempfile.gettempdir(), u'%d%s' % (int(time()), extension))
    while os.path.exists(result):
        result = os.path.join(tempfile.gettempdir(), u'%d%s' % (int(time()), extension))

    return result


def move(source_path, destination_path):
    logutil.info('fileutil', 'move: %s -> %s' % (source_path, destination_path))
    if not os.path.exists(source_path):
        logutil.info('fileutil', '%s is not exists' % source_path)
        return

    if is_on_same_disc(source_path, destination_path):
        body, _ = os.path.split(destination_path)
        if not os.path.exists(body):
            makedirs(body)

        shutil.move(source_path, destination_path)
        return

    copy(source_path, destination_path)
    if os.path.isdir(source_path):
        shutil.rmtree(source_path)
    else:
        os.remove(source_path)


def is_on_same_disc(lhs_path, rhs_path):
    lhs_volume_name = lhs_path.split('/')[2]
    rhs_volume_name = rhs_path.split('/')[2]

    return lhs_volume_name == rhs_volume_name


def copy(source_path, destination_path):
    if os.path.isdir(source_path):
        for file in files_in(source_path):
            _, file_name = os.path.split(file)
            copy(file, os.path.join(destination_path, file_name))

        return

    body, _ = os.path.split(destination_path)
    if not os.path.exists(body):
        makedirs(body)

    shutil.copy(source_path, destination_path)
    while not is_equal(source_path, destination_path):
        shutil.copy(source_path, destination_path)


def is_equal(lhs_path, rhs_path):
    if lhs_path == rhs_path:
        return True

    if os.path.getsize(lhs_path) != os.path.getsize(rhs_path):
        return False

    block_size = 4096
    lhs = open(lhs_path, 'rb')
    rhs = open(rhs_path, 'rb')

    while True:
        lhs_block = lhs.read(block_size)
        rhs_block = rhs.read(block_size)

        if lhs_block != rhs_block:
            return False

        if lhs_block == b'':
            break

    return True


def change_ext(file_path, ext):
    body, _ = os.path.splitext(file_path)

    return body + ext


def change_filename(file_path, name):
    body, file = os.path.split(file_path)
    _, ext = os.path.splitext(file)

    return os.path.join(body, name + ext)


def get_filename(file):
    return os.path.splitext(os.path.split(file)[1])[0]


def get_time_created(file_path):
    return datetime.fromtimestamp(os.path.getctime(file_path))


def get_time_modified(file_path):
    return datetime.fromtimestamp(os.path.getmtime(file_path))


def get_time_last_accessed(file_path):
    return datetime.fromtimestamp(os.path.getatime(file_path))


def is_video(file_path):
    return os.path.splitext(file_path)[1].lower() in ['.mp4', '.mov', '.mpg', '.avi', '.m4v', '.mkv', '.m2t', '.wmv', '.mpeg', '.webm']


def is_audio(file_path):
    return os.path.splitext(file_path)[1].lower() in ['.mp3', '.m4a']


def is_subtitle(file_path):
    return os.path.splitext(file_path)[1].lower() in ['.ass', '.srt', '.smi']


def get_subtitle_path(vid_path):
    for subtitle_ext in ['.ass', '.srt', '.smi']:
        subtitle_path = change_ext(vid_path, subtitle_ext)
        if os.path.exists(subtitle_path):
            return subtitle_path

    body = os.path.split(vid_path)[0]
    for file in files_in(body):
        if not is_subtitle(file):
            continue

        if os.path.splitext(os.path.split(file)[1])[0] == os.path.splitext(os.path.split(vid_path)[1])[0]:
            return file

    return None
