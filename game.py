import pygame
import math
import time
from field.fields import Field
from sprites.cell import Cell

class Game:
    def __init__(self):
        self.counter = 0 #Counting of unchecked cells(kletok)
        self.running = True
        self.game_statuse = 'playing'

    def start_game(self):
        #inicialization of game
        pygame.init()
        self.screen = pygame.display.set_mode((500,400))
        pygame.display.update()
        pygame.display.set_caption('Сапёр')
        clock = pygame.time.Clock()
        #Create a game field
        self.field = Field(size=10, count_of_mines=15)
        if not self.field.create_field():
            return
        #Create a field background
        self.background = pygame.sprite.Group()
        self.field_background = Cell(True,145,30)
        GRAY = (30, 31, 30)
        self.field_background.set_surface(self.field.size * 20 + self.field.size - 1,self.field.size * 20 + self.field.size - 1) #(209,209) id size == 10
        self.field_background.set_cells_color(color=GRAY)
        self.background.add(self.field_background)
        #Making all cells(sprites)
        self.sprites = self.load_cells_from_field()
        #Is game running? 
        while self.running:
            clock.tick(30) #30 FPS 
            #update the screen
            pygame.display.flip()
            #draw all sprites
            self.screen.fill((0,0,0)) #reset background
            self.background.update() #Draw gray field background
            self.background.draw(self.screen)
            self.make_field_outline() # Draw game's field outline
            self.sprites.update() #draw all cells
            self.sprites.draw(self.screen)
            #Winning statuse and GameOver statuse
            if self.game_statuse == 'winning':
                self.Win()
            elif self.game_statuse == 'gameover':
                self.Game_over()
            #Catching all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_statuse == 'playing':
                    #get mouse coordinates
                    pos = pygame.mouse.get_pos()
                    #Find the sprite(cell) which was clicked
                    clicked_sprite = [s for s in self.sprites if s.rect.collidepoint(pos)]
                    if not clicked_sprite:
                        break
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        self.show_empty_area(clicked_sprite[0])
                    elif mouse_presses[2]:
                        self.mark_cell_as_mine(clicked_sprite[0])
        #End of game
        pygame.quit()
            
    def make_field_outline(self):
        mask = pygame.mask.from_surface(self.field_background.image)
        mask_outline = mask.outline()
        n = 0
        for point in mask_outline:
            mask_outline[n] = (point[0] + self.field_background.x_cor, point[1] + self.field_background.y_cor)
            n += 1
        pygame.draw.polygon(self.screen,"crimson",mask_outline, 1)


    def load_cells_from_field(self):
            sprites = pygame.sprite.Group()
            x_cor = 145 #Base padding 
            y_cor = 30
            for i in range(self.field.size):
                x_cor = 145
                for j in range(self.field.size):
                    new_sprite = Cell(False, x_cor,y_cor)
                    new_sprite.set_cells_value(self.field.game_field[i][j])
                    sprites.add(new_sprite)
                    x_cor += 21
                y_cor += 21
            return sprites
    
    def show_cell(self, cell: Cell):
        pygame.font.init()
        text_font = pygame.font.SysFont('Arial', 14)
        COLOR = (204,204,59) if cell.value == '☼' else (255,255,255)
        cell.image = text_font.render(f'{cell.value}', False, COLOR)

    def show_empty_area(self, cell: Cell):
        #If this cell is already checked
        if cell.is_opened == True:
            return
        elif cell.value == '☼': #End of game, Game Over
            self.game_statuse = 'gameover'
            return
        #Show this cell
        self.show_cell(cell=cell)
        cell.is_opened = True
        self.counter += 1
        #End of game, Win
        if self.counter == self.field.size**2 - self.field.count_of_mines:
            self.game_statuse = 'winning'
            return
        #Break recursion
        if cell.value != ' ': 
            return
        #Body of recursion
        for i in range(self.field.size):
            for j in range(self.field.size):
                x_cor = (cell.x_cor - 145) // 21 #Getting the ccordinates in field (x, y)
                y_cor = (cell.y_cor - 30) // 21
                if int(math.sqrt((i - y_cor)**2 + (j - x_cor)**2) ) == 1:
                    neighbour = [s for s in self.sprites if (30 + i * 21) == s.y_cor and (145 + j * 21) == s.x_cor]
                    self.show_empty_area(neighbour[0])
    
    def mark_cell_as_mine(self, cell: Cell):
        if cell.is_opened == True:
            return
        if cell.image.get_at((0, 0)) == (204,204,59):
            cell.set_cells_color("crimson")
        else:
            cell.set_cells_color((204,204,59))

    def Win(self):
        pygame.font.init()
        text_font = pygame.font.SysFont('Comic Sans MS', 24)
        text_surface = text_font.render(f'You won!', False, (255,255,255))
        text_rect = text_surface.get_rect(center=(250,300))
        self.screen.blit(text_surface, text_rect)

    def Game_over(self):
        for cell in self.sprites:
            if cell.value == '☼':
                self.show_cell(cell=cell)
        pygame.font.init()
        text_font = pygame.font.SysFont('Comic Sans MS', 24)
        text_surface = text_font.render(f'Game over!', False, (255,255,255))
        text_rect = text_surface.get_rect(center=(250,300))
        self.screen.blit(text_surface, text_rect)
