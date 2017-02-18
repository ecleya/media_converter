from unittest import TestCase, mock
from media_converter import MediaConverter, codecs
from media_converter.streams import AudioOutstream


class TestMediaConverter(TestCase):
    @mock.patch('subprocess.call')
    def test_simple_convert(self, mock_subprocess):
        MediaConverter('a.mkv', 'b.mp4').convert()

        mock_subprocess.assert_called_with(['/usr/local/bin/ffmpeg', '-i', 'a.mkv', 'b.mp4'])
