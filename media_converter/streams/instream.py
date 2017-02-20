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

    def as_ffmpeg_instream(self):
        return ['-i', self._file_path]


class VideoInstream(Instream):
    def __init__(self, file_path, track_index=0):
        Instream.__init__(self, file_path, 'v', track_index)

    def __eq__(self, other):
        if type(other) is not VideoInstream:
            return False

        return self.file_path == other.file_path and self.track_index == other.track_index


class AudioInstream(Instream):
    def __init__(self, file_path, track_index=0):
        Instream.__init__(self, file_path, 'a', track_index)

    def __eq__(self, other):
        if type(other) is not AudioInstream:
            return False

        return self.file_path == other.file_path and self.track_index == other.track_index


class ImageSequenceInstream(Instream):
    def __init__(self, image_seq_pattern, frame_rate):
        Instream.__init__(self, image_seq_pattern, 'v', 0)
        self._image_seq_pattern = image_seq_pattern
        self._frame_rate = frame_rate

    @property
    def frame_rate(self):
        return self._frame_rate

    def as_ffmpeg_instream(self):
        return ['-r', str(self._frame_rate), '-vsync', '1', '-f', 'image2', '-i', self._image_seq_pattern]

    def __eq__(self, other):
        if type(other) is not ImageSequenceInstream:
            return False

        return self.file_path == other.file_path and self.frame_rate == other.frame_rate


class ImageInstream(Instream):
    def __init__(self, file_path):
        Instream.__init__(self, file_path, 'v', 0)

    def __eq__(self, other):
        if type(other) is not ImageInstream:
            return False

        return self.file_path == other.file_path and self.frame_rate == other.frame_rate


class SilentAudioInstream(Instream):
    def __init__(self, duration):
        Instream.__init__(self, '/dev/zero', 'a', 0)

        self._duration = duration

    @property
    def duration(self):
        return self._duration

    def as_ffmpeg_instream(self):
        return ['-ar', '48000', '-ac', '1', '-f', 's16le', '-t', str(self.duration), '-i', self.infile_path]

    def __eq__(self, other):
        if type(other) is not SilentAudioInstream:
            return False

        return self.duration == other.duration
