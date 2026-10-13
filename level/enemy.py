import pygame
import level.track as track
import util.timer
from util.constants import (
    enemy_constants as e
)

# spawns after its timer goes down
# goes along the track
# different pictures for different hp
class Enemy(util.timer.Dependent):
    def __init__(this, max_hp: int, path: track.Track,  dest: list['Enemy']):
        this.max_hp = max_hp
        this.hp = max_hp
        match this.hp:
            case 2:
                this.status = "high"
            case 1: 
                this.status =  "low"
        this.set_image()
        this.path = path
        this.x = path.points[0][0]
        this.y = path.points[0][1]
        this.pos = pygame.math.Vector2(this.x, this.y)
        this.target_pos = 1
        this.set_velocity()
        
        this.dest = dest
        
        this.vel = 10
        this.stre = 10
        this.dx = 10
        this.ground = this.y
        this.animate = True
    
    def move_along_track(this):
        if ((this.pos - this.path.points[this.target_pos - 1]).magnitude_squared() >
           (this.path.points[this.target_pos] - this.path.points[this.target_pos - 1]).magnitude_squared()):
            this.pos = pygame.math.Vector2(this.path.points[this.target_pos])
            this.target_pos += 1
            
            if this.target_pos >= this.path.points.__len__():
                return False
            
            this.set_velocity()
            
        if this.hp <= 0: return False

        this.pos += this.velocity
        return True
        
    def set_velocity(this):
        if this.hp > 0:
            vel = this.path.points[this.target_pos] - this.pos
            this.velocity = vel / vel.magnitude() * e.ENEMY_BASE_SPEED * this.hp
        
    def set_image(this):
        match this.status:
            case "low":
                this.image = e.ENEMY_IMAGE_1HP
            case "high":
                this.image = e.ENEMY_IMAGE_2HP

    def death_animate(this):
        if not this.animate:
            return False
        
        this.y -= this.stre
        this.x -= this.dx
        this.stre -= this.vel
        if this.y > this.ground:
            this.y = this.ground
            this.stre *= -0.75
            this.dx *= 0.75
        if abs(this.stre) < 1:
            this.vel = 0
            this.dx = 0
            this.stre = 0
            this.animate = False
                      
    def update(this):
        this.dest.append(this)