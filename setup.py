# https://coderwall.com/p/qawuyq
# Thanks James.

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''
    print 'warning: pandoc or pypandoc does not seem to be installed; using empty long_description'

import os
requirements_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'requirements.txt')
with open(requirements_file, 'r') as f:
    install_requires = [x.strip() for x in f.readlines()]

from setuptools import setup

setup(
    name='baiji-serialization',
    version=__import__('baiji.serialization').__version__,
    author='Body Labs',
    author_email='alex@bodylabs.com, paul.melnikow@bodylabs.com',
    description='Read and write common file formats to Amazon S3 and local files',
    long_description=long_description,
    url='https://github.com/bodylabs/baiji-serialization',
    license='MIT',
    packages=[
        'baiji',
        'baiji/serialization',
    ],
    install_requires=install_requires,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
