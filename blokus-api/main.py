from cmath import pi
from fastapi import FastAPI, Depends, status, Response
from piece import rotate
import json
pieces_fr = rotate.pieces_fr
p_fr_base = {key: [x.tolist() for x in pieces_fr[key]] for key in pieces_fr.keys()}

app = FastAPI()

@app.get("/")
def index():
    return json.dumps(p_fr_base)

@app.get("/{piece_name}/", status_code=status.HTTP_200_OK)
def fr(piece_name:str, response:Response):
    if piece_name not in p_fr_base.keys():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Piece name of {piece_name} is not available"}
    return json.dumps(p_fr_base[piece_name])

@app.get("/{piece_name}/{id}", status_code=status.HTTP_200_OK)
def fr(piece_name:str, id:int, response:Response):
    if piece_name not in p_fr_base.keys():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Piece name of {piece_name} is not available"}
    if id>=len(p_fr_base[piece_name]):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Index {id} is not found in flip-rotation of the piece {piece_name}"}
    return json.dumps(p_fr_base[piece_name][id])
