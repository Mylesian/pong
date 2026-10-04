import pygame
from util.constants import (
    stage_constants as stage
)

# just a class to hold all the points for the stage's track
class Track:
    def __init__(this, points: list[tuple]):
        this.points: list[pygame.math.Vector2] = []
        
        for pt in points:
            this.points.append(pygame.math.Vector2(pt[0], pt[1]))
    
    def draw(this, screen: pygame.Surface):
        for i in range(this.points.__len__() - 1):
            pygame.draw.line(screen, stage.TRACK_COLOR, this.points[i], this.points[i+1], stage.TRACK_THICKNESS)