class FFmpegInfile:
    def __init__(self, infile_path):
        self._infile_path = infile_path

    def get_ffmpeg_options(self):
        return ['-i', self._infile_path]

    def __eq__(self, other):
        if type(other) is not type(self):
            return False

        return self._infile_path == other.infile_path

    @property
    def infile_path(self):
        return self._infile_path

    @property
    def width(self):
        return self


class FFmpegInfileImageSequence(FFmpegInfile):
    def __init__(self, image_sequence_pattern, frame_rate):
        FFmpegInfile.__init__(self, image_sequence_pattern)
        self._frame_rate = frame_rate

    def get_ffmpeg_options(self):
        return ['-r', str(self._frame_rate), '-vsync', '1', '-f', 'image2', '-i', self._infile_path]

    def __eq__(self, other):
        if type(other) is not FFmpegInfileImageSequence:
            return False

        return self._infile_path == other.infile_path and self._frame_rate == other.frame_rate

    @property
    def frame_rate(self):
        return self._frame_rate


class FFmpegInfileImage(FFmpegInfile):
    def __init__(self, infile_path):
        FFmpegInfile.__init__(self, infile_path)

    def get_ffmpeg_options(self):
        return ['-i', self._infile_path]


class FFmpegInfileSilentAudio(FFmpegInfile):
    def __init__(self):
        FFmpegInfile.__init__(self, '/dev/zero')

    def get_ffmpeg_options(self):
        return ['-ar', '48000', '-ac', '1', '-f', 's16le', '-i', self._infile_path]

    def __eq__(self, other):
        return type(other) is FFmpegInfileSilentAudio
