import argparse
import logging

from deecubes.constants import VERSION

def main():
  parser = argparse.ArgumentParser(prog='deecubes')
  parser.add_argument('-v', '--version', action='version',
                      version='%(prog)s version' + VERSION)
  parser.add_argument('-l', '--log', type=int, action='store',
                      help='Set log level. 0=> Warning, 1=>Info, 2=>Debug',
                      default=0)

  action = parser.add_mutually_exclusive_group()
  action.add_argument('-a', '--add', action='store',
                      help='Generate shorturl for given link')
  action.add_argument('-d', '--delete', action='store',
                      help='Delete given shorturl')
  action.add_argument('-s', '--sync', action='store_true', default=False,
                      help='Sync raw data storage and html output')

  req_args = parser.add_argument_group('required arguments')
  req_args.add_argument('-r', '--raw-data-path', help='Raw data storage path')
  req_args.add_argument('-o', '--output-path', help='HTML output path')

  try:
    args = parser.parse_args()
  except:
    exit(1)

  if args.log >= 2:
    log_level = logging.DEBUG
  elif args.log == 1:
    log_level = logging.INFO
  else:
    log_level = logging.WARNING
  logging.basicConfig(level=log_level,
                      format='%(asctime)s: %(filename)s - %(message)s')


if __name__ == "__main__":
  main()
