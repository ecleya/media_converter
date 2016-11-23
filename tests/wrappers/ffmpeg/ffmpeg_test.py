import pytest
import unittest

from media_converter.wrappers.ffmpeg import FFmpeg, VideoOutstream, AudioOutstream,\
    VideoInstream, AudioInstream, SubtitleInstream
from media_converter.wrappers.ffmpeg.ffmpeg_codecs import VideoCodecs, AudioCodecs
from media_converter.wrappers.ffmpeg.ffmpeg_infiles import FFmpegInfileImageSequence

from media_converter.models.medium import Container


class TestFFmpeg(unittest.TestCase):
    def test_transcode_to_lossless_format(self):
        src = 'dummy.mp4'
        video_codec = VideoCodecs.H264(quantization_parameter=0)
        audio_codec = AudioCodecs.ALAC()

        video_outstream = VideoOutstream(src, video_codec)
        audio_outstream = AudioOutstream(src, audio_codec)

        ffmpeg = FFmpeg([video_outstream, audio_outstream], Container.MATROSKA)
        self.assertEqual(ffmpeg.command[:-1],
                         ['/usr/local/bin/ffmpeg', '-y', '-i', src,
                          '-map', '0:v:0', '-c:v', 'h264', '-qp', '0', '-pix_fmt', 'yuv420p',
                          '-map', '0:a:0', '-c:a:0', 'alac', '-threads', '0'])

    def test_mix_track(self):
        srcs = ['a.m4v', 'b.m4v']
        video_codec = VideoCodecs.H264()
        audio_codec = AudioCodecs.AAC(bitrate='256k', channels=2, sampling_rate=48000)

        video_outstream = VideoOutstream(srcs[0], video_codec)
        audio_outstream = AudioOutstream(srcs[1], audio_codec)

        ffmpeg = FFmpeg([video_outstream, audio_outstream], Container.M4V)
        self.assertEqual(ffmpeg.command[:-1],
                         ['/usr/local/bin/ffmpeg', '-y', '-i', srcs[0], '-i', srcs[1],
                          '-map', '0:v:0', '-c:v', 'h264', '-crf', '18.0', '-pix_fmt', 'yuv420p',
                          '-profile:v', 'high', '-level', '4.0',
                          '-map', '1:a:0', '-c:a:0', 'libfdk_aac', '-b:a:0', '256k', '-ac:a:0', '2', '-ar:a:0', '48000',
                          '-threads', '0'])

    def test_analyze_duration_and_probe_size(self):
        src = 'dummy.mp4'
        video_codec = VideoCodecs.H264()
        audio_codec = AudioCodecs.ALAC()

        video_outstream = VideoOutstream(src, video_codec)
        audio_outstream = AudioOutstream(src, audio_codec)

        ffmpeg = FFmpeg([video_outstream, audio_outstream], Container.M4V,
                        analyze_duration=2147483647, probe_size=2147483647)
        self.assertEqual(ffmpeg.command[:-1],
                         ['/usr/local/bin/ffmpeg', '-y',
                          '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', src,
                          '-map', '0:v:0', '-c:v', 'h264', '-crf', '18.0', '-pix_fmt', 'yuv420p',
                          '-profile:v', 'high', '-level', '4.0',
                          '-map', '0:a:0', '-c:a:0', 'alac', '-threads', '0'])

    @pytest.mark.skip
    def test_multiple_audio_track(self):
        src = 'a.m4v'
        video_codec = VideoCodecs.H264()
        audio_codec = AudioCodecs.AAC(bitrate='256k', channels=2, sampling_rate=48000)

        video_outstream = VideoOutstream(src, video_codec)
        audio_outstream1 = AudioOutstream(AudioInstream(src, 0), audio_codec)
        audio_outstream2 = AudioOutstream(AudioInstream(src, 3), audio_codec)

        ffmpeg = FFmpeg([video_outstream, audio_outstream1, audio_outstream2], Container.M4V)
        self.assertEqual(ffmpeg.command[:-1],
                         ['/usr/local/bin/ffmpeg', '-y', '-i', src,
                          '-map', '0:v:0', '-c:v', 'h264', '-crf', '18.0', '-pix_fmt', 'yuv420p',
                          '-profile:v', 'high', '-level', '4.0',
                          '-map', '0:a:0', '-c:a:0', 'libfdk_aac', '-b:a:0', '256k', '-ac:a:0', '2', '-ar:a:0', '48000',
                          '-map', '0:a:3', '-c:a:1', 'libfdk_aac', '-b:a:1', '256k', '-ac:a:1', '2', '-ar:a:1', '48000',
                          '-threads', '0'])

    def test_hardburn_image_subtitle(self):
        src = 'a.mkv'
        video_codec = VideoCodecs.H264(constant_rate_factor=13.0)
        audio_codec = AudioCodecs.AAC(bitrate='256k', channels=2, sampling_rate=48000)

        video_outstream = VideoOutstream(src, video_codec)
        video_outstream.add_overlay(SubtitleInstream(src))
        audio_outstream = AudioOutstream(src, audio_codec)

        ffmpeg = FFmpeg([video_outstream, audio_outstream], Container.M4V)
        self.assertEqual(ffmpeg.command[:-1],
                         ['/usr/local/bin/ffmpeg', '-y', '-i', src,
                          '-filter_complex', "[0:v][0:s:0]overlay=0:0[vf0_out]",
                          '-map', '[vf0_out]', '-c:v', 'h264', '-crf', '13.0', '-pix_fmt', 'yuv420p',
                          '-profile:v', 'high', '-level', '4.0',
                          '-map', '0:a:0', '-c:a:0', 'libfdk_aac', '-b:a:0', '256k', '-ac:a:0', '2', '-ar:a:0', '48000',
                          '-threads', '0'])

    def test_hardburn_text_subtitle(self):
        src = 'a.mkv'
        subtitle_path = 'b.srt'
        video_codec = VideoCodecs.H264(constant_rate_factor=13.0)
        audio_codec = AudioCodecs.AAC(bitrate='256k', channels=2, sampling_rate=48000)

        video_outstream = VideoOutstream(src, video_codec)
        video_outstream.add_subtitle(subtitle_path)
        audio_outstream = AudioOutstream(src, audio_codec)

        ffmpeg = FFmpeg([video_outstream, audio_outstream], Container.M4V)
        self.assertEqual(ffmpeg.command[:-1],
                         ['/usr/local/bin/ffmpeg', '-y', '-i', src,
                          '-filter_complex', "[0:v]subtitles=%s[vf0_out]" % subtitle_path,
                          '-map', '[vf0_out]', '-c:v', 'h264', '-crf', '13.0', '-pix_fmt', 'yuv420p',
                          '-profile:v', 'high', '-level', '4.0',
                          '-map', '0:a:0', '-c:a:0', 'libfdk_aac', '-b:a:0', '256k', '-ac:a:0', '2', '-ar:a:0', '48000',
                          '-threads', '0'])

    @pytest.mark.skip
    def test_overlay_watermark_image(self):
        video_in = 'a.mkv'
        image_in = 'a.png'
        video_codec = VideoCodecs.H264(constant_rate_factor=13.0)
        audio_codec = AudioCodecs.AAC(bitrate='256k', channels=2, sampling_rate=48000)

        video_outstream = VideoOutstream(video_in, video_codec)
        video_outstream.add_overlay(VideoInstream(image_in))
        audio_outstream = AudioOutstream(video_in, audio_codec)

        ffmpeg = FFmpeg([video_outstream, audio_outstream], Container.M4V)
        self.assertEqual(ffmpeg.command[:-1],
                         ['/usr/local/bin/ffmpeg', '-y', '-i', video_in, '-i', image_in,
                          '-filter_complex', '[0:v][1:v:0]overlay=0:0[vf0_out]',
                          '-map', '[vf0_out]', '-c:v', 'h264', '-crf', '13.0', '-pix_fmt', 'yuv420p',
                          '-profile:v', 'high', '-level', '4.0',
                          '-map', '0:a:0', '-c:a:0', 'libfdk_aac', '-b:a:0', '256k', '-ac:a:0', '2', '-ar:a:0', '48000',
                          '-threads', '0'])

    def test_make_video_from_image_sequence(self):
        sequence_pattern = 'vid-%09d.png'
        frame_rate_of_images = 30
        audio_in = 'a.flac'
        video_codec = VideoCodecs.MPEG2()
        audio_codec = AudioCodecs.FLAC(channels=2, sampling_rate=48000)

        video_outstream = VideoOutstream(FFmpegInfileImageSequence(sequence_pattern, frame_rate=frame_rate_of_images),
                                         video_codec)
        audio_outstream = AudioOutstream(audio_in, audio_codec)

        ffmpeg = FFmpeg([video_outstream, audio_outstream], Container.MATROSKA)
        self.assertEqual(ffmpeg.command[:-1],
                         ['/usr/local/bin/ffmpeg', '-y', '-r', str(frame_rate_of_images), '-vsync', '1', '-f',
                          'image2', '-i', sequence_pattern,
                          '-i', audio_in,
                          '-map', '0:v:0', '-c:v', 'mpeg2video', '-b:v', '10000k',
                          '-map', '1:a:0', '-c:a:0', 'flac', '-ac:a:0', '2', '-ar:a:0', '48000',
                          '-threads', '0'])

    def test_video_presentation_timestamp(self):
        src = 'a.mkv'
        video_codec = VideoCodecs.H264(constant_rate_factor=13.0)
        audio_codec = AudioCodecs.AAC(bitrate='256k', channels=2, sampling_rate=48000)

        video_outstream = VideoOutstream(src, video_codec)
        video_outstream.add_presentation_timestamp(0.5)
        audio_outstream = AudioOutstream(src, audio_codec)

        ffmpeg = FFmpeg([video_outstream, audio_outstream], Container.MATROSKA)
        self.assertEqual(ffmpeg.command[:-1],
                         ['/usr/local/bin/ffmpeg', '-y', '-i', src,
                          '-filter_complex', '[0:v]setpts=0.5*PTS[vf0_out]',
                          '-map', '[vf0_out]', '-c:v', 'h264', '-crf', '13.0', '-pix_fmt', 'yuv420p', '-profile:v',
                          'high', '-level', '4.0',
                          '-map', '0:a:0', '-c:a:0', 'libfdk_aac', '-b:a:0', '256k', '-ac:a:0', '2', '-ar:a:0', '48000',
                          '-threads', '0'])
