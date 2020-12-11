from setuptools import setup, find_packages

setup(
    name='PartsOfSpeech',
    extras_reqiure=dict(tests=['pytest']),
    packages=find_packages(where='src'),
    package_dir={"": "src"},
)