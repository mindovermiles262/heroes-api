from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List

from db.database import get_session

from models.team_model import TeamBase, Team, TeamCreate, TeamRead, TeamUpdate
from models.heroteam_model import TeamReadWithHeroes

router = APIRouter()

@router.post('/teams', response_model=TeamRead)
def create_team(
    *,
    params_team: TeamCreate,
    session: Session = Depends(get_session)
):
    db_team = Team.from_orm(params_team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get('/teams', response_model=List[TeamRead])
def read_teams(
    *,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session)
):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@router.get("/teams/{team_id}", response_model=TeamReadWithHeroes)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/teams/{team_id}", response_model=TeamRead)
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete("/teams/{team_id}")
def delete_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"status": "deleted"}