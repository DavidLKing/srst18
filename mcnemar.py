#!/usr/bin/env python3

import sys
import argparse
import logging
import math
import os
import rpy2.robjects as ro
import pdb

class McNemar:
    def __init__(self):
        print("Sample usage: ./mcnemar.py gold out1 out2")

    def main(self):
        assert(len(sys.argv) == 4)
        golds = open(sys.argv[1], 'r').readlines()
        sys1 = open(sys.argv[2], 'r').readlines()
        sys2 = open(sys.argv[3], 'r').readlines()
        golds = [ line.split('\t')[2].strip() for line in golds ]
        sys1 = [ line.strip() for line in sys1 ]
        sys2 = [ line.strip() for line in sys2 ]
        bothright = 0
        bothwrong = 0
        oneright = 0
        tworight = 0
        for g, one, two in zip(golds, sys1, sys2):
            if g == one and g == two:
                bothright += 1
            elif g == one and g != two:
                oneright += 1
            elif g != one and g == two:
                tworight += 1
            elif g != one and g != two:
                bothwrong += 1
            else:
                raise
        """
        r stuff:
            x = matrix(c(1,2,3,4), 2, 2)
            mcnemar.test(x)
        """
        rstring = "mcnemar.test(matrix(c("
        rstring += str(bothright)
        rstring += ", "
        rstring += str(oneright)
        rstring += ", "
        rstring += str(tworight)
        rstring += ", "
        rstring += str(bothwrong)
        rstring += "), 2, 2))"
        print(ro.r(rstring))
        # test = ro.r(rstring)
        # pdb.set_trace()


if __name__ == '__main__':
    n = McNemar()
    n.main()
