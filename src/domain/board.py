import numpy as np

class Board:
    def __init__(self, height = 15, width = 15):
        self.HEIGHT = height
        self.WIDTH = width
        self.__board = np.full((self.HEIGHT, self.WIDTH), -1, dtype = int)
        self.__last_move = None
    
    @property
    def board(self):
        return self.__board
    
    @property
    def last_move(self):
        return self.__last_move
    
    @property
    def height(self):
        return self.HEIGHT
    
    @property
    def width(self):
        return self.WIDTH
    
    def element(self, row, col):
        return self.__board[row, col]
    
    def add_move(self, row, col, player):
        self.__board[row, col] = player
        self.__last_move = (row, col)

    def add_temp_move(self, row, col, player):
        self.__board[row, col] = player
        
    def remove_move(self, row, col):
        self.__board[row, col] = -1