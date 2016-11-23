import importlib


class Codec:
    def __init__(self):
        pass

    @staticmethod
    def get_codec_by_name(codec_name):
        module = importlib.import_module('media_converter.wrappers.codec')
        return getattr(module, codec_name.upper())

    def is_video_codec(self):
        return isinstance(self, VideoCodec)

    def is_audio_codec(self):
        return isinstance(self, AudioCodec)

    def is_subtitle_codec(self):
        return isinstance(self, SubtitleCodec)


class VideoCodec(Codec):
    def __init__(self):
        Codec.__init__(self)


class AudioCodec(Codec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        Codec.__init__(self)
        self._bitrate = bitrate
        self._channels = channels
        self._sampling_rate = sampling_rate


class LosslessAudioCodec(AudioCodec):
    def __init__(self, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, None, channels, sampling_rate)


class SubtitleCodec(Codec):
    def __init__(self):
        Codec.__init__(self)


class H264(VideoCodec):
    def __init__(self, constant_rate_factor, quantization_parameter, pixel_format, profile, level,
                 aspect_ratio, frame_rate):
        VideoCodec.__init__(self)
        self._constant_rate_factor = constant_rate_factor
        self._quantization_parameter = quantization_parameter
        self._pixel_format = pixel_format
        self._profile = profile
        self._level = level
        self._aspect_ratio = aspect_ratio
        self._frame_rate = frame_rate


class MPEG2(VideoCodec):
    def __init__(self, bitrate, aspect_ratio, frame_rate):
        VideoCodec.__init__(self)
        self._bitrate = bitrate
        self._aspect_ratio = aspect_ratio
        self._frame_rate = frame_rate


class AAC(AudioCodec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)


class AC3(AudioCodec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)


class EAC3(AudioCodec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)


class ALAC(LosslessAudioCodec):
    def __init__(self, channels=None, sampling_rate=None):
        LosslessAudioCodec.__init__(self, channels, sampling_rate)


class FLAC(LosslessAudioCodec):
    def __init__(self, channels=None, sampling_rate=None):
        LosslessAudioCodec.__init__(self, channels, sampling_rate)


class PCMS16LE(LosslessAudioCodec):
    def __init__(self, channels=None, sampling_rate=None):
        LosslessAudioCodec.__init__(self, channels, sampling_rate)


class MP2(AudioCodec):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AudioCodec.__init__(self, bitrate, channels, sampling_rate)


class SRT(SubtitleCodec):
    def __init__(self):
        super(SRT, self).__init__()
