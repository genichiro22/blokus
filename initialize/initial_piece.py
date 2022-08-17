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
    r_post = requests.post(url+"pieces/", json=body)
    
requests.post(url+"pieces/all/")

requests.post(url+"field/")

i = 0
for name in ["isshin", "genichiro", "sekiro", "fukuro"]:
    body = {
        "name": name,
        "turn": 0,
        "is_current": (i==0)
    }
    requests.post(url+"player/", json=body)
    i = 1

requests.post(url+"player/pieces/")

body = {
    "player": 1,
    "piece_id": 1,
    "fr_id": 0,
    "coordinate": {
        "x": 0,
        "y": 19
    }
}

requests.post(url+"field/piece/", body)
body["player"]+=1
body["coordinate"]["x"]=19
requests.post(url+"field/piece/", body)
body["player"]+=1
body["coordinate"]["y"]=19
requests.post(url+"field/piece/", body)
body["player"]+=1
body["coordinate"]["x"]=0
requests.post(url+"field/piece/", body)
body["player"]=1
body["coordinate"]["x"]=1
body["coordinate"]["y"]=1
requests.post(url+"field/piece/", body)
body["piece_id"]=2
requests.post(url+"field/piece/", body)