from fractions import Fraction
from xml.etree import ElementTree

from media_converter.utils import processutil
from media_converter.wrappers import mediainfo


class Medium:
    def __init__(self, file_path):
        self._file_path = file_path
        self._video_tracks = None
        self._audio_tracks = None
        self._subtitle_tracks = None
        self._duration = None
        self._mean_volume = None
        self._xml_root = None

    def is_audio_track_empty(self):
        return len(self.audio_tracks) == 0

    def is_hd(self):
        return self.width >= 1200 or self.height >= 700

    def is_video(self):
        return len(self.video_tracks) > 0

    def is_audio(self):
        return not self.is_video() and len(self.audio_tracks) > 0

    @property
    def xml_root(self):
        if self._xml_root is None:
            cmd = ['/usr/local/bin/mediainfo', '--Output=XML', '-f', self._file_path]
            ret_code, out, err = processutil.call(cmd)

            self._xml_root = ElementTree.fromstring(out)

        return self._xml_root

    @property
    def title(self):
        return self._xml_root.find('File').find('track').find('Title').text

    @property
    def album(self):
        return self._xml_root.find('File').find('track').find('Album').text

    @property
    def album(self):
        return self._xml_root.find('File').find('track').find('Album').text

    @property
    def album_performer(self):
        return self._xml_root.find('File').find('track').find('Album_Performer').text

    @property
    def track_name(self):
        return self._xml_root.find('File').find('track').find('Track_name').text

    @property
    def track_name_position(self):
        return self._xml_root.find('File').find('track').find('Track_name_Position').text

    @property
    def part_position(self):
        return self._xml_root.find('File').find('track').find('Part_Position').text

    @property
    def file_path(self):
        return self._file_path

    @property
    def video_tracks(self):
        if self._video_tracks is None:
            self._video_tracks = VideoTrack.from_mediainfo(mediainfo.get_video_tracks(self.file_path))

        return self._video_tracks

    @property
    def audio_tracks(self):
        if self._audio_tracks is None:
            self._audio_tracks = AudioTrack.from_mediainfo(mediainfo.get_audio_tracks(self._file_path))

        return self._audio_tracks

    @property
    def subtitle_tracks(self):
        if self._subtitle_tracks is None:
            self._subtitle_tracks = SubtitleTrack.from_mediainfo(mediainfo.get_subtitle_tracks(self._file_path))

        return self._subtitle_tracks

    @property
    def chapters(self):
        chapters = []
        chapter_number = 1
        for chapter in mediainfo.get_chapters(self.file_path):
            start_time, _ = chapter.split(' : ')
            hour, minutes, seconds = start_time.strip().split(':')
            chapters.append({'Number': chapter_number,
                             'Start': float(hour)*3600 + float(minutes)*60 + float(seconds),
                             'Duration': None})

            chapter_number += 1

        if len(chapters) == 0:
            return [{'Number': 1, 'Start': 0, 'Duration': self.duration}]

        chapters.append({'Start': self.duration})
        for idx in range(len(chapters) - 1):
            chapters[idx]['Duration'] = chapters[idx + 1]['Start'] - chapters[idx]['Start']

        chapters.pop(-1)
        return chapters

    @property
    def main_video_track(self):
        return self.video_tracks[0]

    @property
    def main_audio_track(self):
        if len(self.audio_tracks) == 0:
            return None

        return self.audio_tracks[0]

    @property
    def width(self):
        return self.main_video_track.width

    @property
    def height(self):
        return self.main_video_track.height

    @property
    def interlaced(self):
        return self.main_video_track.interlaced

    @property
    def duration(self):
        if self._duration is None:
            self._duration = mediainfo.get_duration(self.file_path)

        hour, minutes, seconds = self._duration.split(':')
        return float(hour)*3600 + float(minutes)*60 + float(seconds)


class VideoTrack:
    def __init__(self, details):
        self._details = details

    @property
    def codec(self):
        return self._details['Codec']

    @property
    def track_number(self):
        return self._details['Track Number']

    @property
    def width(self):
        aspect_ratio = self._details['Aspect Ratio']
        if ':' in aspect_ratio:
            w_ratio, h_ratio = self._details['Aspect Ratio'].split(':')
        else:
            fraction = Fraction(self._details['Aspect Ratio'])
            w_ratio, h_ratio = fraction.numerator, fraction.denominator

        return int(self.height * Fraction(w_ratio) / Fraction(h_ratio))

    @property
    def height(self):
        return int(self._details['Height'])

    @property
    def interlaced(self):
        return self._details['Scan Type'] == 'Interlaced'

    @property
    def frame_rate(self):
        if self._details['Frame Rate'].strip() == '':
            return float(self._details['Original Frame Rate'])

        return float(self._details['Frame Rate'])

    @staticmethod
    def from_mediainfo(dictionaries):
        return [VideoTrack(dic) for dic in dictionaries]


class AudioTrack:
    def __init__(self, details):
        self._details = details

    @property
    def codec(self):
        return self._details['Codec']

    @property
    def channels(self):
        return self._details['Channels'].split('/')[0].strip()

    @property
    def track_number(self):
        return self._details['Track Number']

    @property
    def language(self):
        return self._details['Language']

    @property
    def compression_mode(self):
        return self._details['Compression Mode']

    @staticmethod
    def from_mediainfo(dictionaries):
        return [AudioTrack(dic) for dic in dictionaries]


class SubtitleTrack:
    def __init__(self, details):
        self._details = details

    @property
    def language(self):
        return self._details['Language']

    @property
    def format(self):
        return self._details['Format']

    @staticmethod
    def from_mediainfo(dictionaries):
        return [SubtitleTrack(dic) for dic in dictionaries]
