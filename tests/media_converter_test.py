from unittest import TestCase, mock
from media_converter import MediaConverter, codecs
from media_converter.streams import AudioOutstream


class TestMediaConverter(TestCase):
    @mock.patch('subprocess.call')
    def test_simple_convert(self, mock_subprocess):
        MediaConverter('a.mkv', 'b.mp4').convert()

        mock_subprocess.assert_called_with(['/usr/local/bin/ffmpeg', '-y', '-i', 'a.mkv', 'b.mp4'])

    @mock.patch('subprocess.call')
    def test_audio_convert(self, mock_subprocess):
        MediaConverter(AudioOutstream('a.wav', codecs.AAC('256k', 2, 44100)), 'a.m4a').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-i', 'a.wav',
               '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-ar', '44100',
               'a.m4a']
        mock_subprocess.assert_called_with(cmd)
