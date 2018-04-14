#!/usr/bin/env python3

import pdb
# from __future__ import division
from random import uniform

import score

# TODO build class and functions, this is for testing
# character level testing
# s = score.Score('./data/en-char')
# model = s.load_model('./models/model.en.char.pt')
# word level testing
s = score.Score('./data/en-word')
# s = score.Score('./data/en-char')
model = s.load_model('./models/model.en.word.pt')
# model = s.load_model('./models/model.en.char.pt')
lstmscore = lambda cand: s.score_sent(cand, model)
# formatting
def lstmify(sent):
    # characterize = lambda sent: ' '.join(' '.join(sent.hyp)[4:].replace(' ', '@').replace('</s>', '<eos>'))
    seq = sent.hyp
    # remove the <s>, that's already the LSTM's input
    seq = ' '.join(seq)[4:]
    seq = seq.replace('</s>', '<eos>')
    return seq

def characterize(sent):
    # characterize = lambda sent: ' '.join(' '.join(sent.hyp)[4:].replace(' ', '@').replace('</s>', '<eos>'))
    seq = sent.hyp
    # remove the <s>, that's already the LSTM's input
    seq = ' '.join(seq)[4:]
    seq = seq.replace(' ', '@')
    seq = ' '.join(seq)
    seq = seq.replace('</s>', '<eos>')
    pdb.set_trace()
    return seq

def unkify(sent, lang):
    newsent = []
    for word in sent.hyp:
        if word not in lang and word not in ['<s>', '</s>']:
            newsent.append('UNK')
        else:
            newsent.append(word)
    sent.hyp = newsent
    return sent

"""
Scores are negative since the LSTM outputs loss over a sequence (cross entropy or neg. log. likelihood).
We want sents w/ minimal loss (common sequences)
Once negative, the sorting and pull the max should be the same as pulling the min w/o changing 
the rest of the code
"""
charscore = lambda sent: -float(lstmscore(characterize(unkify(sent, s.data.dictionary.word2idx)))[0][0])
wordscore = lambda sent: -float(lstmscore(lstmify(unkify(sent, s.data.dictionary.word2idx)))[0][0])

# a simple 2-gram precision scorer
class Bleu2:
    # init bigrams from ref with start and end tags
    def __init__(self, ref):
        bounded_ref = ['<s>'] + ref + ['</s>']
        self.bigrams = [bi for bi in zip(bounded_ref,bounded_ref[1:])]
    # calc 2-gram precision wrt ref bigrams
    def score(self, hyp):
        hyp_bigrams = [bi for bi in zip(hyp,hyp[1:])]
        matches = len([bi for bi in hyp_bigrams if bi in self.bigrams])
        return matches / len(hyp_bigrams)
    # update 2-gram precision wrt previous score,
    # assuming one additional word
    def update_score(self, hyp, prev_score):
        num_hyp_bigrams = len(hyp) -1
        prev_hyp_bigrams = num_hyp_bigrams - 1
        prev_matches = prev_score * prev_hyp_bigrams
        new_bi = (hyp[-2],hyp[-1])
        matches = prev_matches + 1 if new_bi in self.bigrams else prev_matches
        return matches / num_hyp_bigrams

# a candidate consists of a word sequence, a permutation vector and a score;
# the permutation vector is a mapping from a list of input words to their
# positions in the hypothesized sequence, with zero (root in the inputs)
# mapping to zero (start symbol in hypothesis), and no mapping for the end symbol
class Candidate:
    # input length for permutation vector, including 0 -> 0
    # hypothesis initialized to ['<s>'], vector to all zeros, score to one
    def __init__(self, perm_len):
        self.hyp = ['<s>']
        self.perm = [0 for i in range(perm_len)]
        self.score = 1
    # string rep = hyp (score) [perm]
    def __repr__(self):
        return ' '.join(self.hyp) + ' (' + str(self.score) + ') ' + str(self.perm)
    # nb: shared linked lists would be more efficient
    def copy(self):
        retval = Candidate(len(self.perm))
        retval.hyp = self.hyp[:]
        for (i,idx) in enumerate(self.perm):
            retval.perm[i] = idx
        retval.score = self.score
        return retval
        
# returns a function from a candidate to an updated bleu2 score
def bleu2_cand_scorer(words):
    bleu2 = Bleu2(words)
    return lambda cand: bleu2.update_score(cand.hyp, cand.score)

# a beam gen instance uses beam search to generate permutations of the input words
# according to the given scoring function from candidates to scores;
# if epsilon is greater than zero, then a random number up to epsilon is added
# to the score of each candidate so that ties are randomly broken (if not more
# generally varying the search, depending on the size of epsilon);
# the beam size can be configured, and steps can be logged if desired
class BeamGen:
    # initialize beam with a single candidate that's just the start symbol,
    # and with the initial *ROOT* word pointing to the start symbol,
    # so that real words start with index 1
    def __init__(self, words, cand_scorer, beam_size=10, epsilon=0.01, log_steps=False):
        self.words = words
        if words[0] != '*ROOT*':
            self.words = ['*ROOT*'] + words
        self.cand_scorer = cand_scorer
        self.beam_size = beam_size
        self.beam = [Candidate(len(self.words))]
        self.epsilon = epsilon
        self.log_steps = log_steps
    # run beam search
    def search(self):
        # add random increment to sort key, if apropos
        if self.epsilon > 0:
            sort_key = lambda cand: -1 * (cand.score + uniform(0,self.epsilon))
        else:
            sort_key = lambda cand: -1 * cand.score
        # add sequence of words
        for step in [i+1 for i in range(len(self.words)-1)]:
            if self.log_steps:
                print('starting step',step)
            # start new beam
            new_beam = []
            # extend each candidate
            for cand in self.beam:
                # try each word
                for (idx,word) in [pair for pair in enumerate(self.words)][1:]:
                    # make sure not already covered
                    if cand.perm[idx] > 0:
                        continue
                    # add word to new candidate
                    new_cand = cand.copy()
                    new_cand.hyp.append(word)
                    # update permutation vector
                    new_cand.perm[idx] = len(new_cand.hyp) - 1
                    # update score
                    # pdb.set_trace()
                    new_cand.score = self.cand_scorer(new_cand)
                    # add to new beam
                    new_beam.append(new_cand)
            # sort, trim new beam
            new_beam.sort(key = sort_key)
            new_beam = new_beam[:self.beam_size]
            # update beam
            self.beam = new_beam
            if self.log_steps:
                print('updated beam:')
                for cand in self.beam:
                    print(cand)
        # update each candidate with </s>, resort
        if self.log_steps:
            print('finalizing')
        for cand in self.beam:
            cand.hyp.append('</s>')
            cand.score = self.cand_scorer(cand)
        self.beam.sort(key = sort_key)
        if self.log_steps:
            print('final beam:')
            for cand in self.beam:
                print(cand)
        # return beam
        return self.beam
                     
# test beam search
def test(ref, log_steps=True):
    if log_steps:
        print('generating from ref:', ref)
    cs = bleu2_cand_scorer(ref)
    # gen = BeamGen(ref,cs,log_steps=log_steps)
    # gen = BeamGen(ref,charscore,log_steps=log_steps)
    gen = BeamGen(ref,wordscore,log_steps=log_steps)
    return gen.search()
    
# run test as main
if __name__ == "__main__": 
    ref = 'Kim loves Sandy madly'.split()
    ref2 = 'President Bush on Tuesday nominated two individuals to replace retiring jurists on federal courts in the Washington area'.split()
    ref3 = 'From the AP comes this story :'.split()
    test(ref)
    test(ref2)
    test(ref3)
