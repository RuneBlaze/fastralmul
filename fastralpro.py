import subprocess
from arstid import astrid_disco
import argparse
from sampler_frontend import strategy1
from sampler import TreeSampler
from treeutils import *

def import_trees(fn):
    trees = []
    with open(fn) as fh:
        for l in fh:
            trees.append(ts.read_tree_newick(l))
    return trees

def consensus(trees, minfreq=0.5):
    import dendropy
    res = dendropy.TreeList()
    for treenewick in trees:
        res.read(data=treenewick, schema="newick", rooting='force-unrooted')
    con = res.consensus(min_freq = minfreq)
    con.is_rooted = False
    return con.as_string(schema="newick")

def complete_trees(gtrees, ctree):
    gtreepath = args.output + ".gtrees"
    ctreepath = args.output + ".fctree"
    with open(ctreepath, "w+") as fh:
        fh.write(ctree)
    with open(gtreepath, "w+") as fh:
        for g in gtrees:
            fh.write(g)
            fh.write("\n")
    import subprocess
    cmd = f"java -cp /home/baqiaol2/scratch/Constrained-search/astral.5.6.9.jar phylonet.coalescent.TreeCompletion {gtreepath} {ctreepath}"
    return subprocess.check_output(cmd, shell=True,text=True)

def run_apro(gtreepath, ctreepath, streepath):
    import os
    cmd = f"sh /home/baqiaol2/scratch/A-pro/apro.sh {gtreepath} {ctreepath} {streepath}"
    os.system(cmd)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True)
parser.add_argument('-o', '--output', type=str, default="-")
parser.add_argument('-t', '--threshold', type = float, default = -1)
args = parser.parse_args()
G = import_trees(args.input)
sampler = TreeSampler(G)
samples = strategy1(1, sampler)
X = []
for s in samples:
    X.append(astrid_disco([G[i] for i in s]))

res = None
if args.threshold > 0:
    res = complete_trees(X, consensus(X, args.threshold))
else:
    res = "\n".join(X) + "\n"

def strip(s):
    import treeswift as ts
    trees = [ts.read_tree_newick(s) for l in s.strip().split("\n")]
    for t in trees:
        t.resolve_polytomies()
    for t in trees:
        continue
        for n in t.traverse_postorder(True, True):
            n.edge_length = None
            if not n.is_leaf():
                n.label = None
    return "\n".join([t.newick() for t in trees])

with open(args.input + ".x", "w+") as fh:
    fh.write(strip(res))

run_apro(args.input, args.input + ".x", args.output)
