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

# Character or word level?
# char = True
char = False

class Prep:
    def __init__(self):
        ### HELPER FUNCTIONS ###
        self.pprint = lambda y: [print(x) for x in y]
        self.get_rel = lambda x: x.split('\t')[7]
        self.get_head = lambda x: x.split('\t')[6]
        self.get_dep = lambda x: x.split('\t')[0]
        self.get_deps = lambda x, y: [z for z in y if self.get_head(z) == self.get_dep(x)]
        self.tree2str = lambda tree: '{0}\n'.format(str(tree).replace(
            '\\n', '').replace(
            "'", "").replace(
            '\\t', ' ').replace(
            "_,", '_').replace(
            "[", '( ').replace(
            "]", " )").replace(
            "),", ')').strip())
            #.replace(
            # '_', '').replace(
            # "  ", ' ').replace(
            # "   ", ' ')

    def sep(self, lines):
        sents = []
        sent = []
        for l in lines:
            if l != '\n':
                sent.append(l)
            else:
                sents.append(sent)
                sent = []
        # double check that we're getting everything
        # if sent != []:
        #     sents.append(sent)
        return sents

    def split_stuff(self, sents):
        newsents = []
        for line in sents:
            line = line.split('\t')
            if len(line) > 1:
                # grammar
                line[5] = line[5].replace('|', ' ')
                # char level words
                if char:
                    line[1] = ' '.join(line[1])
                # pdb.set_trace()
            newsents.append('\t'.join(line))
        return newsents

    def tree_it(self, root, sent, feats):
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
                d = self.conv_to_feats(d, feats)
                root.append([d])
                pdb.set_trace()
            return root

    def conv_to_feats(self, line, feats):
        line = line.split('\t')
        pdb.set_trace()

    def find_root(self, sent):
        root = [x for x in sent if self.get_rel(x) == 'root']
        assert(len(root) == 1)
        sent.pop(sent.index(root[0]))
        return root, sent

    def build_hier(self, sent, feats):
        root, sent = self.find_root(sent)
        tree = self.tree_it(root, sent, feats)
        return tree

    def load_file(self, _file):
        data = open(_file, 'r').readlines()
        return data

    def build_feats(self, data):
        allFeats = set()
        for line in data:
            line = line.split('\t')
            if len(line) > 1:
                feats = [line[3], line[4], line[7]]
            for f in feats:
                allFeats.add(f)
        return allFeats


    def main(self):
        data = self.load_file(args.input)
        data = self.split_stuff(data)
        self.feats = self.build_feats(data)
        sents = self.sep(data)
        done = 0
        of = open(args.output, 'w')
        for s in sents:
            if s != []:
                tree = self.build_hier(s, self.feats)
                done += 1
                tree = self.tree2str(tree)
                # if tree[-2:] == '\n\n':
                pdb.set_trace()
                of.write(self.tree2str(tree))
        print("Processed", done, "sentences")

if __name__ == '__main__':
    p = Prep()
    p.main()
