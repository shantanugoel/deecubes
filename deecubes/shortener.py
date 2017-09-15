import os
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

  def _save(self, shorturl, url):
    raw_file_name = shorturl + '.txt'
    # TODO: Handle conflicts while maintaining determinism
    raw_file = os.path.join(self.raw_path, raw_file_name)
    output_dir = os.path.join(self.output_path, shorturl)
    output_file = os.path.join(output_dir, 'index.html')
    preview_file = os.path.join(output_dir, 'preview.html')
    os.mkdir(output_dir)
    with open(raw_file, 'w') as f:
      f.write(url)
    with open(output_file, 'w') as f:
      f.write(REDIR_TEMPLATE_PRE + url + REDIR_TEMPLATE_POST)
    with open(preview_file, 'w') as f:
      f.write(url)

  def _encode(self, url):
    # Calculate CRC32 and convert to base64
    # Add 16 LSB of simple checksum base64 for additional collision avoidance
    return base64_encode(crc32(bytes(url, 'utf-8'))) + base64_encode(sum(bytearray(url, 'utf-8')))

  def add(self, shorturl, url):
    self._save(shorturl, url)

  def generate(self, url):
    shorturl = self._encode(url)
    self.add(shorturl, url)

  def sync(self):
    pass
