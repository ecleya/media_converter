from unittest import TestCase, mock
from media_converter import MediaConverter, codecs
from media_converter.streams import VideoOutstream, AudioOutstream


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

    @mock.patch('subprocess.call')
    def test_video_convert(self, mock_subprocess):
        MediaConverter([VideoOutstream('a.mp4', codecs.MPEG2('3000k', '16:9', '23.97')),
                        AudioOutstream('a.mp4', codecs.AAC('256k', 2, 44100))], 'b.mp4').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-i', 'a.mp4',
               '-c:v', 'mpeg', '-b:v', '3000k', '-aspect', '16:9', '-r', '23.97',
               '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-ar', '44100',
               'b.mp4']
        mock_subprocess.assert_called_with(cmd)
