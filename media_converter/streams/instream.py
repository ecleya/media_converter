from pyfileinfo import PyFileInfo


class Instream:
    def __init__(self, file_path, track_type, track_index):
        self._file_path = file_path
        self._track_type = track_type
        self._track_index = track_index

    @property
    def file_path(self):
        return self._file_path

    @property
    def track_type(self):
        return self._track_type

    @property
    def track_index(self):
        return self._track_index

    def is_blank(self):
        return False

    def as_ffmpeg_instream(self):
        return ['-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', self._file_path]


class VideoInstream(Instream):
    def __init__(self, file_path, track_index=0):
        Instream.__init__(self, file_path, 'v', track_index)

    @staticmethod
    def factory(file_path):
        if BlackVideoInstream.is_valid(file_path):
            return BlackVideoInstream()

        if ImageSequenceInstream.is_valid(file_path):
            return ImageSequenceInstream(file_path)

        if ImageInstream.is_valid(file_path):
            return ImageInstream(file_path)

        return VideoInstream(file_path, 0)


class ImageSequenceInstream(VideoInstream):
    def __init__(self, image_seq_pattern, frame_rate=30):
        VideoInstream.__init__(self, image_seq_pattern, 0)

        self._image_seq_pattern = image_seq_pattern
        self._frame_rate = frame_rate

    @property
    def frame_rate(self):
        return self._frame_rate

    @staticmethod
    def is_valid(file_path):
        try:
            return file_path != file_path % 1
        except:
            return False

    def as_ffmpeg_instream(self):
        return ['-r', str(self._frame_rate), '-vsync', '1', '-f', 'image2', '-i', self._image_seq_pattern]


class ImageInstream(VideoInstream):
    def __init__(self, file_path):
        VideoInstream.__init__(self, file_path, 0)

    @staticmethod
    def is_valid(file_path):
        return PyFileInfo(file_path).is_image()

    def as_ffmpeg_instream(self):
        return ['-i', self._file_path]


class BlackVideoInstream(VideoInstream):
    def __init__(self, width=640, height=360, duration=None, frame_rate=30):
        VideoInstream.__init__(self, '/dev/zero', 0)

        self._width = width
        self._height = height
        self._duration = duration
        self._frame_rate = frame_rate

    @staticmethod
    def is_valid(file_path):
        return file_path is None or file_path.lower() in ['/dev/zero', 'null']

    @property
    def duration(self):
        return self._duration

    def is_blank(self):
        return True

    def as_ffmpeg_instream(self):
        options = [] if self._duration is None else ['-t', str(self.duration)]
        return options + ['-s', f'{self._width}x{self._height}', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-r', str(self._frame_rate), '-i', self.file_path]


class AudioInstream(Instream):
    def __init__(self, file_path, track_index=0):
        Instream.__init__(self, file_path, 'a', track_index)

    @staticmethod
    def factory(file_path):
        if SilentAudioInstream.is_valid(file_path):
            return SilentAudioInstream()

        return AudioInstream(file_path, 0)


class SilentAudioInstream(AudioInstream):
    def __init__(self, duration=None):
        AudioInstream.__init__(self, '/dev/zero', 0)

        self._duration = duration

    @staticmethod
    def is_valid(file_path):
        return file_path is None or file_path.lower() in ['/dev/zero', 'null']

    @property
    def duration(self):
        return self._duration

    def is_blank(self):
        return True

    def as_ffmpeg_instream(self):
        options = [] if self._duration is None else ['-t', str(self.duration)]
        return options + ['-ar', '48000', '-ac', '1', '-f', 's16le',  '-i', self.file_path]


class SubtitleInstream(Instream):
    def __init__(self, file_path, track_index=0):
        Instream.__init__(self, file_path, 's', track_index)

    @staticmethod
    def factory(file_path):
        return SubtitleInstream(file_path, 0)
