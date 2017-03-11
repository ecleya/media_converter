from unittest import TestCase, mock
from media_converter import MediaConverter, codecs
from media_converter.tracks import VideoTrack, AudioTrack, SubtitleTrack
from media_converter.streams import VideoOutstream, AudioInstream


class TestMediaConverter(TestCase):
    @mock.patch('subprocess.call')
    def test_simple_convert(self, mock_subprocess):
        MediaConverter('a.mp4', 'b.mkv').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mp4',
               '-map', '0:v:0', '-c:v', 'h264', '-crf', '23', '-pix_fmt', 'yuv420p',
               '-profile:v', 'high', '-level', '3.1',
               '-map', '0:a:0', '-c:a', 'aac', '-b:a', '192k', '-ac', '2', '-ar', '44100',
               '-threads', '0', 'b.mkv']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_audio_convert(self, mock_subprocess):
        MediaConverter(AudioTrack('a.wav', codecs.AAC('256k', 2, 44100)), 'a.m4a').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.wav',
               '-map', '0:a:0', '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-ar', '44100',
               '-threads', '0', 'a.m4a']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_video_convert(self, mock_subprocess):
        MediaConverter([VideoTrack('a.mp4', codecs.MPEG2('3000k', '16:9', '23.97')),
                        AudioTrack('a.mp4', codecs.MP2('256k', 2, 44100))], 'b.mkv').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mp4',
               '-map', '0:v:0', '-c:v', 'mpeg2video', '-b:v', '3000k', '-aspect', '16:9', '-r', '23.97',
               '-map', '0:a:0', '-c:a', 'mp2', '-b:a', '256k', '-ac', '2', '-ar', '44100',
               '-threads', '0', 'b.mkv']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_convert_to_480p(self, mock_subprocess):
        vos = VideoOutstream('a.mp4').scale(height=480)
        MediaConverter([VideoTrack(vos, codecs.MPEG2('3000k', '16:9', '23.97')),
                        AudioTrack('a.mp4', codecs.AAC('256k', 2, 44100))], 'b.mkv').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mp4',
               '-filter_complex', '[0:v:0]scale=-2:480[vout0]',
               '-map', '[vout0]', '-c:v', 'mpeg2video', '-b:v', '3000k', '-aspect', '16:9', '-r', '23.97',
               '-map', '0:a:0', '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-ar', '44100',
               '-threads', '0', 'b.mkv']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_h265_with_ac3(self, mock_subprocess):
        MediaConverter([VideoTrack('a.mkv', codecs.H265(constant_rate_factor=18, preset='slow')),
                        AudioTrack('a.mkv', codecs.AC3('448k', 6, 48000))], 'b.mp4').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mkv',
               '-map', '0:v:0', '-c:v', 'libx265', '-preset', 'slow', '-x265-params', 'crf=18',
               '-map', '0:a:0', '-c:a', 'ac3', '-b:a', '448k', '-ac', '6', '-ar', '48000',
               '-threads', '0', 'b.mp4']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_silent_audio_for_10_secs(self, mock_subprocess):
        MediaConverter([AudioTrack(None, codecs.AAC('256k', 2, 48000))], 'b.m4a').convert(duration=10)

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-ar', '48000', '-ac', '1', '-f', 's16le', '-i', '/dev/zero',
               '-map', '0:a:0', '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-ar', '48000', '-t', '10',
               '-threads', '0', 'b.m4a']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_blank_video_with_audio(self, mock_subprocess):
        MediaConverter([VideoTrack(None, codecs.H264()),
                        AudioTrack('a.mp3', codecs.AAC())], 'b.mp4').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-s', '640x360', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-r', '30', '-i', '/dev/zero',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mp3',
               '-map', '0:v:0', '-c:v', 'h264', '-crf', '23', '-pix_fmt', 'yuv420p',
               '-profile:v', 'high', '-level', '3.1',
               '-map', '1:a:0', '-c:a', 'aac', '-b:a', '192k', '-ac', '2', '-ar', '44100',
               '-shortest',
               '-threads', '0', 'b.mp4']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    @mock.patch('media_converter.streams.instream.ImageInstream.is_valid')
    def test_image_video_with_audio(self, mock_valid, mock_subprocess):
        mock_valid.return_value = True
        MediaConverter([VideoTrack('a.png', codecs.H264()),
                        AudioTrack('a.mp3', codecs.AAC())], 'b.mp4').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-i', 'a.png',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mp3',
               '-map', '0:v:0', '-c:v', 'h264', '-crf', '23', '-pix_fmt', 'yuv420p',
               '-profile:v', 'high', '-level', '3.1',
               '-map', '1:a:0', '-c:a', 'aac', '-b:a', '192k', '-ac', '2', '-ar', '44100',
               '-threads', '0', 'b.mp4']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_copy(self, mock_subprocess):
        MediaConverter([VideoTrack('a.mkv', codecs.Copy()),
                        AudioTrack('a.mkv', codecs.Copy()),
                        SubtitleTrack('a.mkv', codecs.Copy())], 'b.mkv').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mkv',
               '-map', '0:v:0', '-c:v', 'copy',
               '-map', '0:a:0', '-c:a', 'copy',
               '-map', '0:s:0', '-c:s', 'copy',
               '-threads', '0', 'b.mkv']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_delay_audio_for_5sec(self, mock_subprocess):
        delayed_instream = AudioInstream('a.mkv', start_at=5)
        MediaConverter([VideoTrack('a.mkv', codecs.H264()),
                        AudioTrack(delayed_instream, codecs.AC3('448k', 6, 48000))], 'b.mp4').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mkv',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-ss', '5', '-i', 'a.mkv',
               '-map', '0:v:0', '-c:v', 'h264', '-crf', '23', '-pix_fmt', 'yuv420p',
               '-profile:v', 'high', '-level', '3.1',
               '-map', '1:a:0', '-c:a', 'ac3', '-b:a', '448k', '-ac', '6', '-ar', '48000',
               '-threads', '0', 'b.mp4']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    def test_multiple_video_filters(self, mock_subprocess):
        vos = VideoOutstream('a.mp4').deinterlace().scale(width=1920)
        MediaConverter([VideoTrack(vos, codecs.H264()),
                        AudioTrack('a.mp4', codecs.AC3('448k', 6, 48000))], 'b.mp4').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mp4',
               '-filter_complex', '[0:v:0]yadif[vout0];[vout0]scale=1920:-2[vout1]',
               '-map', '[vout1]', '-c:v', 'h264', '-crf', '23', '-pix_fmt', 'yuv420p',
               '-profile:v', 'high', '-level', '3.1',
               '-map', '0:a:0', '-c:a', 'ac3', '-b:a', '448k', '-ac', '6', '-ar', '48000',
               '-threads', '0', 'b.mp4']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    @mock.patch('media_converter.streams.instream.ImageInstream.is_valid')
    def test_overlay_filter(self, mock_valid, mock_subprocess):
        mock_valid.side_effect = lambda x: x == 'a.png'

        vos = VideoOutstream('a.mp4').overlay('a.png')
        MediaConverter([VideoTrack(vos, codecs.H264()),
                        AudioTrack('a.mp4', codecs.AC3('448k', 6, 48000))], 'b.mp4').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mp4',
               '-i', 'a.png',
               '-filter_complex', '[0:v:0][1:v:0]overlay=0:0[vout0]',
               '-map', '[vout0]', '-c:v', 'h264', '-crf', '23', '-pix_fmt', 'yuv420p',
               '-profile:v', 'high', '-level', '3.1',
               '-map', '0:a:0', '-c:a', 'ac3', '-b:a', '448k', '-ac', '6', '-ar', '48000',
               '-threads', '0', 'b.mp4']
        mock_subprocess.assert_called_with(cmd)

    @mock.patch('subprocess.call')
    @mock.patch('media_converter.streams.instream.ImageInstream.is_valid')
    def test_overlay_filter_with_xy_option(self, mock_valid, mock_subprocess):
        mock_valid.side_effect = lambda x: x == 'a.png'

        vos = VideoOutstream('a.mp4').overlay('a.png', 30, 70)
        MediaConverter([VideoTrack(vos, codecs.H264()),
                        AudioTrack('a.mp4', codecs.AC3('448k', 6, 48000))], 'b.mp4').convert()

        cmd = ['/usr/local/bin/ffmpeg', '-y',
               '-analyzeduration', '2147483647', '-probesize', '2147483647', '-i', 'a.mp4',
               '-i', 'a.png',
               '-filter_complex', '[0:v:0][1:v:0]overlay=30:70[vout0]',
               '-map', '[vout0]', '-c:v', 'h264', '-crf', '23', '-pix_fmt', 'yuv420p',
               '-profile:v', 'high', '-level', '3.1',
               '-map', '0:a:0', '-c:a', 'ac3', '-b:a', '448k', '-ac', '6', '-ar', '48000',
               '-threads', '0', 'b.mp4']
        mock_subprocess.assert_called_with(cmd)
