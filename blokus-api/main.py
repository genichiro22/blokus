from fastapi import FastAPI
from piece import rotate
import json
pieces_fr = rotate.pieces_fr
p_fr_base = {key: [x.tolist() for x in pieces_fr[key]] for key in pieces_fr.keys()}

app = FastAPI()

@app.get("/")
def index():
    return json.dumps(p_fr_base)

@app.get("/{piece_name}/")
def fr(piece_name):
    return json.dumps(p_fr_base[piece_name])

@app.get("/{piece_name}/{id}")
def fr(piece_name:str,id:int):
    return json.dumps(p_fr_base[piece_name][id])
