from typing import List, Optional

from models.team_model import TeamRead
from models.hero_model import HeroRead

class TeamReadWithHeroes(TeamRead):
    heroes: List[HeroRead] = []


class HeroReadWithTeam(HeroRead):
    team: Optional[TeamRead] = None