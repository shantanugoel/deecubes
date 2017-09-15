import argparse
import logging
import os

from deecubes.constants import VERSION
from deecubes.shortener import Shortener


def is_dir(path):
  if not os.path.isdir(path):
    msg = "{0} is not a directory".format(path)
    raise argparse.ArgumentTypeError(msg)
  else:
    return path


def main():
  parser = argparse.ArgumentParser(prog='deecubes')
  parser.add_argument('-v', '--version', action='version',
                      version='%(prog)s version ' + VERSION)
  parser.add_argument('-l', '--log', metavar='LOGLEVEL', type=int, action='store',
                      help='Set log level. 0=> Warning, 1=>Info, 2=>Debug', default=0)

  action = parser.add_mutually_exclusive_group()
  action.add_argument('-a', '--add', nargs=2, metavar=('SHORTURL', 'URL'), action='store',
                      help='Add given shorturl for given url')
  action.add_argument('-g', '--generate', metavar='URL', action='store', help='Generate shorturl for given url')
  action.add_argument('-d', '--delete', metavar='SHORTURL', action='store', help='Delete given shorturl')
  action.add_argument('-s', '--sync', action='store_true', default=False, help='Sync raw data storage and html output')

  req_args = parser.add_argument_group('required arguments')
  req_args.add_argument('-r', '--raw-data-path', required=True, type=is_dir, help='Raw data storage path')
  req_args.add_argument('-o', '--output-path', required=True, type=is_dir, help='HTML output path')

  args = parser.parse_args()

  if args.log >= 2:
    log_level = logging.DEBUG
  elif args.log == 1:
    log_level = logging.INFO
  else:
    log_level = logging.WARNING
  logging.basicConfig(level=log_level, format='%(asctime)s: %(filename)s - %(message)s')

  shortener = Shortener(args.raw_data_path, args.output_path)
  if args.add:
    shortener.add(args.add[0], args.add[1])
  elif args.generate:
    shortener.generate(args.generate)
  elif args.sync:
    shortener.sync()
  elif args.delete:
    shortener.delete(args.delete)
  else:
    logging.error('No action specified')


if __name__ == "__main__":
  main()
