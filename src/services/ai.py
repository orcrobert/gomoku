import numpy as np
from domain.board import Board

class AI:
    def __init__(self):
        self.__board = Board()
        self.__game_over = False
        self.max_depth = 3
        self.board_height = 15
        self.board_width = 15
        self.__player = 0
        self.COMPUTER = 1
        self.PLAYER = 0
        self.EMPTY = -1

    @property
    def board(self):
        return self.__board.board

    @property
    def game_over(self):
        return self.__game_over
    
    @game_over.setter
    def game_over(self, value):
        self.__game_over = value
        
    @property
    def player(self):
        return self.__player
    
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

    def is_board_full(self):
        '''
        Checks if the board is full
        :return: True if the board is full, False otherwise
        '''
        return all(self.__board.element(i, j) != self.EMPTY for i in range(self.board_height) for j in range(self.board_width))
    
    def generate_moves(self):
        '''
        Generates all the possible moves. For efficiency purposes, I only generate the moves around active cells.
        Also, I sort the moves by the distance from the last move.
        :return: a list of possible moves
        '''
        moves = []
        for i in range(self.board_height):
            for j in range(self.board_width):
                if self.__board.element(i, j) != self.EMPTY:
                    for ni, nj in self.get_neighbors(i, j):
                        if self.__board.element(ni, nj) == self.EMPTY:
                            moves.append((ni, nj))
                            
        most_recent_move = self.__board.last_move
        moves.sort(key=lambda move: abs(move[0] - most_recent_move[0]) + abs(move[1] - most_recent_move[1]))

        return moves
    
    def get_neighbors(self, i, j):
        '''
        Gets the neighbors of a cell.
        :param i: the row of the cell
        :param j: the column of the cell
        :return: a list of neighbors
        '''
        neighbors = []
        for ni in range(max(0, i - 1), min(self.board_height, i + 2)):
            for nj in range(max(0, j - 1), min(self.board_width, j + 2)):
                neighbors.append((ni, nj))
        return neighbors

    def is_winner(self, player, purpose = None):
        '''
        Checks if the player has won the game. If the purpose is 'minmax', it only checks if the player has won the game.
        If the purpose is None, it also sets the game_over attribute to True.
        :param player: the player to check
        :param purpose: the purpose of the check
        :return: True if the player has won the game, False otherwise
        '''
        for i in range(self.board_height):
            for j in range(self.board_width):
                if (
                    j + 4 < self.board_width and all(self.__board.element(i, j + k) == player for k in range(5)) or
                    i + 4 < self.board_height and all(self.__board.element(i + k, j) == player for k in range(5)) or
                    i + 4 < self.board_height and j + 4 < self.board_width and all(self.__board.element(i + k, j + k) == player for k in range(5)) or
                    i - 4 >= 0 and j + 4 < self.board_width and all(self.__board.element(i - k, j + k) == player for k in range(5))
                ):
                    if purpose == None:
                        self.__game_over = True
                    return True
        return False

    def computer_move(self, depth = 4):
        '''
        Makes a move for the computer player.
        :param depth: the depth of the search
        :return: the row and column of the move
        '''
        _, best_move = self.minimax(depth, self.COMPUTER, float('-inf'), float('inf'), True)
        
        if best_move:
            row, col = best_move
            return row, col

    def minimax(self, depth, player, alpha, beta, maximize=True):
        '''
        The minimax algorithm, with alpha-beta pruning.
        :param depth: the depth of the search
        :param player: the current player
        :param alpha: the alpha value
        :param beta: the beta value
        :param maximize: True if the current player is the maximizing player, False otherwise
        '''
        if depth == 0 or self.is_winner(self.PLAYER, 'minmax') or self.is_winner(self.COMPUTER, 'minmax') or self.is_board_full():
            return self.evaluate_position(), None

        moves = self.generate_moves()

        if player == self.COMPUTER:
            max_eval = float('-inf')
            best_move = None
            
            for move in moves:
                row, col = move
                
                self.__board.add_temp_move(row, col, self.COMPUTER)
                eval = self.minimax(depth - 1, self.PLAYER, alpha, beta, maximize = False)[0]
                self.__board.remove_move(row, col)
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, max_eval)
                
                if beta <= alpha:
                    break
                
            return max_eval, best_move
        
        else:
            min_eval = float('inf')
            best_move = None
            
            for move in moves:
                row, col = move
                
                self.__board.add_temp_move(row, col, self.PLAYER)
                eval = self.minimax(depth - 1, self.COMPUTER, alpha, beta, maximize = True)[0]
                self.__board.remove_move(row, col)
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                    
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
                
            return min_eval, best_move
    
    def evaluate_position(self):
        computer_score = self.evaluate_player_score(self.COMPUTER)
        player_score = self.evaluate_player_score(self.PLAYER)

        return computer_score - player_score

    def evaluate_player_score(self, player):
        score = 0
        last_row, last_col = self.__board.last_move

        for direction in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            player_score = self.evaluate_streak(last_row, last_col, player, direction)
            opponent_score = self.evaluate_streak(last_row, last_col, player ^ 1, direction)
            score += player_score - opponent_score

        return score

    def evaluate_streak(self, row, col, player, direction):
        consecutive_count = 0
        open_ends = 0

        for k in range(-4, 5):
            i, j = row + k * direction[0], col + k * direction[1]

            if 0 <= i < self.board_height and 0 <= j < self.board_width:
                if self.__board.element(i, j) == player:
                    consecutive_count += 1
                elif self.__board.element(i, j) == self.EMPTY:
                    open_ends += 1

        return self.calculate_streak_score(consecutive_count, open_ends, player)

    def calculate_streak_score(self, consecutive_count, open_ends, player):
        if consecutive_count == 4:
            return 100000 # Winning move
        elif consecutive_count == 3 and open_ends == 2:
            return 100000 # Also winning move
        elif consecutive_count == 3:
            return 5000 # Potential winning moves
        elif consecutive_count == 2 and open_ends == 2:
            return 500
        elif consecutive_count == 2 and open_ends == 1:
            return 50
        else:
            return 0

    def check_four_threat(self, row, col, player):
        '''
        Checks if there are 3 consecutive active cells for the player, in which case, it returns True.
        :param row: the row of the move
        :param col: the column of the move
        :param player: the player for which the move is made
        :return: True if there are 3 consecutive active cells for the player, False otherwise
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
        This is more efficient than letting the minmax search for the blocking move. As the game
        takes place on a 15x15 board, the minmax is not really ideal. The same goes for searching
        the winning move.
        :return: True if there is a move that the computer player has to block, None otherwise
        '''
        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.is_valid_move(row, col):
                    self.add_move(row, col, self.PLAYER)

                    if self.is_winner(self.PLAYER, 'minmax'):
                        self.remove_move(row, col)
                        return row, col

                    self.remove_move(row, col)

        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.is_valid_move(row, col):
                    self.add_temp_move(row, col, self.PLAYER)

                    if self.check_four_threat(row, col, self.PLAYER):
                        self.remove_move(row, col)
                        return row, col

                    self.remove_move(row, col)

        return None, None
    
    def search_winning_move(self):
        '''
        Checks if there is a winning move for the computer player.
        :return: True if there is a winning move, None otherwise
        '''
        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.is_valid_move(row, col):
                    self.add_temp_move(row, col, self.COMPUTER)
                    if self.is_winner(self.COMPUTER, 'minmax'):
                        return row, col
                    
                    self.remove_move(row, col)
        return None, None
    
    def add_move(self, row, col, player = -1):
        '''
        Adds a move to the board
        :param row: the row of the move
        :param col: the column of the move
        :param player: the player for which the move is made
        '''
        if player == -1:
            player = self.__player

        self.__board.add_move(row, col, player)
        
    def add_temp_move(self, row, col, player = -1):
        '''
        Adds a temporary move to the board
        :param row: the row of the move
        :param col: the column of the move
        :param player: the player for which the move is made
        '''
        if player == -1:
            player = self.__player

        self.__board.add_temp_move(row, col, player)
        
    def remove_move(self, row, col):
        '''
        Removes a move from the board
        :param row: the row of the move
        :param col: the column of the move
        '''
        if 0 <= row < self.board_height and 0 <= col < self.board_width:
            self.__board.remove_move(row, col)