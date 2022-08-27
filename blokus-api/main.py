from fastapi import FastAPI
from database import engine, Base
# from routes import piece, field, player, frontend, auth
from routes import user, game, piece, auth, frontend

app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(user.router)
app.include_router(game.router)
app.include_router(piece.router)
app.include_router(auth.router)
app.include_router(frontend.router)
