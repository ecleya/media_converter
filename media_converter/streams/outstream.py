class Outstream:
    def __init__(self, instream, codec):
        self._instream = instream
        self._codec = codec

    @property
    def instream(self):
        return self._instream

    @property
    def codec(self):
        return self._codec


class VideoOutstream(Outstream):
    pass


class AudioOutstream(Outstream):
    pass
