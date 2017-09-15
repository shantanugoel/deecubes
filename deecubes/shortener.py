import os


REDIR_TEMPLATE_PRE = '<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="refresh" content="0;URL=\''
REDIR_TEMPLATE_POST='\'" /></head></html>'


class Shortener():

  raw_path = None
  output_path = None

  def __init__(self, raw_path, output_path):
    self.raw_path = raw_path
    self.output_path = output_path

  def _save(self, shorturl, url):
    raw_file_name = shorturl + '.txt'
    #TODO: Handle conflicts while maintaining determinism
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

  def add(self, shorturl, url):
    self._save(shorturl, url)

  def generate(self, url):
    pass

  def sync(self):
    pass
