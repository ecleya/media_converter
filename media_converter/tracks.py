from media_converter.codecs import Copy, VideoCopy, AudioCopy, SubtitleCopy
from media_converter.streams import VideoOutstream, AudioOutstream, SubtitleOutstream, Outstream


__all__ = ['Track', 'VideoTrack', 'AudioTrack', 'SubtitleTrack']


class Track:
    def __init__(self, outstream, codec, default, language):
        self._outstream = outstream
        self._codec = codec
        self._default = default
        self._language = language

    @property
    def outstream(self):
        return self._outstream

    @property
    def codec(self):
        return self._codec

    @property
    def default(self):
        return self._default

    @property
    def language(self):
        return self._language


class VideoTrack(Track):
    def __init__(self, outstream, codec, default=False, language=None):
        if not isinstance(outstream, Outstream):
            outstream = VideoOutstream(outstream)
        if isinstance(codec, Copy):
            codec = VideoCopy()

        Track.__init__(self, outstream, codec, default, language)


class AudioTrack(Track):
    def __init__(self, outstream, codec, default=False, language=None):
        if not isinstance(outstream, Outstream):
            outstream = AudioOutstream(outstream)
        if isinstance(codec, Copy):
            codec = AudioCopy()

        Track.__init__(self, outstream, codec, default, language)


class SubtitleTrack(Track):
    def __init__(self, outstream, codec, default=False, language=None):
        if not isinstance(outstream, Outstream):
            outstream = SubtitleOutstream(outstream)
        if isinstance(codec, Copy):
            codec = SubtitleCopy()

        Track.__init__(self, outstream, codec, default, language)
