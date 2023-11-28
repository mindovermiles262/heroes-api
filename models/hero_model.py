from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team: Optional["Team"] = Relationship(back_populates="heroes")


class HeroCreate(HeroBase):
    pass


class HeroRead(HeroBase):
    id: int

# Create a new "Update" Model wtih the same "HeroBase" fields, just optional.
class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None
