from unittest import TestCase, mock, skip
from media_converter import MediaConverter, codecs
from media_converter.tracks import VideoTrack, AudioTrack
from media_converter.streams import VideoOutstream


class TestMediaConverter(TestCase):
    @skip
    @mock.patch('subprocess.call')
    def test_simple_convert(self, mock_subprocess):
        MediaConverter('a.mkv', 'b.mp4').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y', '-i', 'a.mkv', 'b.mp4']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_audio_convert(self, mock_subprocess):
        MediaConverter(AudioTrack('a.wav', codecs.AAC('256k', 2, 44100)), 'a.m4a').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-i', 'a.wav',
               '-map', '0:a:0', '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-ar', '44100',
               'a.m4a']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_video_convert(self, mock_subprocess):
        MediaConverter([VideoTrack('a.mp4', codecs.MPEG2('3000k', '16:9', '23.97')),
                        AudioTrack('a.mp4', codecs.AAC('256k', 2, 44100))], 'b.mkv').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-i', 'a.mp4',
               '-map', '0:v:0', '-c:v', 'mpeg', '-b:v', '3000k', '-aspect', '16:9', '-r', '23.97',
               '-map', '0:a:0', '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-ar', '44100',
               'b.mkv']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_convert_to_480p(self, mock_subprocess):
        vos = VideoOutstream('a.mp4').scale(height=480)
        MediaConverter([VideoTrack(vos, codecs.MPEG2('3000k', '16:9', '23.97')),
                        AudioTrack('a.mp4', codecs.AAC('256k', 2, 44100))], 'b.mkv').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-i', 'a.mp4', '-filter_complex', '[0:v:0]scale=-2:480[vout0]',
               '-map', '[vout0]', '-c:v', 'mpeg', '-b:v', '3000k', '-aspect', '16:9', '-r', '23.97',
               '-map', '0:a:0', '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-ar', '44100',
               'b.mkv']
        mock_subprocess.assert_called_with(cmd)
