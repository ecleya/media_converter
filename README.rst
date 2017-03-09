MediaConverter
==============

MediaConverter is FFmpeg wrapper. FFmpeg is great, but it's really hard to use. MediaConverter's goal is use FFmpeg more easier way.

With MediaConverter, all you need is just focus about tracks. It will do the rest.

Installation
------------

    pip install media_converter

Examples
--------

..
>>> from media_converter import MediaConverter
>>> MediaConverter('src.mkv', 'dst.mp4').convert()

This will convert ``src.mkv`` to ``dst.mp4`` with default parameters for mp4.


..
>>> from media_converter import MediaConverter
>>> from media_converter.tracks import AudioTrack
>>> MediaConverter(AudioTrack('src.wav', codecs.AAC('192k', 2, 44100)), 'dst.m4a').convert()

This will convert PCM to AAC with 192k bitrates, 2 channels, 44100Hz. Of course simply ``MediaConverter('src.wav', dst.m4a').convert()`` will do the same.


..
>>> from media_converter import MediaConverter
>>> MediaConverter([AudioTrack(None, codecs.AAC('256k', 2, 48000))], 'dst.m4a').convert(duration=10)

This will generate silent audio for 10 seconds.


If you want to make audio with black screen or image, it will do the trick.

..
>>> from media_converter import MediaConverter
>>> MediaConverter([AudioTrack(None, codecs.AAC('256k', 2, 48000))], 'dst.m4a').convert(duration=10)
>>> MediaConverter([VideoTrack(None, codecs.H264()),
                    AudioTrack('a.mp3', codecs.AAC())], 'b.mp4').convert()

and more.

..
>>> from media_converter import MediaConverter, codecs
>>> from media_converter.tracks import VideoTrack, AudioTrack
>>>
>>> MediaConverter([VideoTrack('src.mp4', codecs.MPEG2('3000k', '16:9', '23.97')),
...                 AudioTrack('src.mp4', codecs.AAC('256k', 2, 44100))],
...                 'dst.mkv').convert()


..
>>> from media_converter import MediaConverter, codecs
>>> from media_converter.tracks import VideoTrack, AudioTrack
>>> from media_converter.streams import VideoOutstream
>>>
>>> vos = VideoOutstream('src.mp4').scale(height=480)
>>> MediaConverter([VideoTrack(vos, codecs.MPEG2('3000k', '16:9', '23.97')),
...                 AudioTrack('src.mp4', codecs.AAC('256k', 2, 44100))], 'dst.mkv').convert()


..
>>> from media_converter import MediaConverter, codecs
>>> from media_converter.tracks import VideoTrack, AudioTrack
>>>
>>> MediaConverter([VideoTrack('src1.mp4', codecs.Copy()),
...                 AudioTrack('src2.mp4', codecs.Copy())],
...                 'dst.mkv').convert()
