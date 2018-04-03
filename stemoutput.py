#!/usr/bin/env python3

import sys
import argparse
import pdb
from nltk import word_tokenize
from nltk.stem import SnowballStemmer


# stemmer = PorterStemmer()
stemmer = SnowballStemmer("english")

print("Sample usage: python3 stemoutput.py -i dev-out.txt -o dev-stemmed.txt")
parser = argparse.ArgumentParser()
# parser.add_argument('-f', '--folds_dir', help="folds directory (e.g. folds/gold")
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-i', '--input', help='Input file name', required=True)
requiredNamed.add_argument('-o', '--output', help='Output file name', required=True)
args = parser.parse_args()

char = False

class Stem:
    def __init__(self):
        pass

    def characterize(self, line):
        line = '@'.join(line)
        return ' '.join(line)

    def main(self, infile, outfile):
        data = open(infile, 'r').readlines()
        of = open(outfile, 'w')
        done = 0
        for line in data:
            line = line.strip()
            line = word_tokenize(line)
            line = [stemmer.stem(x) for x in line]
            if char:
                of.write(self.characterize(line) + '\n')
            else:
                of.write(' '.join(line) + '\n')
            done += 1
        print("Processed", done, "sentences")


if __name__ == '__main__':
    s = Stem()
    s.main(args.input, args.output)