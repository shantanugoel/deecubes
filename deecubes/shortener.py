import os

class Shortener():

  raw_path = None
  output_path = None

  def __init__(self, raw_path, output_path):
    self.raw_path = raw_path
    self.output_path = output_path

  def _save(self, shorturl, url):
    raw_file_name = shorturl + '.txt'
    output_file_name = 'index.html'
    output_preview_file_name = 'preview.html'
    raw_file = os.path.join(self.raw_path, raw_file_name)
    output_dir = os.path.join(self.output_path, shorturl)
    os.mkdir(output_dir)

  def add(self, shorturl, url):
    _save(shorturl, url)

  def generate(self, url):
    pass

  def sync(self):
    pass
