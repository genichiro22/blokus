from fastapi import FastAPI
from database import engine, Base
from routes import piece, field, player, frontend

app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(piece.router)
app.include_router(field.router)
app.include_router(player.router)
app.include_router(frontend.router)