import yaml
import numpy as np

with open("piece.yaml") as f:
    yml = yaml.safe_load(f)
print(yml)

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
        drop_i = []
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

new_yml = {key: flip_rot(yml[key]) for key in yml.keys()}
for s in new_yml.keys():
    print(s)
    print(new_yml[s])
    drop_dup(new_yml[s])
    print(new_yml[s])