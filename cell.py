import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self, is_opened: bool, x_cor: int, y_cor: int):
        pygame.sprite.Sprite.__init__(self)
        self.is_opened = is_opened
        self.x_cor = x_cor
        self.y_cor = y_cor
        #make a cell
        self.set_surface(20,20)
        self.set_cells_color("crimson")
        self.rect = self.image.get_rect()
        self.rect.x = x_cor
        self.rect.y = y_cor
    
    def set_cells_value(self, value):
        self.value = value

    def set_cells_color(self, color):
        self.image.fill(color)

    def set_surface(self,height: int, width: int):
        self.image = pygame.Surface((height,width))