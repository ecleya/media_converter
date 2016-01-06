from media_converter.utils import processutil


def get_video_tracks(file_path):
    template = {'Type': 'Video',
                'Codec': 'Codec',
                'Width': 'Width',
                'Height': 'Height',
                'Frame Rate': 'FrameRate',
                'Original Frame Rate': 'FrameRate_Original',
                'Aspect Ratio': 'DisplayAspectRatio/String',
                'Scan Type': 'ScanType',
                'Language': 'Language/String'}

    return _get_medium_details(file_path, template)


def get_audio_tracks(file_path):
    template = {'Type': 'Audio',
                'Channels': 'Channel(s)',
                'Codec': 'Codec',
                'Compression Mode': 'Compression_Mode',
                'Language': 'Language/String'}

    return _get_medium_details(file_path, template)


def get_subtitle_tracks(file_path):
    template = {'Type': 'Text',
                'Language': 'Language/String',
                'Format': 'Format'}

    return _get_medium_details(file_path, template)


def get_duration(file_path):
    details = _get_medium_details(file_path, {'Type': 'General', 'Duration': 'Duration/String3'})

    return details[0]['Duration']


def get_chapters(file_path):
    command = ['/usr/local/bin/MediaInfo', file_path]
    ret_code, out, err = processutil.call(command)
    chapter_info = out[out.find('Menu'):]

    return [chapter for chapter in chapter_info.splitlines(False)[1:] if chapter.strip() != '']


def _get_medium_details(file_path, dictionary):
    template = _to_template(dictionary)

    command = ['/usr/local/bin/mediainfo', '--Inform=%s' % template, file_path]
    ret_code, details_raw, _ = processutil.call(command)

    return _parse_details(details_raw)


def _to_template(dictionary):
    template = '%s;Type : %%StreamKind/String%%|' % dictionary['Type']
    for key, value in dictionary.items():
        if key == 'Type':
            continue

        template += '%s : %%%s%%|' % (key, value)

    return template + '|'


def _parse_details(details_raw):
    details = []
    for track_details in _get_tracks(details_raw):
        if track_details.strip() == '':
            continue

        track_details += '\nTrack Number : %d' % len(details)
        details.append(_parse_track(track_details))

    return details


def _parse_track(track_details):
    track = {}
    for key_value in track_details.splitlines(False):
        key, value = key_value.split(' : ')
        track[key.strip()] = value.strip()

    return track


def _get_tracks(details_raw):
    return details_raw.replace('|', '\n').split('\n\n')
