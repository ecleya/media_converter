class Outstream:
    def __init__(self, instream):
        self._instream = instream

    @property
    def instream(self):
        return self._instream


class VideoOutstream(Outstream):
    pass


class AudioOutstream(Outstream):
    pass
