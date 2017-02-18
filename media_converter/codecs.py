__all__ = ['VideoCodec', 'H264', 'H265', 'MPEG2',
           'AudioCodec', 'MP2', 'AAC', 'AC3', 'EAC3']


class Codec:
    def is_video_codec(self):
        return isinstance(self, VideoCodec)

    def is_audio_codec(self):
        return isinstance(self, AudioCodec)

    def is_subtitle_codec(self):
        return isinstance(self, SubtitleCodec)


class VideoCodec(Codec):
    def __init__(self, aspect_ratio=None, frame_rate=None):
        Codec.__init__(self)

        self._frame_rate = frame_rate


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
    def __init__(self, constant_rate_factor, quantization_parameter, pixel_format, profile, level,
                 aspect_ratio, frame_rate):
        VideoCodec.__init__(self, frame_rate)

        self._constant_rate_factor = constant_rate_factor
        self._quantization_parameter = quantization_parameter
        self._pixel_format = pixel_format
        self._profile = profile
        self._level = level
        self._aspect_ratio = aspect_ratio


class H265(VideoCodec):
    def __init__(self, constant_rate_factor, quantization_parameter, pixel_format, profile, level,
                 aspect_ratio, frame_rate):
        VideoCodec.__init__(self, frame_rate)

        self._constant_rate_factor = constant_rate_factor
        self._quantization_parameter = quantization_parameter
        self._pixel_format = pixel_format
        self._profile = profile
        self._level = level
        self._aspect_ratio = aspect_ratio


class MPEG2(VideoCodec):
    def __init__(self, bitrate, aspect_ratio, frame_rate):
        VideoCodec.__init__(self, frame_rate)

        self._bitrate = bitrate
        self._aspect_ratio = aspect_ratio


class AAC(AudioCodec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)


class AC3(AudioCodec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)


class EAC3(AudioCodec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)


class MP2(AudioCodec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)


class SRT(SubtitleCodec):
    def __init__(self):
        super(SRT, self).__init__()
