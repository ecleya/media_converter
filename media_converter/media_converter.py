import subprocess
from pyfileinfo import PyFileInfo
from media_converter.codecs import VideoCodec, AudioCodec
from media_converter.tracks import Track, AudioTrack, VideoTrack
from media_converter.streams import VideoInstream, AudioInstream, VideoOutstream, AudioOutstream
from media_converter.mixins import TemporaryFileMixin


class MediaConverter(TemporaryFileMixin):
    def __init__(self, tracks, dst):
        TemporaryFileMixin.__init__(self)

        if not isinstance(tracks, list):
            tracks = [tracks]

        self._tracks = tracks
        self._dst = dst
        self._command = None
        self._infiles = None

    def convert(self):
        subprocess.call(self.command)

    @property
    def command(self):
        self._init_command()
        self._append_instreams()
        self._append_tracks()
        self._append_dst()

        return self._command

    def _init_command(self):
        self._command = ['/usr/local/bin/ffmpeg', '-y']
        self._infiles = []

    @property
    def tracks(self):
        for track in self._tracks:
            if isinstance(track, Track):
                yield track

    def _append_instreams(self):
        for track in self._tracks:
            print(track, track.outstream)
            instream = track.outstream.instream
            if instream.as_ffmpeg_instream() in self._infiles:
                continue

            self._infiles.append(instream.as_ffmpeg_instream())
            self._command.extend(instream.as_ffmpeg_instream())

    def _append_tracks(self):
        for track in self._tracks:
            instream = track.outstream.instream
            infile_index = self._infiles.index(instream.as_ffmpeg_instream())
            filter = track.outstream.filter_options_for_ffmpeg(infile_index)
            if len(filter) == 0:
                self._command.extend(['-map', f'{infile_index}:{instream.track_type}:{instream.track_index}'])
            else:
                self._command.extend(['-filter_complex', filter, '-map', '[vout0]'])

            if isinstance(track, VideoTrack):
                codec = track.codec
                self._command.extend(['-c:v', 'mpeg', '-b:v', str(codec.bitrate), '-aspect', str(codec.aspect_ratio), '-r', str(codec.frame_rate)])
            if isinstance(track, AudioTrack):
                codec = track.codec
                self._command.extend(['-c:a', 'aac', '-b:a', str(codec.bitrate), '-ac', str(codec.channels), '-ar', str(codec.sampling_rate)])

    def _append_dst(self):
        self._command.append(self._dst)
