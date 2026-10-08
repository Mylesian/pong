from tower.tower_base import Tower
from util.constants import (
    player_constants as play
)

class BaseTower(Tower):
    image = play.BASE_TOWER_IMAGE
    base_price = 70
    base_shot_cd = 0.7
    
    def __init__(this, stage):
        super().__init__(stage, BaseTower.base_shot_cd, BaseTower.image)