import unittest

from media_converter.wrappers.ffmpeg.ffmpeg_infiles import FFmpegInfile, FFmpegInfileImageSequence,\
    FFmpegInfileImage, FFmpegInfileSilentAudio


class TestFFmpeg(unittest.TestCase):
    def test_eq_ffmpeg_infile(self):
        lhs = FFmpegInfile('a.mkv')
        rhs = FFmpegInfile('a.mkv')

        self.assertEqual(lhs, rhs)

    def test_ne_ffmpeg_infile(self):
        lhs = FFmpegInfile('a.mkv')
        rhs = FFmpegInfile('b.mkv')

        self.assertNotEqual(lhs, rhs)

    def test_eq_ffmpeg_image_sequence(self):
        lhs = FFmpegInfileImageSequence('a-05d.png', 30)
        rhs = FFmpegInfileImageSequence('a-05d.png', 30)

        self.assertEqual(lhs, rhs)

    def test_eq_ffmpeg_image(self):
        lhs = FFmpegInfileImage('a.png')
        rhs = FFmpegInfileImage('a.png')

        self.assertEqual(lhs, rhs)

    def test_eq_silent_audio(self):
        lhs = FFmpegInfileSilentAudio()
        rhs = FFmpegInfileSilentAudio()

        self.assertEqual(lhs, rhs)

    def test_ne_other_type(self):
        lhs = FFmpegInfileSilentAudio()
        rhs = FFmpegInfileImage('a.png')

        self.assertNotEqual(lhs, rhs)
