import os
import logging
import glob
from binascii import crc32

from deecubes.utils import base64_encode


REDIR_TEMPLATE_PRE = '<html><head><meta http-equiv="refresh" content="0;URL=\''
REDIR_TEMPLATE_POST = '\'" /></head></html>'


class Shortener():

  raw_path = None
  output_path = None

  def __init__(self, raw_path, output_path):
    self.raw_path = raw_path
    self.output_path = output_path

  def _save_raw(self, shorturl, url):
    raw_file_name = shorturl + '.txt'
    # TODO: Handle conflicts while maintaining determinism
    raw_file = os.path.join(self.raw_path, raw_file_name)
    logging.debug('Saving raw file %s' % (raw_file))
    with open(raw_file, 'w') as f:
      f.write(url)

  def _save_output(self, shorturl, url):
    output_dir = os.path.join(self.output_path, shorturl)
    output_file = os.path.join(output_dir, 'index.html')
    preview_file = os.path.join(output_dir, 'preview.html')
    os.mkdir(output_dir)

    logging.debug('Saving output file %s' % (output_file))
    with open(output_file, 'w') as f:
      f.write(REDIR_TEMPLATE_PRE + url + REDIR_TEMPLATE_POST)

      logging.debug('Saving Preview file %s' % (preview_file))
    with open(preview_file, 'w') as f:
      f.write(url)

  def _encode(self, url):
    # Calculate CRC32 and convert to base64
    # Add 16 LSB of simple checksum base64 for additional collision avoidance
    return base64_encode(crc32(bytes(url, 'utf-8'))) + base64_encode(sum(bytearray(url, 'utf-8')))

  def add(self, shorturl, url):
    logging.debug('Adding shorturl %s for %s' % (shorturl, url))
    self._save_raw(shorturl, url)
    self._save_output(shorturl, url)

  def generate(self, url):
    shorturl = self._encode(url)
    logging.debug('Generated shorturl %s for %s' % (shorturl, url))
    self.add(shorturl, url)

  def sync(self):
    # TODO: Use asyncio to make this faster
    search_pattern = os.path.join(self.raw_path, '*.txt')
    raw_files = glob.glob(search_pattern)
    for file in raw_files:
      shorturl = os.path.splitext(os.path.basename(file))[0]
      if not os.path.isdir(os.path.join(self.output_path, shorturl)):
        with open(file, 'r') as f:
          url = f.readline()
        self._save_output(shorturl, url)
