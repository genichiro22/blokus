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

for name in ["admin", "isshin", "genichiro", "sekiro", "fukuro"]:
    body = {
        "name": name,
        "pwd": name + "1234",
    }
    requests.post(url+"user/", json=body)

r = requests.post(url+"game/")
game_id = r.json()
print(game_id)
game_id = r.json()["id"]
print(game_id)

for p, u in [(1,1), (3,3), (2,4), (4,2)]:
    body = {"player": p, "user_id": u}
    requests.post(url+f"game/{game_id}/", json=body)

body = {
    "user_id": 1,
    "piece_id": 1,
    "fr_id": 0,
    "coordinate": {
        "x": 0,
        "y": 0
    }
}

put_piece_url = url + f"game/{game_id}/field/piece/"

requests.put(put_piece_url, json=body)
body["user_id"]=4
body["coordinate"]["x"]=19
requests.put(put_piece_url, json=body)
body["user_id"]=3
body["coordinate"]["y"]=19
requests.put(put_piece_url, json=body)
body["user_id"]=2
body["coordinate"]["x"]=0
requests.put(put_piece_url, json=body)
body["user_id"]=1
body["coordinate"]["x"]=1
body["coordinate"]["y"]=1
requests.put(put_piece_url, json=body)
body["piece_id"]=2
requests.put(put_piece_url, json=body)
