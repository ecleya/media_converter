__all__ = ['VideoCodec', 'H264', 'H265', 'MPEG2',
           'AudioCodec', 'MP2', 'AAC', 'AC3', 'MP2',
           'SubtitleCodec', 'SRT',
           'Copy']


class Codec:
    def is_video_codec(self):
        return isinstance(self, VideoCodec)

    def is_audio_codec(self):
        return isinstance(self, AudioCodec)

    def is_subtitle_codec(self):
        return isinstance(self, SubtitleCodec)


class VideoCodec(Codec):
    def __init__(self, bitrate=None, aspect_ratio=None, frame_rate=None):
        Codec.__init__(self)

        self._bitrate = bitrate
        self._aspect_ratio = aspect_ratio
        self._frame_rate = frame_rate

    @property
    def bitrate(self):
        return self._bitrate

    @property
    def aspect_ratio(self):
        return self._aspect_ratio

    @property
    def frame_rate(self):
        return self._frame_rate


class AudioCodec(Codec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        Codec.__init__(self)
        self._bitrate = bitrate
        self._channels = channels
        self._sampling_rate = sampling_rate

    @property
    def bitrate(self):
        return self._bitrate

    @property
    def channels(self):
        return self._channels

    @property
    def sampling_rate(self):
        return self._sampling_rate


class SubtitleCodec(Codec):
    def __init__(self):
        Codec.__init__(self)


class H264(VideoCodec):
    def __init__(self, bitrate=None, constant_rate_factor=23, quantization_parameter=None,
                 pixel_format='yuv420p', profile='high', level='3.1',
                 aspect_ratio=None, frame_rate=None):
        VideoCodec.__init__(self, bitrate, aspect_ratio, frame_rate)

        self._constant_rate_factor = str(constant_rate_factor)
        self._quantization_parameter = str(quantization_parameter)
        self._pixel_format = pixel_format
        self._profile = profile
        self._level = level

    def options_for_ffmpeg(self):
        options = ['-c:v', 'h264']
        options.extend(['-crf', self._constant_rate_factor] if self._bitrate is None else ['-b:v', self._bitrate])
        options.extend(['-pix_fmt', self._pixel_format, '-profile:v', self._profile, '-level', self._level])

        if self._aspect_ratio is not None:
            options.extend(['-aspect', str(self.aspect_ratio)])
        if self._frame_rate is not None:
            options.extend(['-r', str(self.frame_rate)])

        return options


class H265(VideoCodec):
    def __init__(self, constant_rate_factor=23, preset='medium',
                 aspect_ratio=None, frame_rate=None):
        VideoCodec.__init__(self, None, aspect_ratio, frame_rate)

        self._constant_rate_factor = str(constant_rate_factor)

    def options_for_ffmpeg(self):
        options = ['-c:v', 'libx265']
        options.extend(['-preset', 'slow', '-x265-params', f'crf={self._constant_rate_factor}'])

        if self._aspect_ratio is not None:
            options.extend(['-aspect', str(self.aspect_ratio)])
        if self._frame_rate is not None:
            options.extend(['-r', str(self.frame_rate)])

        return options


class MPEG2(VideoCodec):
    def __init__(self, bitrate, aspect_ratio=None, frame_rate=None):
        VideoCodec.__init__(self, bitrate, aspect_ratio, frame_rate)

    def options_for_ffmpeg(self):
        options = ['-c:v', 'mpeg2video', '-b:v', str(self.bitrate)]
        if self._aspect_ratio is not None:
            options.extend(['-aspect', str(self.aspect_ratio)])
        if self._frame_rate is not None:
            options.extend(['-r', str(self.frame_rate)])

        return options


class PNGSequence(VideoCodec):
    def __init__(self):
        VideoCodec.__init__(self, None, None, None)

    def options_for_ffmpeg(self):
        return ['-f', 'image2', '-pix_fmt', 'rgb32']


class AAC(AudioCodec):
    def __init__(self, bitrate='192k', channels='2', sampling_rate='44100'):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)

    def options_for_ffmpeg(self):
        return ['-c:a', 'aac', '-b:a', str(self.bitrate), '-ac', str(self.channels), '-ar', str(self.sampling_rate)]


class AC3(AudioCodec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)

    def options_for_ffmpeg(self):
        return ['-c:a', 'ac3', '-b:a', str(self.bitrate), '-ac', str(self.channels), '-ar', str(self.sampling_rate)]


class MP2(AudioCodec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)

    def options_for_ffmpeg(self):
        return ['-c:a', 'mp2', '-b:a', str(self.bitrate), '-ac', str(self.channels), '-ar', str(self.sampling_rate)]


class SRT(SubtitleCodec):
    def __init__(self):
        super(SRT, self).__init__()


class Copy(Codec):
    pass


class VideoCopy(VideoCodec):
    def options_for_ffmpeg(self):
        return ['-c:v', 'copy']


class AudioCopy(AudioCodec):
    def options_for_ffmpeg(self):
        return ['-c:a', 'copy']


class SubtitleCopy(SubtitleCodec):
    def options_for_ffmpeg(self):
        return ['-c:s', 'copy']
