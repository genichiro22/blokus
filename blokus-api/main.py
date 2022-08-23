from fastapi import FastAPI
from database import engine, Base
# from routes import piece, field, player, frontend, auth
from routes import user

app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(user.router)

"""
app.include_router(piece.router)
app.include_router(field.router)
app.include_router(player.router)
app.include_router(frontend.router)
app.include_router(auth.router)
"""