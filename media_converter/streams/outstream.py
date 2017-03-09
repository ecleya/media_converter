from media_converter.streams.instream import Instream, VideoInstream, AudioInstream, SubtitleInstream


class Outstream:
    def __init__(self, instream):
        self._instream = instream

    @property
    def instream(self):
        return self._instream


class VideoOutstream(Outstream):
    def __init__(self, instream):
        Outstream.__init__(self, instream if isinstance(instream, Instream) else VideoInstream.factory(instream))

        self._filters = []

    def scale(self, width=None, height=None):
        if width is None:
            width = -2
        if height is None:
            height = -2

        self._filters.append(f'scale={width}:{height}')
        return self

    def filter_options_for_ffmpeg(self, infile_index):
        instream = f'[{infile_index}:{self._instream.track_type}:{self._instream.track_index}]'
        outstream = '[vout0]'
        filters = []
        for filter in self._filters:
            filters.append(f'{instream}{filter}{outstream}')
            instream = outstream
            outstream = '[vout1]'

        return ';'.join(filters)


class AudioOutstream(Outstream):
    def __init__(self, instream):
        Outstream.__init__(self, instream if isinstance(instream, Instream) else AudioInstream.factory(instream))

        self._filters = []

    def filter_options_for_ffmpeg(self, infile_index):
        return ''


class SubtitleOutstream(Outstream):
    def __init__(self, instream):
        Outstream.__init__(self, instream if isinstance(instream, Instream) else SubtitleInstream.factory(instream))

        self._filters = []

    def filter_options_for_ffmpeg(self, infile_index):
        return ''
