import random
import math

class Field:
    def __init__(self, size: int, count_of_mines: int):
        self.size = size
        self.count_of_mines = count_of_mines
        self.field = [] #shows the positions of mines
        self.game_field = [] #shows the field for users(without mines)

    def generate_mines(self):
        #Check errors
        if self.count_of_mines > self.size * self.size:
            print('The count of mines is bigger than it can be')
            return False
        #Fill the entire field with zeros
        self.field = [[0] * self.size for i in range(self.size)]
        # 0 - no mine, 9 - there is a mine
        # Fill the field with mines randomly
        i = 0
        while i < self.count_of_mines:
            x_cor = int(random.uniform(0,self.size - 1))
            y_cor = int(random.uniform(0,self.size - 1))
            if self.field[x_cor][y_cor] == '☼': #every mine must have it's own position
                i -= 1
            else:
                self.field[x_cor][y_cor] = '☼'
            i += 1
        return True #Succesfully

    def print_field(self):
        print(' ' + '----'*self.size + '\n', end='')
        for i in range(self.size):
            print('|', end='')
            for j in range(self.size):
                print(f' {self.field[i][j]} |', end='')
            print('\n ' + '----'*self.size + '\n', end='')

    def print_game_field(self):
        print(' ' + '----'*self.size + '\n', end='')
        for i in range(self.size):
            print('|', end='')
            for j in range(self.size):
                print(f' {self.game_field[i][j]} |', end='')
            print('\n ' + '----'*self.size + '\n', end='')

    def count_mines_here(self, x_cor: int, y_cor: int):
        if self.field[x_cor][y_cor] == '☼':
            return '☼'
        counter = 0
        for x in range(self.size):
            for y in range(self.size):
                if int(math.sqrt(math.pow(y - y_cor,2) + math.pow(x - x_cor,2))) == 1:
                    if self.field[x][y] == '☼': #If there is a mine here
                        counter += 1
        return ' ' if counter == 0 else counter 

    def create_field(self) -> bool:
        self.game_field = [[' '] * self.size for i in range(self.size)]
        if self.generate_mines() == False:
            return False
        # Now we need to mark every cell
        for i in range(self.size):
            for j in range(self.size):
                self.game_field[i][j] = self.count_mines_here(i,j)
        return True