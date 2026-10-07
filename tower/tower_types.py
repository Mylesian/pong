from tower.tower_base import Tower
from util.constants import (
    player_constants as play
)

class BaseTower(Tower):
    image = play.BASE_TOWER_IMAGE
    base_price = 70
    
    def __init__(this, stage):
        super().__init__(stage, 0.5, BaseTower.image)