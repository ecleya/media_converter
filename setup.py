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

requirements = [
    'chardet',
    'pyfileinfo'
]

setup(
    name='media_converter',
    version=version(),
    author='Kiheon Choi',
    author_email='ecleya' '@' 'smartstudy.co.kr',
    maintainer='DevOps Team, SMARTSTUDY',
    maintainer_email='d9@smartstudy.co.kr',
    url='https://github.com/smartstudy/media_converter',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    setup_requires=[
        'pytest-runner'
    ],
    description='Media Converter',
)
