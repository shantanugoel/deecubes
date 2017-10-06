import os
import shutil
import logging
import glob
from binascii import crc32
from urllib.parse import urljoin

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
    # Handle collision
    tie_breaker_char = ''
    tie_breaker_counter = 0
    while True:
      shorturl = shorturl + tie_breaker_char
      raw_file_name = shorturl + '.txt'
      raw_file = os.path.join(self.raw_path, raw_file_name)
      if os.path.exists(raw_file):
        with open(raw_file, 'r') as f:
          url_in_file = f.readline()
        if url_in_file == url:
          logging.info("Existing url. Returning existing shorturl")
          return shorturl, False
        else:
          tie_breaker_char = base64_encode(tie_breaker_counter)
          tie_breaker_counter += 1
      else:
        # No collision so break out of the loop
        break

    logging.debug('Saving raw file %s' % (raw_file))
    try:
      with open(raw_file, 'w') as f:
        f.write(url)
      return shorturl, True
    except OSError as e:
      logging.error('Received error while saving raw %s: %s' % (shorturl, e))
      return None, False

  def _clean_dir(dir):
    try:
      shutil.rmtree(dir)
    except OSError as e:
      logging.error("Could not clean up %s because: %s" % (dir, e))

  def _save_output(self, shorturl, url):
    output_dir = os.path.join(self.output_path, shorturl)
    output_file = os.path.join(output_dir, 'index.html')
    preview_file = os.path.join(output_dir, 'preview.html')
    try:
      os.mkdir(output_dir)
    except OSError as e:
      logging.error('Received error while creating %s: %s' % (output_dir, e))
      return None

    logging.debug('Saving output file %s' % (output_file))
    try:
      with open(output_file, 'w') as f:
        f.write(REDIR_TEMPLATE_PRE + url + REDIR_TEMPLATE_POST)
    except OSError as e:
      logging.error('Received error while saving output %s: %s' % (shorturl, e))
      self._clean_dir(output_dir)
      return None

    logging.debug('Saving Preview file %s' % (preview_file))
    try:
      with open(preview_file, 'w') as f:
        f.write(url)
    except OSError as e:
      logging.error('Received error while saving preview %s: %s' % (shorturl, e))
      self._clean_dir(output_dir)
      return None

    return output_dir

  def _encode(self, url):
    # Calculate CRC32 and convert to base64
    # Add 16 LSB of simple checksum base64 for additional collision avoidance
    return base64_encode(crc32(bytes(url, 'utf-8'))) + base64_encode(sum(bytearray(url, 'utf-8')))

  def _fix_url(self, url):
    # Fix missing scheme in most cases
    return urljoin('http://', url)

  def add(self, shorturl, url):
    url = self._fix_url(url)
    logging.debug('Adding shorturl %s for %s' % (shorturl, url))
    shorturl, raw_saved = self._save_raw(shorturl, url)
    if raw_saved:
      output_dir = self._save_output(shorturl, url)
      if output_dir:
        logging.debug("Added shorturl at %s " % output_dir)
        return shorturl
      else:
        return None
    return shorturl

  def generate(self, url):
    url = self._fix_url(url)
    shorturl = self._encode(url)
    logging.debug('Generated shorturl %s for %s' % (shorturl, url))
    return self.add(shorturl, url)

  def delete(self, shorturl):
    try:
      shutil.rmtree(os.path.join(self.output_path, shorturl))
      try:
        delete_file = os.path.join(self.raw_path, shorturl + '.txt')
        os.unlink(delete_file)
        logging.debug("Deleted file %s" % delete_file)
        return shorturl
      except OSError as e:
        logging.error('Received error while deleting raw %s: %s' % (shorturl, e))
        return None
    except OSError as e:
      logging.error('Received error while deleting output %s: %s' % (shorturl, e))
      return None

  def sync(self):
    search_pattern = os.path.join(self.raw_path, '*.txt')
    raw_files = glob.glob(search_pattern)
    for file in raw_files:
      shorturl = os.path.splitext(os.path.basename(file))[0]
      if not os.path.isdir(os.path.join(self.output_path, shorturl)):
        try:
          with open(file, 'r') as f:
            url = f.readline()
          self._save_output(shorturl, url)
        except OSError as e:
          logging.error('Error during syncing shorturl %s: %s' %(shorturl, e))
    else:
        logging.warning('No files found for syncing')
        return None
