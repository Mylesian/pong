import inspect
import pygame
from util.button import Button
from tower import tower_types, tower_base
from util.constants import (
    screen_constants as sc,
    stage_constants as st,
    player_constants as play
)

# actual shop, displays towers player can buy
class Shop(pygame.Surface):
    def __init__(this, stage):
        super().__init__((st.SHOP_WIDTH, st.STAGE_DIMENSIONS[1]))
        
        this.itemlist: list[ShopElement] = []
        y_offset = 0
        for name, cls in inspect.getmembers(tower_types, inspect.isclass):
            if cls in tower_base.Tower.__subclasses__():
                this.itemlist.append(ShopElement(stage, pygame.math.Vector2(0, y_offset), cls))
                y_offset += st.SHOP_WIDTH / 2
    
    def draw(this) -> 'Shop':
        this.fill(st.SHOP_BGCOLOR)
        for item in this.itemlist:
            this.blit(item.get_full_image(), (item.pos.x, item.pos.y))
        
        return this
    
    def update(this, mouse_just_down: bool):
        for item in this.itemlist:
            item.update(mouse_just_down)

# an element in the shop, displays image of tower and price
class ShopElement(Button):
    def __init__(this, stage, pos: pygame.math.Vector2, type: type[tower_base.Tower]):
        this.pos = pos
        this.item_image = type.image
        this.price = type.base_price
        
        def action():
            for tower in stage.towers:
                if tower.state == play.NOT_PLACED:
                    return
            
            if stage.current_money >= type.base_price:
                stage.towers.append(type(stage))
                stage.current_money -= type.base_price
        
        super().__init__((pos.x + st.STAGE_DIMENSIONS[0], pos.y, type.image.get_width(), type.image.get_height() + 100), this.get_full_image(), action)

    def get_full_image(this) -> pygame.Surface:
        price_render = sc.GAME_FONT.render(f'{this.price}', False, sc.MONEY_FONT_COLOR)
        img = pygame.Surface((this.item_image.get_width(), this.item_image.get_height() + price_render.get_height()))
        img.fill(st.SHOP_BGCOLOR)
        img.blit(this.item_image, (0, 0))
        img.blit(price_render, (0, this.item_image.get_height()))
        
        return img
        