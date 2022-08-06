import yaml
import numpy as np
import requests

with open("piece.yaml") as f:
    d = yaml.safe_load(f)

url = "http://localhost:8000/"

for key in d.keys():
    c = np.where(np.array(d[key])==1)
    print(key)
    base_shape = [{"x":int(x), "y":int(y)} for x,y in zip(c[0],c[1])]
    print(base_shape)
    body = {
        "name": key,
        "base_shape": base_shape
    }
    r_post = requests.post(url, json=body)
    



