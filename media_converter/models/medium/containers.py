class _ContainerBase:
    @property
    def extention(self):
        raise NotImplemented


class _M4V(_ContainerBase):
    @property
    def extension(self):
        return '.m4v'


class _MP4(_ContainerBase):
    @property
    def extension(self):
        return '.mp4'


class _Mpeg(_ContainerBase):
    @property
    def extension(self):
        return '.mpg'


class _Matroska(_ContainerBase):
    @property
    def extension(self):
        return '.mkv'


class _Movie(_ContainerBase):
    @property
    def extension(self):
        return '.mov'


class _FlashVideo(_ContainerBase):
    @property
    def extension(self):
        return '.flv'


class Container:
    M4V = _M4V()
    MPEG = _Mpeg()
    MATROSKA = _Matroska()
    MP4 = _MP4()
    MOVIE = _Movie()
    FLASH_VIDEO = _FlashVideo()
