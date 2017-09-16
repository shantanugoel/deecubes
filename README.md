# deecubes (Damn Simple Static url Shortener)

The name comes from the short form DSSS of Damn Simple Static url Shortener (so, a D and a cube of S's. Idiotic, I know :P). This program allows to maintain a website of short urls, akin to bit.ly/tinyurl etc, that can redirect to longer urls so one has to remember/give shorter ones. The main point of this project is to allow this to be done via a static website instead of a database based solution.

There are several benefits of a static website like they are much cheaper (Free to host on github/gitlab etc), easy to migrate to any host in minutes (if not seconds), etc. On top of this, the project strives to make this process as simple as possible to use.

## Input

Long url that you want to shorten

A mnemonic/shorturl you want to assign to it (Optional. If not given, one is generated automatically)

## Output

Static website of shorturls redirecting to your long urls

One can also go to shorturl/preview.html to see the long url it points to without getting redirected.

# Demo Website:
https://shgl.in/ uses this project. Repository for reference: https://shgl.in/deecubesdemo

# Installation

It's recommended to install deecubes from pypi using pip

```
pip install deecubes
```

# Deployment methods

You can use/deploy your own shorturl websites using deecubes in various ways given below and more:

- Host website on github/gitlab etc. Run deecubes cli commands (given in next section) locally to generate shorturls in a git repository. Commit and upload.

- Host website on github/gitlab etc. Create a 'source' branch in the website repository. Add a link to input directory from PC or directly through web interface and use a CI job (like Travis/CircleCI/Pipeline etc) to automatically generate shorturls using "sync" commands. https://shgl.in/ uses this method.

- Create your own automation to host the output directory on any host (through APIs or mounted directories etc)

# CLI Usage

```
usage: deecubes [-h] [-v] [-l LOGLEVEL]
                [-a SHORTURL URL | -g URL | -d SHORTURL | -s] -r RAW_DATA_PATH
                -o OUTPUT_PATH

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l LOGLEVEL, --log LOGLEVEL
                        Set log level. 0=> Warning, 1=>Info, 2=>Debug
  -a SHORTURL URL, --add SHORTURL URL
                        Add given shorturl for given url
  -g URL, --generate URL
                        Generate shorturl for given url
  -d SHORTURL, --delete SHORTURL
                        Delete given shorturl
  -s, --sync            Sync raw data storage and html output

required arguments:
  -r RAW_DATA_PATH, --raw-data-path RAW_DATA_PATH
                        Raw data storage path
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        HTML output path

```

Notes:

- Raw Path: A directory where deecubes stores raw information about urls. This can be empty directory if you are using add/generate commands for urls. Otherwise, you can add a .txt file here with the content being a long url. Then when, sync command is used, deecubes will add corresponding shorturl html files in output directory using the filename as the shorturl.

- Output Path: Path where the static website is generated. This directory should be used for deployment.

- Raw path and output path are mandatory to specify for all commands

## Examples

Add a specific shorturl for a long url

```
deecubes -r ./raw -o ./public -a github https://github.com/shantanugoel/
```

Add a long url and deecubes will generate a shorturl on its own

```
deecubes -r ./raw -o ./public -g https://github.com/shantanugoel/
```

Automatically generate shorturls in output dir for any .txt files that were manually added to raw directory

```
deecubes -r ./raw -o ./public --sync
```

# TODO

- Add collision handling

- Add google analytics

- Add configurable templates

- Suggestions?
