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
    image: pygame.Surface = None
    base_price: int = None
    def __init__(this, type, stage, shot_timer: float, image: pygame.Surface):
        this.pos = pygame.mouse.get_pos()
        this.x = pygame.mouse.get_pos()[0]
        this.y = pygame.mouse.get_pos()[1]
        this.state = play.NOT_PLACED
        this.image = image
        this.stage = stage
        this.type = type
        match this.type:
            case 1:
                this.range = play.TOWER_VIEW_RADIUS_SQUARED
            case 2:
                this.range = play.TOWER_VIEW_RADIUS_SQUARED * 1.5
            case 3:
                this.range = play.TOWER_VIEW_RADIUS_SQUARED * 2
        this.shot_timer = timer.Timer(shot_timer, False)
    
    def place(this):
        this.state = play.PLACED
    
    def update(this, dt: float, enemies: list[enemy.Enemy], mouse_just_down: bool):
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        match this.state:
            case play.NOT_PLACED:
                this.pos = mouse_pos
                if mouse_just_down:
                    this.state = play.PLACED
                
            case play.PLACED:
                this.shot_logic(dt, enemies)
                if (mouse_just_down and 
                    mouse_pos[0] > this.x - play.TOWER_RADIUS / 2 and
                    mouse_pos[0] < this.x + play.TOWER_RADIUS / 2 and
                    mouse_pos[1] > this.y - play.TOWER_RADIUS / 2 and
                    mouse_pos[1] < this.y + play.TOWER_RADIUS / 2):
                    this.state = play.NOT_PLACED
            
    def shot_logic(this, dt: float, enemies: list[enemy.Enemy]):
        if this.shot_timer.countdown(dt):
            for e in enemies:
                if this.pos.distance_squared_to(e.pos) <= this.range:
                    this.shoot(e)
                    this.shot_timer.reset()
                    break
    
    def shoot(this, enemy: enemy.Enemy):
        this.stage.projectiles.append(Projectile(this.stage, this.type, this.pos, enemy.pos, this.type))

# projectile class shot from a tower
class Projectile:
    def __init__(this, stage, tower, pos: pygame.math.Vector2, target: pygame.math.Vector2, damage: int):
        this.pos: pygame.math.Vector2 = pygame.math.Vector2(pos)
        dist = target - pos
        this.velocity = dist / dist.magnitude() * proj.PROJECTILE_SPEED
        this.damage = damage
        this.stage = stage
        this.angle = 0
        match tower:
            case 1:
                this.base_image = proj.BASE_IMAGE
            case 2:
                this.base_image = proj.REIN_IMAGE
            case 3:
                this.base_image = proj.WIZ_IMAGE
        this.image = this.base_image
        
    def update(this, enemies: list[enemy.Enemy]):
        this.pos += this.velocity
        this.velocity *= 1.05
        this.angle = (this.angle + proj.SPIN_SPEED) % 360
        this.image = pygame.transform.rotate(this.base_image, this.angle)
        for e in enemies[:]:
            if this.pos.distance_squared_to(e.pos) <= (proj.PROJECTILE_RADIUS + enm.ENEMY_RADIUS) ** 2:
                e.hp -= this.damage
                if e.hp < 0: e.hp = 0
                
                this.stage.current_money += 1
                
                e.set_image()
                e.set_velocity()
                return True
        
        return False