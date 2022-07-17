from setuptools import setup

setup(
    name='tendermint-chunked-genesis-download',
    version='1.0',
    description='Package for easily downloading a chunked Tendermint genesis from a RCP enabled node.',
    url='https://github.com/dclaudiud/tendermint-chunked-genesis-download',
    author='dclaudiud',
    author_email='dclaudiud@proton.me',
    packages=['tendermint-chunked-genesis-download'],
    install_requires=[
        'requests==2.28.1',
        'click==8.1.3',
        'setuptools==57.0.0'
    ],
    entry_points={
        'console_scripts': ['tendermint-chunked-genesis-download=src.tendermint-chunked-genesis-download.cli:main']
    },
    license='MIT'
)
