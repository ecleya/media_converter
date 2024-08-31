from setuptools import setup, find_packages


REQUIREMENTS = [
    'chardet',
    'future',
]

EXTRAS_REQUIRE = {
    'test': [
        'pytest',
        'pytest-cov',
        'flake8',
        'unittest-xml-reporting',
        'mock',
    ]
}

setup(
    name='media_converter',
    version='1.2.0',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    author='Kiheon Choi',
    author_email='ecleya' '@' 'gmail.com',
    maintainer='Kiheon Choi',
    maintainer_email='ecleya@gmail.com',
    url='https://github.com/ecleya/media_converter',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    extras_require=EXTRAS_REQUIRE,
    setup_requires=[
        'pytest-runner'
    ],
    description='Media Converter',
)
