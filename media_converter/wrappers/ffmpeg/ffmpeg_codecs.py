from media_converter.wrappers import H264, AAC, ALAC, PCMS16LE, MPEG2, MP2, AC3, EAC3, FLAC


class FFmpegCodecMixin:
    def __init__(self, codec_name):
        self._codec_name = codec_name

    def get_ffmpeg_options(self, track_no=0):
        raise NotImplemented

    @property
    def codec(self):
        raise NotImplemented


class FFmpegVideoCodecMixin(FFmpegCodecMixin):
    def __init__(self, codec_name):
        FFmpegCodecMixin.__init__(self, codec_name)


class VideoCopyFFmpegCodec(FFmpegVideoCodecMixin):
    def __init__(self):
        FFmpegVideoCodecMixin.__init__(self, None)

    def get_ffmpeg_options(self, track_no=0):
        return ['-c:v:%d' % track_no, 'copy']


class H264FFmpegCodec(H264, FFmpegVideoCodecMixin):
    def __init__(self, constant_rate_factor=18.0, quantization_parameter=None, pixel_format='yuv420p', profile='high',
                 level='4.0', aspect_ratio=None, frame_rate=None):
        H264.__init__(self, constant_rate_factor, quantization_parameter, pixel_format, profile,
                      level, aspect_ratio, frame_rate)
        FFmpegVideoCodecMixin.__init__(self, 'h264')

    def get_ffmpeg_options(self, track_no=0):
        options = ['-c:v', self._codec_name]
        options.extend(['-crf', str(self._constant_rate_factor)]
                       if self._quantization_parameter is None else ['-qp', str(self._quantization_parameter)])
        options.extend(['-pix_fmt', self._pixel_format])
        if self._quantization_parameter != 0:
            options.extend(['-profile:v', self._profile])
            options.extend(['-level', self._level])
        if self._aspect_ratio is not None:
            options.extend(['-aspect', self._aspect_ratio])
        if self._frame_rate is not None:
            options.extend(['-r', str(self._frame_rate)])

        return options

    @property
    def codec(self):
        return 'V_MPEG4/ISO/AVC'


class MPEG2FFmpegCodec(MPEG2, FFmpegVideoCodecMixin):
    def __init__(self, bitrate='10000k', aspect_ratio=None, frame_rate=None):
        MPEG2.__init__(self, bitrate, aspect_ratio, frame_rate)
        FFmpegVideoCodecMixin.__init__(self, 'mpeg2video')

    def get_ffmpeg_options(self, track_no=0):
        options = ['-c:v', self._codec_name]
        options.extend(['-b:v', str(self._bitrate)])
        if self._aspect_ratio is not None:
            options.extend(['-aspect', self._aspect_ratio])
        if self._frame_rate is not None:
            options.extend(['-r', str(self._frame_rate)])

        return options

    @property
    def codec(self):
        return 'MPEG-2V'


class FFmpegAudioCodecMixin(FFmpegCodecMixin):
    def __init__(self, codec_name):
        FFmpegCodecMixin.__init__(self, codec_name)

    def get_ffmpeg_options(self, track_no=0):
        options = ['-c:a:%d' % track_no, self._codec_name]
        if self._bitrate is not None:
            options.extend(['-b:a:%d' % track_no, str(self._bitrate)])
        if self._channels is not None:
            options.extend(['-ac:a:%d' % track_no, str(self._channels)])
        if self._sampling_rate is not None:
            options.extend(['-ar:a:%d' % track_no, str(self._sampling_rate)])

        return options

    @property
    def channels(self):
        return self._channels


class AudioCopyFFmpegCodec(FFmpegAudioCodecMixin):
    def __init__(self):
        FFmpegAudioCodecMixin.__init__(self, None)

    def get_ffmpeg_options(self, track_no=0):
        return ['-c:a:%d' % track_no, 'copy']


class AACFFmpegCodec(AAC, FFmpegAudioCodecMixin):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AAC.__init__(self, bitrate=bitrate, channels=channels, sampling_rate=sampling_rate)
        FFmpegAudioCodecMixin.__init__(self, codec_name='libfdk_aac')

    @property
    def codec(self):
        return 'AAC LC'


class AC3FFmpegCodec(AC3, FFmpegAudioCodecMixin):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        AC3.__init__(self, bitrate=bitrate, channels=channels, sampling_rate=sampling_rate)
        FFmpegAudioCodecMixin.__init__(self, codec_name='ac3')

    @property
    def codec(self):
        return 'AC3'


class EAC3FFmpegCodec(EAC3, FFmpegAudioCodecMixin):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        EAC3.__init__(self, bitrate=bitrate, channels=channels, sampling_rate=sampling_rate)
        FFmpegAudioCodecMixin.__init__(self, codec_name='eac3')

    @property
    def codec(self):
        return 'EAC3'


class ALACFFmpegCodec(ALAC, FFmpegAudioCodecMixin):
    def __init__(self, channels=None, sampling_rate=None):
        ALAC.__init__(self, channels=channels, sampling_rate=sampling_rate)
        FFmpegAudioCodecMixin.__init__(self, codec_name='alac')

    @property
    def codec(self):
        return 'A_ALAC'


class FLACFFmpegCodec(FLAC, FFmpegAudioCodecMixin):
    def __init__(self, channels=None, sampling_rate=None):
        FLAC.__init__(self, channels=channels, sampling_rate=sampling_rate)
        FFmpegAudioCodecMixin.__init__(self, codec_name='flac')

    @property
    def codec(self):
        return 'A_FLAC'


class MP2FFmpegCodec(MP2, FFmpegAudioCodecMixin):
    def __init__(self, bitrate=None, channels=None, sampling_rate=None):
        MP2.__init__(self, bitrate=bitrate, channels=channels, sampling_rate=sampling_rate)
        FFmpegAudioCodecMixin.__init__(self, codec_name='mp2')

    @property
    def codec(self):
        return 'MPEG-1 Audio layer 2'


class PCMS16LEFFmpegCodec(PCMS16LE, FFmpegAudioCodecMixin):
    def __init__(self, channels=None, sampling_rate=None):
        PCMS16LE.__init__(self, channels=channels, sampling_rate=sampling_rate)
        FFmpegAudioCodecMixin.__init__(self, codec_name='pcm_s16le')

    @property
    def codec(self):
        return 'PCM'


class VideoCodecs:
    H264 = H264FFmpegCodec
    MPEG2 = MPEG2FFmpegCodec


class AudioCodecs:
    AAC = AACFFmpegCodec
    AC3 = AC3FFmpegCodec
    EAC3 = EAC3FFmpegCodec
    ALAC = ALACFFmpegCodec
    FLAC = FLACFFmpegCodec
    MP2 = MP2FFmpegCodec
    PCMS16LE = PCMS16LEFFmpegCodec
