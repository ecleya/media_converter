import unittest

from media_converter.wrappers import Codec
from media_converter.wrappers import H264


class TestFFmpeg(unittest.TestCase):
    def test_get_codec_by_name(self):
        h264_codec = Codec.get_codec_by_name('H264')

        self.assertTrue(h264_codec is H264)
