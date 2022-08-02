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

new_yml = {key: flip_rot(yml[key]) for key in yml.keys()}

print(new_yml)