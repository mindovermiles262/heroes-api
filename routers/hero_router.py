from typing import List

from fastapi import APIRouter, FastAPI, HTTPException, Query, Depends
from sqlmodel import Session, select

from db.database import create_db_and_tables, engine, get_session

from models.hero_model import HeroBase, Hero, HeroRead, HeroCreate, HeroUpdate
from models.heroteam_model import HeroReadWithTeam, TeamReadWithHeroes

router = APIRouter()


@router.get('/heroes', response_model=List[HeroRead])
def read_heroes(
    *,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session)
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get('/heroes/{hero_id}', response_model=HeroReadWithTeam)
def read_hero(*, hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.post('/heroes', response_model=HeroRead)
def create_hero(*, hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.patch('/heroes/{hero_id}', response_model=HeroRead)
def update_hero(
    *, hero_id: int,
    hero: HeroUpdate,
    session: Session = Depends(get_session)
):
    # Get the existing Hero from the DB
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    # Get incoming data as dict
    hero_data = hero.dict(exclude_unset=True)
    
    # Set/Update any attributes on the db_hero from the incoming data
    for k, v in hero_data.items():
        setattr(db_hero, k, v)

    # Persist changes
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.delete('/heroes/{hero_id}')
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"status": "deleted"}
