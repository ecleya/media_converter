from media_converter.codecs import VideoCodec, AudioCodec
from media_converter.streams import VideoOutstream, AudioOutstream, Outstream


__all__ = ['Track', 'VideoTrack', 'AudioTrack']


class Track:
    def __init__(self, outstream, codec, **kwargs):
        if not isinstance(outstream, Outstream):
            if isinstance(codec, VideoCodec):
                outstream = VideoOutstream(outstream, **kwargs)
            elif isinstance(codec, AudioCodec):
                outstream = AudioOutstream(outstream, **kwargs)

        self._outstream = outstream
        self._codec = codec

    @property
    def outstream(self):
        return self._outstream

    @property
    def codec(self):
        return self._codec


class VideoTrack(Track):
    pass


class AudioTrack(Track):
    pass
