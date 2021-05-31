from sampler_frontend import *
from treeutils import *

trees = import_trees("assets/g_100.trees")
sampler = TreeSampler(trees)
def test_trivial_samplers():
    for rep in range(10):
        for i in [51, 101, 151]:
            for st in [1,2,4]:
                assert len(STRATEGIES[st](i, sampler)) == i