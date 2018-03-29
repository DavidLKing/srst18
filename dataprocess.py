#!/usr/bin/env python3

# from __future__ import print_function
import sys
import argparse
import pdb
# import cPickle as pkl

print("Sample usage: python3 datapreprocess.py -i file.conll")
parser = argparse.ArgumentParser()
# parser.add_argument('-f', '--folds_dir', help="folds directory (e.g. folds/gold")
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-i', '--input', help='Input file name', required=True)
args = parser.parse_args()

class template:
    def __init__(self):
        ### HELPER FUNCTIONS ###
        self.pprint = lambda y: [print(x) for x in y]
        self.get_rel = lambda x: x.split('\t')[7]
        self.get_head = lambda x: x.split('\t')[6]
        self.get_dep = lambda x: x.split('\t')[0]

    def sep(self, lines):
        sents = []
        sent = []
        for l in lines:
            if l != '\n':
                sent.append(l)
            else:
                sents.append(sent)
                sent = []
        if sent != []:
            sents.append(sent)
        return sents

    def find_root(self, sent):
        pass

    def build_hier(self, sent):
        pdb.set_trace()

    def load_file(self, _file):
        data = open(_file, 'r').readlines()
        sents = self.sep(data)
        for s in sents:
            self.build_hier(s)

    def main(self):
        self.load_file(args.input)

if __name__ == '__main__':
    t = template()
    t.main()
