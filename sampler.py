import treeswift as ts
from bitarray import bitarray
from random import choice

def leafset(tree):
    l = Set(int(e.split("_")[0]) for e in tree.labels(True, False))
    return l

class TreeSampler():
    def __init__(self, G):
        self.G = G
        S = set()
        self.naive_leafsets = list(map(leafset, G))
        for ls in naive_leafsets:
            for l in ls:
                S.add(l)
        self.S = sorted(S)
        self.mapper = {}
        for i, s in enumerate(self.S):
            self.mapper[s] = i
        self.eff_leafsets = [self.eff_leafset(x) for x in self.naive_leafsets]
        self.covers = None

        self.compute_covers()

    def eff_leafset(self, leafset):
        x = bitarray(size)
        x.setall(0)
        for l in leafset:
            x[self.mapper[l]] = 1
        return x

    def ensure_subsample(self, subsample_inds):
        if is_subsample_complete(subsample_inds):
            return subsample_inds
        c = choice(self.covers)
        l = len(c)
        for i in range(l):
            ind = choice(subsample_inds)
            subsample_inds.remove(ind)
        return subsample_inds.union(c)
        
    def is_subsample_complete(self, subsample_inds):
        if len(subsample_inds) == 1:
            return self.eff_leafsets[subsample_inds[0]].all()
        fst = self.eff_leafsets[subsample_inds[0]]
        for i in range(1, len(subsample_inds)):
            fst |= self.eff_leafsets[subsample_inds[i]]
            if fst.all():
                return True
        return False

    def compute_covers(self):
        covers = []
        complete_cover_inds = [i for i, ls in enumerate(self.naive_leafsets) if len(ls) == len(self.S)]
        for i in complete_cover_inds:
            covers.append(set([i]))
        while len(covers) < len(self.G) / 20:
            pass # FIXME: compute the set covers
