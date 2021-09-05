import asterid as ad
import itertools

def taxon_pairs(ts):
    for i in range(len(ts)):
        for j in range(i, len(ts)):
            yield i, j

def has_missing(ts, dm):
    for i, j in taxon_pairs(ts):
        v = dm.getmask((i, j))
        if v == 0:
            return True
    return False

def run_iterations(ts, D, methods):
    fns = {
        "u": lambda ts, D: ad.upgma_star(ts, D) + ";",
        "f": lambda ts, D: ad.fastme_balme(ts, D, 0, 0),
        "n": lambda ts, D: ad.fastme_balme(ts, D, 1, 0),
        "s": lambda ts, D: ad.fastme_balme(ts, D, 1, 1),
        "j": lambda ts, D: ad.fastme_nj(ts, D, 0, 0),
        "N": lambda ts, D: ad.fastme_nj(ts, D, 1, 0),
        "S": lambda ts, D: ad.fastme_nj(ts, D, 1, 1),
    }
    t = None
    for m in methods:
        if m not in fns:
            raise f"{m} not found as a method!"
        f = fns[m]
        t = f(ts, D)
        D.fill_in_transient(ts, t)
    return t

def astrid(gtrees, methods = "uns", explicit = True):
    ts = ad.get_ts(gtrees)
    D = ad.mk_distance_matrix(ts, gtrees)
    if not explicit and len(methods) > 1:
        if not has_missing(ts, D):
            methods = methods[-1]
    return run_iterations(ts, D, methods)

def disco(gtree):
    from disco import get_min_root, tag, decompose, trivial
    import treeswift
    tree = treeswift.read_tree_newick(gtree)
    root, _, _ = get_min_root(tree)
    tree.reroot(root)
    tag(tree)
    out = list(filter(lambda x:x.num_nodes(internal=False) >= 4, decompose(tree)))
    res = []
    for t in out:
        t.suppress_unifurcations()
        res.append(t.newick())
    return res

# https://stackoverflow.com/a/20037408
def flatmap(func, *iterable):
    return itertools.chain.from_iterable(map(func, *iterable))
    
def astrid_disco(gtrees, methods = "uns", explicit = True):
    decomposed = list(flatmap(disco, gtrees))
    return astrid(decomposed, methods, explicit)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str,
                        help="Input tree list file", required=True)
    parser.add_argument("-m", "--methods", type=str,
                        help="methods", default="uns")
    parser.add_argument("-o", "--output", type=str,
                        help="Output tree list file")
    parser.add_argument("--disco", action="store_true")
    parser.add_argument("-a", "--auto", action="store_true")
    args = parser.parse_args()
    with open(args.input) as fh: gtrees = fh.readlines()
    f = astrid_disco if args.disco else astrid
    s = f(gtrees, args.methods, not args.auto)
    with open(args.output, "w+") as oh:
        oh.write(s)
