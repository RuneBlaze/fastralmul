import treeswift as ts
from bitarray import bitarray
from random import choice, random, sample
from functools import reduce
import numpy as np
from icecream import ic

def leafset(tree):
    l = set(int(e.split("_")[0]) for e in tree.labels(True, False))
    return l

def is_complete_cover(cands, valid, universe):
    if not cands:
        return False
    valid_cands = [cands[i] for i in valid]
    if not valid_cands:
        return False
    finalcover = reduce(lambda x, y: x | y, valid_cands)
    if finalcover != universe:
        return False
    return True

# greedy heuristic for set cover
def obtain_cover(cands, valid, universe):
    if not is_complete_cover(cands, valid, universe):
        return None
    currentcover = bitarray(len(universe))
    
    currentcover.setall(0)
    cover = []
    while currentcover != universe:
        itr = list(valid)
        i = np.argmax([((~currentcover) & cands[j]).count() for j in itr])
        valid.remove(itr[i])
        cover.append(itr[i])
        currentcover |= cands[itr[i]]
    return cover

class TreeSampler():
    def __init__(self, G):
        self.G = G
        S = set()
        self.naive_leafsets = list(map(leafset, G))
        for ls in self.naive_leafsets:
            for l in ls:
                S.add(l)
        self.S = sorted(S)
        self.mapper = {}
        for i, s in enumerate(self.S):
            self.mapper[s] = i
        self.eff_leafsets = [self.eff_leafset(x) for x in self.naive_leafsets]
        self.covers = None
        U = bitarray(len(self.S))
        U.setall(1)
        self.U = U

    def eff_leafset(self, leafset):
        x = bitarray(len(self.S))
        x.setall(0)
        for l in leafset:
            x[self.mapper[l]] = 1
        return x
        
    def is_subsample_complete(self, subsample_inds):
        return is_complete_cover(self.eff_leafsets, subsample_inds, self.U)

    def robust_sample(self, fn, r, tries = 0):
        U = self.U
        subsample = fn(r)
        if not is_complete_cover(self.eff_leafsets, subsample, U):
            if not self.covers:
                self.covers = self.compute_covers()
            cover = list(choice(self.covers))
            if len(subsample) < len(cover):
                # resample
                if tries >= 5:
                    return self.robust_sample(fn, r + 0.02, tries + 1)
                else:
                    return self.robust_sample(fn, r, tries + 1)
            todelete = sample(subsample, len(cover))
            for i in todelete:
                subsample.remove(i)
            subsample.update(cover)
        return subsample

    def iid_sample(self, r):
        subsample = set()
        for i in range(len(self.G)):
            if random() < r:
                subsample.add(i)
        return subsample

    def iid_sampler(self):
        return lambda r: self.iid_sample(r)
    
    def choice_sampler(self):
        return lambda r: self.choice_sample(r)

    def choice_sample(self, r):
        r = min(1, r)
        s = len(self.G)
        l = round(s * r)
        return set(sample(range(len(self.G)), l))

    def compute_covers(self):
        covers = []
        complete_cover_inds = [i for i, ls in enumerate(self.naive_leafsets) if len(ls) == len(self.S)]
        for i in complete_cover_inds:
            covers.append(set([i]))
        inds = set(range(len(self.G))) - set(complete_cover_inds)
        U = bitarray(len(self.S))
        U.setall(1)
        while len(covers) < len(self.G) / 20:
            c = obtain_cover(self.eff_leafsets, inds, U)
            if not c:
                break
            covers.append(c)
        return covers