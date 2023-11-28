from fastapi import FastAPI

from db.database import create_db_and_tables

from routers.hero_router import router as hero_router
from routers.team_router import router as team_router

app = FastAPI()

app.include_router(hero_router)
app.include_router(team_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
