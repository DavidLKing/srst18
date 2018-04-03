#!/usr/bin/env python3

# from __future__ import print_function
import sys
import argparse
import pdb
import pprint
from nltk import word_tokenize
from nltk.stem.porter import *

pp = pprint.PrettyPrinter(indent=4)
# import cPickle as pkl

print("Sample usage: python3 datapreprocess.py -i file.conll")
parser = argparse.ArgumentParser()
# parser.add_argument('-f', '--folds_dir', help="folds directory (e.g. folds/gold")
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-i', '--input', help='Input file name', required=True)
requiredNamed.add_argument('-o', '--output', help='Output file name', required=True)
args = parser.parse_args()

# Character or word level?
# char = True
char = False

class Prep:
    def __init__(self):
        self.stemmer = PorterStemmer()
        ### HELPER FUNCTIONS ###
        # self.pprint = lambda y: [print(x) for x in y]
        # self.get_rel = lambda x: x.split('\t')[7]
        # self.get_head = lambda x: x.split('\t')[6]
        # self.get_dep = lambda x: x.split('\t')[0]
        # self.get_deps = lambda x, y: [z for z in y if self.get_head(z) == self.get_dep(x)]
        # self.tree2str = lambda tree: str(tree).replace('\\n', '').replace("'", "").replace('\\t', ' ').replace('_,', '_').replace("[", '( ').replace("]", " )").strip() + '\n'

    def main(self):
        data = open(args.input, 'r').readlines()
        outfile = open(args.output, 'w')
        done = 0
        for line in data:
            if line.startswith('# text'):
                line = line[8:]
                line = line.strip()
                line = word_tokenize(line)
                line = '@'.join(line)
                line = ' '.join(line)
                outfile.write(line + '\n')
                done += 1
        print("Processed", done, "sentences")

if __name__ == '__main__':
    p = Prep()
    p.main()
