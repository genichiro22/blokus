import yaml
import numpy as np

with open("piece/piece.yaml") as f:
    _yml = yaml.safe_load(f)
# print(_yml)

def flip_rot(p):
    res = []
    p = np.array(p)
    for i in range(4):
        p_ = np.rot90(p)
        q_ = np.flipud(p_)
        res.append(p_)
        res.append(q_)
        p = p_
    return res

def drop_dup(l):
    while True:
        # print("current", l)
        n = len(l)
        loop=False
        for i in range(n):
            for j in range(n):
                a = tuple([tuple(e) for e in l[i]])
                b = tuple([tuple(e) for e in l[j]])
                if i>j and a==b:
                    del l[i]
                    loop = True
                    break
            else:
                continue
            break
        if not loop:
            break

pieces_fr = {key: flip_rot(_yml[key]) for key in _yml.keys()}
for s in pieces_fr.values():
    drop_dup(s)
# print(pieces_fr)