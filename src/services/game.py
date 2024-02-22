from domain.board import Board
import numpy as np

class Game:
    def __init__(self):
        self.__board = Board()
        self.__game_over = False
        self.__player = 0
    
    @property
    def board(self):
        return self.__board.board
    
    @property
    def last_move(self):
        return self.__board.last_move
    
    @property
    def board_height(self):
        return self.__board.height
    
    @property
    def board_width(self):
        return self.__board.height
    
    @property
    def game_over(self):
        return self.__game_over
    
    @property
    def player(self):
        return self.__player
    
    @player.setter
    def player(self, value):
        self.__player = value
    
    @game_over.setter
    def game_over(self, value):
        self.__game_over = value
    
    def change_player(self):
        '''
        Changes the current player
        '''
        self.__player = self.__player ^ 1
    
    def is_valid_move(self, row, col):
        '''
        Checks if the move is valid
        :param row: the row of the move
        :param col: the column of the move
        :return: True if the move is valid, False otherwise
        '''
        return 0 <= row < self.board_height and 0 <= col < self.board_width and self.__board.element(row, col) == -1
    
    def add_move(self, row, col):
        '''
        Adds a move to the board
        :param row: the row of the move
        :param col: the column of the move
        '''
        self.__board.add_move(row, col, self.__player)
        
    def add_specific_move(self, row, col, player):
        '''
        Adds a move to the board (stating for which player)
        :param row: the row of the move
        :param col: the column of the move
        :param player: the player for which the move is made
        '''
        self.__board.add_move(row, col, player)
        
    def remove_move(self, row, col):
        '''
        Removes a move from the board
        :param row: the row of the move
        '''
        if 0 <= row < self.board_height and 0 <= col < self.board_width:
            self.__board.remove_move(row, col)
    
    def is_winner(self, row, col, player):
        '''
        Checks if the current player is the winner, based on the last move
        :param row: the row of the move
        :param col: the column of the move
        :param player: the player for which the move is made
        :return: True if the current player is the winner, False otherwise
        '''
        return self.check_line(row, col, 0, 1, player) or \
            self.check_line(row, col, 1, 0, player) or \
            self.check_line(row, col, 1, 1, player) or \
            self.check_line(row, col, -1, 1, player) or \
            self.check_line(row, col, 1, -1, player)
            
    def check_line(self, row, col, row_step, col_step, player):
        '''
        Checks the lines for consecutive moves that are made by the same player
        If there are 5 consecutive moves, the game is over
        :param row: the row of the move (last move)
        :param col: the column of the move (last move)
        :param row_step: the step for the row
        :param col_step: the step for the column
        :return: True if there are 5 consecutive moves, False otherwise
        '''
        max_count = 0
        count = 0
        for direction in [1, -1]:
            for i in range(5):
                current_row = row + i * row_step * direction
                current_col = col + i * col_step * direction
                if 0 <= current_row < self.board_height and 0 <= current_col < self.board_width:
                    if self.__board.element(current_row, current_col) == player:
                        count += 1
                        max_count = max(max_count, count)
                        if max_count == 5:
                            self.__game_over = True
                            return True
                    else:
                        count = 0
                else:
                    count = 0
        return False
    
    def has_nearby_moves(self, row, col):
        '''
        Checks if there are nearby moves, near the last move
        :param row: the row of the move
        :param col: the column of the move
        :return: True if there are nearby moves, False otherwise
        '''
        for i in range(-2, 2):
            for j in range(-2, 2):
                if 0 <= row + i < self.board_height and 0 <= col + j < self.board_width and self.__board.element(row + i, col + j) == 1:
                    return True
        return False
    
    def search_winning_move(self):
        '''
        Checks if there is a winning move for the computer player. Makes the move if there is one.
        :return: True if there is a winning move, False otherwise
        '''
        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.is_valid_move(row, col):
                    self.add_move(row, col)
                    if self.is_winner(row, col, 1):
                        return True
                    
                    self.remove_move(row, col)
        return False
    
    def check_four_threat(self, row, col, player):
        '''
        Checks if there are 3 consecutive active cells for the player, in which case,
        the computer player has to block the move. This is particulary useful when the 3 consecutive cells
        are in the center(not adjacent to the borders).
        :param row: the row of the move
        :param col: the column of the move
        :param player: the player for which the check is made
        :return: True if there are 3 consecutive active cells, False otherwise
        '''
        directions = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 1)]

        for direction in directions:
            count = 0
            for i in range(-3, 3):
                current_row = row + i * direction[0]
                current_col = col + i * direction[1]
                if 0 <= current_row < self.board_height and 0 <= current_col < self.board_width and self.__board.element(current_row, current_col) == player:
                    count += 1
                    if count >= 4:
                        return True
                else:
                    count = 0


        return False
    
    def search_blocking_move(self):
        '''
        Checks if there is a move that the computer player has to block.
        Firstly we check if there are winning moves that require blocking.
        If there are no winning moves, we check if there are 3 consecutive active cells for the player.
        In both cases we block.
        :return: True if there is a move that the computer player has to block, False otherwise
        '''
        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.is_valid_move(row, col):
                    self.add_specific_move(row, col, 0)
                    
                    if self.is_winner(row, col, 0):
                        self.remove_move(row, col)
                        self.__game_over = False
                        self.add_move(row, col)
                        return True
                    
                    self.remove_move(row, col)
                    
        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.is_valid_move(row, col):
                    self.add_specific_move(row, col, 0)
                    
                    if self.check_four_threat(row, col, 0):
                        self.remove_move(row, col)
                        self.add_move(row, col)
                        return True
                    
                    self.remove_move(row, col)
                    
        return False
    
    def search_nearby_move(self):
        '''
        Searches for the first nearby move, near an active cell (computer). Makes that move.
        This is in case there are no winning moves or blocking moves.
        :return: True if there is a nearby move, False otherwise
        '''
        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.is_valid_move(row, col) and self.has_nearby_moves(row, col):
                    self.add_move(row, col)
                    return True
        return False
    
    def make_random_move(self):
        '''
        In case there are no winning moves, blocking moves or nearby moves, the computer player makes a random move.
        '''
        empty_cells = [(r, c) for r in range(self.board_height) for c in range(self.board_width) if self.__board.element(r, c) == -1]
        if empty_cells:
            random_index = np.random.choice(len(empty_cells))
            random_row, random_col = empty_cells[random_index]
            self.add_move(random_row, random_col)
    
    def make_computer_move(self):
        '''
        Makes a move for the computer player.
        '''
        self.search_winning_move() or self.search_blocking_move() or self.search_nearby_move() or self.make_random_move()