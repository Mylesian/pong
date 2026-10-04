import pygame
import level.enemy as enemy
import util.timer as timer
from util.constants import (
    player_constants as play,
    projectile_constants as proj,
    enemy_constants as enm
)

# base class for tower, should probably be made into an abstract kinda thing but i just wanted to get the code working
# eg this is the base tower class and then other subclasses in this folder are types of towers you can buy with their buttons
class Tower:
    def __init__(this, stage, pos: pygame.math.Vector2):
        this.pos = pos
        this.state = play.NOT_PLACED
        this.image = play.BASE_TOWER_IMAGE
        this.stage = stage
        this.shot_timer = timer.Timer(0.5, False)
    
    def place(this):
        this.state = play.PLACED
    
    def update(this, dt: float, enemies: list[enemy.Enemy], mouse_down: bool):
        match this.state:
            case play.NOT_PLACED:
                this.pos = pygame.math.Vector2(pygame.mouse.get_pos())
                if mouse_down:
                    this.state = play.PLACED
            case play.PLACED:
                this.shot_logic(dt, enemies)
            
    def shot_logic(this, dt: float, enemies: list[enemy.Enemy]):
        if this.shot_timer.countdown(dt):
            for e in enemies:
                if this.pos.distance_squared_to(e.pos) <= play.TOWER_VIEW_RADIUS_SQUARED:
                    this.shoot(e)
                    this.shot_timer.reset()
                    break
    
    def shoot(this, enemy: enemy.Enemy):
        this.stage.projectiles.append(Projectile(this.pos, enemy.pos, 1))

# projectile class shot from a tower
class Projectile:
    def __init__(this, pos: pygame.math.Vector2, target: pygame.math.Vector2, damage: int):
        this.pos: pygame.math.Vector2 = pygame.math.Vector2(pos)
        dist = target - pos
        this.velocity = dist / dist.magnitude() * proj.PROJECTILE_SPEED
        this.image = proj.PROJECTILE_IMAGE
        this.damage = damage
        
    def update(this, enemies: list[enemy.Enemy]):
        this.pos += this.velocity
        for e in enemies[:]:
            if this.pos.distance_squared_to(e.pos) <= (proj.PROJECTILE_RADIUS + enm.ENEMY_RADIUS) ** 2:
                e.hp -= this.damage
                e.set_image()
                e.set_velocity()
                return True
        
        return False