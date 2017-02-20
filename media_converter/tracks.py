__all__ = ['Track', 'VideoTrack', 'AudioTrack']


class Track:
    def __init__(self, outstream, codec):
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
