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
requiredNamed.add_argument('-o', '--output', help='Output file name', required=True)
args = parser.parse_args()

class Prep:
    def __init__(self):
        ### HELPER FUNCTIONS ###
        self.pprint = lambda y: [print(x) for x in y]
        self.get_rel = lambda x: x.split('\t')[7]
        self.get_head = lambda x: x.split('\t')[6]
        self.get_dep = lambda x: x.split('\t')[0]
        self.get_deps = lambda x, y: [z for z in y if self.get_head(z) == self.get_dep(x)]
        self.tree2str = lambda tree: str(tree).replace('\\n', '').replace("'", "").replace('\\t', ' ').replace('_,', '_').replace("[", '( ').replace("]", " )") + '\n'

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

    def split_stuff(self, sents):
        newsents = []
        for line in sents:
            line = line.split('\t')
            if len(line) > 1:
                # grammar
                line[5] = line[5].replace('|', '')
                # char level words
                line[1] = ' '.join(line[1])
            newsents.append('\t'.join(line))
        return newsents

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
                root.append([d])
            return root

    def find_root(self, sent):
        root = [x for x in sent if self.get_rel(x) == 'root']
        assert(len(root) == 1)
        sent.pop(sent.index(root[0]))
        return root, sent

    def build_hier(self, sent):
        root, sent = self.find_root(sent)
        tree = self.tree_it(root, sent)
        return tree

    def load_file(self, _file):
        data = open(_file, 'r').readlines()
        return data

    def main(self):
        data = self.load_file(args.input)
        data = self.split_stuff(data)
        sents = self.sep(data)
        done = 0
        of = open(args.output, 'w')
        for s in sents:
            if s != []:
                tree = self.build_hier(s)
                done += 1
                of.write(self.tree2str(tree))
        print("Processed", done, "sentences")

if __name__ == '__main__':
    p = Prep()
    p.main()
