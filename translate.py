from __future__ import absolute_import
import argparse
from io import open

parser = argparse.ArgumentParser()
parser.add_argument(u"file", help=u"file to translate data")
args = parser.parse_args()

filename = args.file

f = open(filename)
seed = int(f.readline())
random.seed(seed)

f.close()
