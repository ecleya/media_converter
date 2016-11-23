class FFmpegVideoFilter:
    def __init__(self, stream_specifier):
        self._stream_specifier = stream_specifier

    def get_ffmpeg_filter_option(self):
        raise NotImplemented()


class Scale(FFmpegVideoFilter):
    def __init__(self, width, height):
        FFmpegVideoFilter.__init__(self, stream_specifier=None)
        self._width = width
        self._height = height

    def get_ffmpeg_filter_option(self):
        return 'scale=%d:%d' % (self._width, self._height)


class Overlay(FFmpegVideoFilter):
    def __init__(self, stream_specifier, x=0, y=0):
        FFmpegVideoFilter.__init__(self, stream_specifier=stream_specifier)
        self._x = x
        self._y = y

    def get_ffmpeg_filter_option(self):
        return '[%s]overlay=%d:%d' % (self._stream_specifier, self._x, self._y)


class Pad(FFmpegVideoFilter):
    def __init__(self, width, height, x=0, y=0):
        FFmpegVideoFilter.__init__(self, stream_specifier=None)
        self._width = width
        self._height = height
        self._x = x
        self._y = y

    def get_ffmpeg_filter_option(self):
        return 'pad=%d:%d:%d:%d:black' % (self._width, self._height, self._x, self._y)


class Crop(FFmpegVideoFilter):
    def __init__(self, width, height, x=0, y=0):
        FFmpegVideoFilter.__init__(self, stream_specifier=None)
        self._width = width
        self._height = height
        self._x = x
        self._y = y

    def get_ffmpeg_filter_option(self):
        return 'crop=%d:%d:%d:%d' % (self._width, self._height, self._x, self._y)


class Subtitle(FFmpegVideoFilter):
    def __init__(self, subtitle_path=None):
        FFmpegVideoFilter.__init__(self, stream_specifier=None)
        self._subtitle_path = subtitle_path

    def get_ffmpeg_filter_option(self):
        if self._subtitle_path is not None:
            return 'subtitles=%s' % self._subtitle_path

        return ''


class Yadif(FFmpegVideoFilter):
    def __init__(self):
        FFmpegVideoFilter.__init__(self, stream_specifier=None)

    def get_ffmpeg_filter_option(self):
        return 'yadif'


class PresentationTimestamp(FFmpegVideoFilter):
    def __init__(self, pts):
        FFmpegVideoFilter.__init__(self, stream_specifier=None)
        self._pts = pts

    def get_ffmpeg_filter_option(self):
        return 'setpts=%s*PTS' % str(self._pts)


class FFmpegAudioFilter:
    def get_ffmpeg_filter_option(self):
        raise NotImplemented()


class Volume(FFmpegAudioFilter):
    def __init__(self, volume):
        self._volume = volume

    def get_ffmpeg_filter_option(self):
        return 'volume=%fdB' % self._volume
