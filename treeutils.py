import treeswift as ts

def import_trees(fn):
    trees = []
    with open(fn) as fh:
        for l in fh:
            trees.append(ts.read_tree_newick(l))
    return trees