from setuptools import setup, find_packages


MODULE_NAME = 'media_converter'
PACKAGE_DATA = list()

__version__ = version = '0.0.1'
__project__ = PROJECT = 'media_converter'
__author__ = AUTHOR = "Kiheon Choi <ecleya@smartstudy.co.kr>"


setup(
    name=PROJECT,
    version=version,
    packages=find_packages(),
    package_data={'': PACKAGE_DATA, },
    zip_safe=True,
    install_requires=['chardet',],
    author='Kiheon Choi',
    author_email='ecleya' '@' 'smartstudy.co.kr',
    maintainer='Kiheon Choi',
    maintainer_email='ecleya' '@' 'smartstudy.co.kr',
    url='https://github.com/smartstudy/media_converter',

    description='Media Converter',
)
