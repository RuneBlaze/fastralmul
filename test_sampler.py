from sampler import *

def test_trivial_setcover():
    U = bitarray('11111')
    cand = [bitarray('11111')]

    assert obtain_cover(cand, set([0]), U) == [0]

def test_second_setcover():
    U = bitarray('11111')
    cand = [bitarray('11100'), bitarray('00011')]

    assert obtain_cover(cand, set([0,1]), U) == [0,1]

def test_third_setcover():
    U = bitarray('11111')
    cand = [bitarray('11100'), bitarray('00011'), bitarray('00001'), bitarray('10000')]

    assert obtain_cover(cand, set(range(len(cand))), U) == [0,1]

def test_fourth_setcover():
    U = bitarray('11111')
    cand = [bitarray('11000'), bitarray('00011'), bitarray('00001'), bitarray('10000')]

    assert obtain_cover(cand, set(range(len(cand))), U) == None

def test_fifth_setcover():
    U = bitarray('11111')
    cand = [bitarray('11000'), bitarray('00011'), bitarray('01111'), bitarray('10000')]
    
    valid = set(range(len(cand)))
    assert obtain_cover(cand, valid, U) == [2,0]
    assert obtain_cover(cand, valid, U) == None

def test_tree_sampler_trivial():
    tree_newicks = ["(0,1,2)","(2,3,4)","(4,5)", "(0,1,2,3,4,5)"]
    trees = [ts.read_tree_newick(t) for t in tree_newicks]
    assert len(trees) == 4

    sampler = TreeSampler(trees)
    assert sampler.choice_sample(1) == set(range(4))
    assert sampler.iid_sample(1) == set(range(4))
    assert len(sampler.choice_sample(0.5)) == 2
    assert len(sampler.choice_sample(0.25)) == 1
    sampler.covers = sampler.compute_covers() # explicitly init set of covers
    assert sampler.covers == [set([3])]
    for i in range(25):
        subsample = sampler.robust_sample(sampler.choice_sampler(), 0.25)
        assert len(subsample) > 0
        assert is_complete_cover(sampler.eff_leafsets, subsample, sampler.U)

def test_tree_sampler_nontrivial():
    tree_newicks = ["(0,1,2)","(2,3,4)","(4,5)", "(0,1,2,3,4,5)"]
    trees = [ts.read_tree_newick(t) for t in tree_newicks]
    sampler = TreeSampler(trees)
    for i in range(30):
        subsample = sampler.robust_sample(sampler.iid_sampler(), 0.1)
        assert 3 in subsample