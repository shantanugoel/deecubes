from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = '0.1.0'

setup(
  name='deecubes',
  version=version,
  install_requires=requirements,
  author='Shantanu Goel',
  author_email='shantanu@shantanugoel.com',
  packages=find_packages(),
  include_package_data=True,
  url='https://github.com/shantanugoel/deecubes/',
  license='MIT',
  description='deecubes (DSSS - Damn Simple Static url Shortener)',
  long_description=long_description,
  entry_points={
    'console_scripts': [
      'deecubes=deecubes.deecubes:main',
    ],
  },
  classifiers=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
  ],
  keywords='url shorturl url-shortener'
)
