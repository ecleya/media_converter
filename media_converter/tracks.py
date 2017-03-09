from media_converter.codecs import Copy, VideoCopy, AudioCopy, SubtitleCopy
from media_converter.streams import VideoOutstream, AudioOutstream, SubtitleOutstream, Outstream


__all__ = ['Track', 'VideoTrack', 'AudioTrack']


class Track:
    def __init__(self, outstream, codec, **kwargs):
        self._outstream = outstream
        self._codec = codec

    @property
    def outstream(self):
        return self._outstream

    @property
    def codec(self):
        return self._codec


class VideoTrack(Track):
    def __init__(self, outstream, codec, **kwargs):
        if not isinstance(outstream, Outstream):
            outstream = VideoOutstream(outstream, **kwargs)
        if isinstance(codec, Copy):
            codec = VideoCopy()

        Track.__init__(self, outstream, codec, **kwargs)


class AudioTrack(Track):
    def __init__(self, outstream, codec, **kwargs):
        if not isinstance(outstream, Outstream):
            outstream = AudioOutstream(outstream, **kwargs)
        if isinstance(codec, Copy):
            codec = AudioCopy()

        Track.__init__(self, outstream, codec, **kwargs)


class SubtitleTrack(Track):
    def __init__(self, outstream, codec, **kwargs):
        if not isinstance(outstream, Outstream):
            outstream = SubtitleOutstream(outstream, **kwargs)
        if isinstance(codec, Copy):
            codec = SubtitleCopy()

        Track.__init__(self, outstream, codec, **kwargs)

