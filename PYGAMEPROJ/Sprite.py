import pygame
from Setting import *
pygame.font.init()
class Tile(pygame.sprite.Sprite):
    def __init__(self,game,x,y,text,defa=-1):
        self.groups = game.all
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.x = x
        self.y = y
        self.text = text
        self.rect = self.image.get_rect()
        if self.text!="empty":
            self.font = pygame.font.SysFont("Consolas",50)
            font_surface = self.font.render(self.text , True,BLACK)
            self.image.fill(WHITE)
            self.font_size=self.font.size(text)
            self.image.blit(font_surface,((TILESIZE/2 - self.font_size[0] /2) ,(TILESIZE/2 - self.font_size[1] /2)))
        
        elif defa != -1:
            self.font = pygame.font.SysFont("Consolas",50)
            font_surface = self.font.render(self.text , True,BLACK)
            self.image.fill(WHITE)
            self.font_size=self.font.size(text)
            self.image.blit(font_surface,((TILESIZE/2 - self.font_size[0] /2) ,(TILESIZE/2 - self.font_size[1] /2)))
    def update(self):
        self.rect.x = self.x*TILESIZE
        self.rect.y = self.y*TILESIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom
    def right(self):
        return self.rect.x + TILESIZE < GAME_SIZE*TILESIZE
    def left(self):
        return self.rect.x-TILESIZE>=0
    def up(self):
        return self.rect.y-TILESIZE>=0
    def down(self):
        return self.rect.y+TILESIZE< GAME_SIZE*TILESIZE
class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))


class Button:
    def __init__(self, x, y, width, height, text, colour, text_colour):
        self.colour, self.text_colour = colour, text_colour
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, self.text_colour)
        self.font_size = font.size(self.text)
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))

    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height