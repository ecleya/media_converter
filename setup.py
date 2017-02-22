import os.path
import warnings

from setuptools import setup, find_packages


def version():
    try:
        root = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(root, '.version')) as f:
            return f.read().strip()
    except IOError:
        warnings.warn("Couldn't found .version file", RuntimeWarning)
        return ''


requirements = [
    'chardet',
    'pyfileinfo',
]


setup(
    name='media_converter',
    version=version(),
    packages=find_packages(),
    package_data={},
    zip_safe=True,
    install_requires=requirements,
    author='Kiheon Choi',
    author_email='ecleya' '@' 'smartstudy.co.kr',
    maintainer='Kiheon Choi',
    maintainer_email='ecleya' '@' 'smartstudy.co.kr',
    url='https://github.com/smartstudy/media_converter',

    description='Media Converter',
)
