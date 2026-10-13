from tower.tower_base import Tower
from util.constants import (
    player_constants as play
)

class BaseTower(Tower):
    image = play.BASE_TOWER_IMAGE
    base_price = 70
    base_shot_cd = 0.7
    
    def __init__(this, stage):
        super().__init__(1, stage, BaseTower.base_shot_cd, BaseTower.image)

class ReinTower(Tower):
    image = play.REIN_TOWER_IMAGE
    base_price = 90
    base_shot_cd = 0.5
    
    def __init__(this, stage):
        super().__init__(2, stage, ReinTower.base_shot_cd, ReinTower.image)

class WizTower(Tower):
    image = play.WIZ_TOWER_IMAGE
    base_price = 100
    base_shot_cd = 0.8
    
    def __init__(this, stage):
        super().__init__(3, stage, WizTower.base_shot_cd, WizTower.image)