from sampler import TreeSampler
from treeutils import *
import treeswift as ts
import pickle
from icecream import ic
import pickle
import argparse

def strategy1(nsubsamples, sampler):
    subsamples = []
    s_1 = nsubsamples - 1
    size = len(sampler.G)
    sdiv5 = s_1 // 5
    s2div5 = 2 * s_1 // 5
    subsampler = sampler.choice_sampler()
    subsamples.append(sampler.robust_sample(subsampler, 1))
    for i in range(sdiv5):
        subsamples.append(sampler.robust_sample(subsampler, 0.5))
    for i in range(s2div5):
        subsamples.append(sampler.robust_sample(subsampler, 0.25))
    for i in range(s2div5):
        subsamples.append(sampler.robust_sample(subsampler, 0.1))
    return subsamples

def strategy2(nsubsamples, sampler):
    subsamples = []
    s = nsubsamples
    subsampler = sampler.choice_sampler()
    for i in range(s):
        subsamples.append(sampler.robust_sample(subsampler, 0.25))
    return subsamples

def strategy4(nsubsamples, sampler):
    import numpy as np
    subsamples = []
    s_1 = nsubsamples - 1
    subsampler = sampler.iid_sampler()
    subsamples.append(sampler.robust_sample(subsampler, 1))
    p = np.random.normal(0.5, 0.16, s_1)
    for i in range(s_1):
        # ic(p[i])
        subsamples.append(sampler.robust_sample(subsampler, p[i]))
    return subsamples

STRATEGIES = {
    1: strategy1,
    2: strategy2,
    4: strategy4, 
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, default="-")
    parser.add_argument('-s', '--strategy', type=int, required=True)
    parser.add_argument('-u', '--subsamples', type=int, default=51)
    args = parser.parse_args()
    nsubsamples = args.subsamples
    G = import_trees(args.input)
    strategyfn = STRATEGIES[args.strategy]
    sampler = TreeSampler(G)
    subsamples = strategyfn(nsubsamples, sampler)
    if args.output == '-':
        print(subsamples)
    else:
        with open(args.output, "wb") as of:
            pickle.dump(subsamples, of)