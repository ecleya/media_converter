MediaConverter
==============

MediaConverter is FFmpeg wrapper. FFmpeg is great, but it's really hard to use. MediaConverter's goal is use FFmpeg more easier way.

With MediaConverter, all you need is just focus about tracks. It will do the rest.

Installation
------------

    pip install media_converter

Examples
--------

.. code:: python
   >>> from media_converter import MediaConverter
   >>> MediaConverter('src.mkv', 'dst.mp4').convert()

This will convert ``src.mkv`` to ``dst.mp4`` with default parameters for mp4.


.. code::python
   >>> from media_converter import MediaConverter
   >>> from media_converter.tracks import AudioTrack
   >>> MediaConverter(AudioTrack('src.wav', codecs.AAC('192k', 2, 44100)), 'dst.m4a').convert()

This will convert PCM to AAC with 192k bitrates, 2 channels, 44100Hz. Of course simply ``MediaConverter('src.wav', dst.m4a').convert()`` will do the same.


.. code::python
   >>> from media_converter import MediaConverter, codecs
   >>> from media_converter.tracks import VideoTrack, AudioTrack
   >>>
   >>> MediaConverter([VideoTrack('src.mp4', codecs.MPEG2('3000k', '16:9', '23.97')),
   ...                 AudioTrack('src.mp4', codecs.AAC('256k', 2, 44100))],
   ...                 'dst.mkv').convert()


.. code::python
   >>> from media_converter import MediaConverter, codecs
   >>> from media_converter.tracks import VideoTrack, AudioTrack
   >>> from media_converter.streams import VideoOutstream
   >>>
   >>> vos = VideoOutstream('src.mp4').scale(height=480)
   >>> MediaConverter([VideoTrack(vos, codecs.MPEG2('3000k', '16:9', '23.97')),
   ...                 AudioTrack('src.mp4', codecs.AAC('256k', 2, 44100))], 'dst.mkv').convert()
