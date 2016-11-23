import pyfileinfo
from media_converter.wrappers.ffmpeg.ffmpeg_infiles import FFmpegInfile


class FFmpegInstream:
    def __init__(self, infile, stream_type, stream_index):
        if type(infile) is str:
            infile = FFmpegInfile(infile)

        self._infile = infile
        self._stream_type = stream_type
        self._stream_index = stream_index

    @property
    def infile(self):
        return self._infile

    @property
    def stream_type(self):
        return self._stream_type

    @property
    def stream_index(self):
        return self._stream_index


class VideoInstream(FFmpegInstream):
    def __init__(self, infile, stream_index=0):
        FFmpegInstream.__init__(self, infile, 'v', stream_index)
        self._medium = pyfileinfo.load(self.infile.infile_path)

    @property
    def width(self):
        return self._medium.video_tracks[self.stream_index].width

    @property
    def height(self):
        return self._medium.video_tracks[self.stream_index].height


class AudioInstream(FFmpegInstream):
    def __init__(self, infile, stream_index=0):
        FFmpegInstream.__init__(self, infile, 'a', stream_index)
        self._medium = pyfileinfo.load(self.infile.infile_path)

    @property
    def codec(self):
        return self._medium.audio_tracks[self.stream_index].codec

    @property
    def channels(self):
        return self._medium.audio_tracks[self.stream_index].channels


class SubtitleInstream(FFmpegInstream):
    def __init__(self, infile, stream_index=0):
        if type(infile) is str:
            infile = FFmpegInfile(infile)

        FFmpegInstream.__init__(self, infile, 's', stream_index)


class FFmpegOutstream:
    def __init__(self, instream, stream_type, target_codec):
        self._instream = instream
        self._effects = []
        self._stream_type = stream_type
        self._target_codec = target_codec

    def _add_effect(self, effect_name, instream=None, **kwargs):
        self._effects.append({'effect_name': effect_name, 'instream': instream, 'args': kwargs})

    @property
    def instream(self):
        return self._instream

    @property
    def effects(self):
        return self._effects

    @property
    def stream_type(self):
        return self._stream_type

    @property
    def target_codec(self):
        return self._target_codec


class VideoOutstream(FFmpegOutstream):
    def __init__(self, instream, target_codec):
        if type(instream) is str:
            instream = FFmpegInfile(instream)

        if isinstance(instream, FFmpegInfile):
            instream = FFmpegInstream(instream, 'v', 0)

        FFmpegOutstream.__init__(self, instream, 'v', target_codec)

    def add_overlay(self, instream, x=0, y=0):
        if type(instream) is str:
            instream = FFmpegInfile(instream)

        if type(instream) is FFmpegInfile:
            instream = FFmpegInstream(instream, 'v', 0)

        self._add_effect('overlay', instream, x=x, y=y)

    def add_scale(self, width, height, scale_type='STRETCH'):
        if scale_type == 'FILL':
            scale = max(width/self.width, height/self.height)
            scaled_width = self.width * scale
            scaled_height = self.height * scale
            scaled_width -= scaled_width % 2
            scaled_height -= scaled_height % 2

            self._add_effect('scale', width=scaled_width, height=scaled_height)
            self._add_effect('crop', width=width, height=height, x=(scaled_width-width)//2, y=(scaled_height-height)//2)
            return

        if scale_type == 'FIT':
            scale = min(width/self.width, height/self.height)
            width = self.width * scale
            height = self.height * scale

            width -= width % 2
            height -= height % 2

        self._add_effect('scale', width=width, height=height)

    def add_subtitle(self, subtitle_path):
        self._add_effect('subtitle', subtitle_path=subtitle_path)

    def add_deinterlace(self):
        self._add_effect('yadif')

    def add_presentation_timestamp(self, pts):
        self._add_effect('presentation_timestamp', pts=pts)

    @property
    def width(self):
        width = self.instream.width
        for effect in self.effects:
            if 'width' in effect['args']:
                width = int(effect['args']['width'])

        return width

    @property
    def height(self):
        height = self.instream.height
        for effect in self.effects:
            if 'height' in effect['args']:
                height = int(effect['args']['height'])

        return height


class AudioOutstream(FFmpegOutstream):
    def __init__(self, instream, target_codec):
        if type(instream) is str:
            instream = FFmpegInfile(instream)

        if type(instream) is FFmpegInfile:
            instream = FFmpegInstream(instream, 'a', 0)

        FFmpegOutstream.__init__(self, instream, 'a', target_codec)

    def add_volume(self, db):
        self._add_effect('volume', volume=db)
