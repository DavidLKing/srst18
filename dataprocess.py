#!/usr/bin/env python3

# from __future__ import print_function
import sys
import argparse
import pdb
import pprint

pp = pprint.PrettyPrinter(indent=4)
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
        self.get_deps = lambda x, y: [z for z in y if self.get_head(z) == self.get_dep(x)]

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

    def ptree(self, tree):
        start = ''
        for dep in tree:
            if type(dep[0]) == str:
                print(dep[0])

    def tree_it(self, root, sent):
        head = root[0]
        if self.get_deps(head, sent) == []:
            return head
        else:
            deps = self.get_deps(head, sent)
            for d in deps:
                sent.pop(sent.index(d))
            for d in deps:
                d = [d]
                d = self.tree_it(d, sent)
                root.append(d)
            return root

    def find_root(self, sent):
        root = [x for x in sent if self.get_rel(x) == 'root']
        assert(len(root) == 1)
        sent.pop(sent.index(root[0]))
        return root, sent

    def build_hier(self, sent):
        root, sent = self.find_root(sent)
        tree = self.tree_it(root, sent)
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
