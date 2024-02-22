import os
import re
import sys
from services.game import Game
from services.ai import AI
from tabulate import tabulate
from colorama import Fore

class UI:
    def __init__(self):
        self.__game = Game()
        self.__ai = AI()
        self.__is_ai = False
        self.__red_circle = "\033[91m\u2B24\033[0m"
        self.__blue_circle = "\033[94m\u2B24\033[0m"
        self.__input_pattern = re.compile(r'^\s*(\d+)\s*[, ]\s*(\d+)\s*$')
        # used regex for case insensitive matching
    
    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_welcome(self):
        self.clear_console()
        print("Welcome to Gomoku!")
        
    def print_options(self):
        print("1. Play against dumb computer.")
        print("2. Play against AI.")
        
    def print_invalid_option(self):
        self.clear_console()
        print("Please enter a valid option.")
        self.press_key()
    
    def print_invalid_indices(self):
        self.clear_console()
        print("It seems your indices are not valid! Please re-enter the indices!")
        self.press_key()
        if self.__is_ai:
            self.player_turn_ai()
        else:
            self.player_turn_computer()
        
    def print_winner(self):
        self.clear_console()
        if self.__is_ai:
            print(f"{Fore.GREEN}You won!" if self.__ai.player == 0 else f"{Fore.RED}The AI won!")
        else:
            print(f"{Fore.GREEN}You won!" if self.__game.player == 0 else f"{Fore.RED}The computer won!")
        self.press_key()
    
    def get_option(self):
        return input("Enter option: ")
    
    def press_key(self):
        input("\nPress enter to continue... ")
        self.clear_console()
            
    def player_turn_ai(self):
        self.clear_console()
        self.print_board(self.__ai.board)
        input_str = input(f"{Fore.GREEN}Your turn {self.__blue_circle}  Enter two integers (1-15, 1-15): ")
        match = self.__input_pattern.match(input_str)
        if match:
            row, column = map(int, match.groups())
            if self.__ai.is_valid_move(row - 1, column - 1):
                self.__ai.add_move(row - 1, column - 1, 0)
                self.__ai.is_winner(0)
            else:
                self.print_invalid_indices()
        else:
            self.print_invalid_indices()
        self.__ai.change_player()
    
    def player_turn_computer(self):
        self.clear_console()
        self.print_board()
        input_str = input(f"{Fore.GREEN}Your turn {self.__blue_circle}  Enter two integers (1-15, 1-15): ")
        match = self.__input_pattern.match(input_str)
        if match:
            row, column = map(int, match.groups())
            if self.__game.is_valid_move(row - 1, column - 1):
                self.__game.add_move(row - 1, column - 1)
                self.__game.is_winner(row - 1, column - 1, 0)
            else:
                self.print_invalid_indices()
        else:
            self.print_invalid_indices()
        self.__game.change_player()
        
    def computer_turn(self):
        self.clear_console()
        self.__game.make_computer_move()
        
        self.print_board(self.__game.board)
        print(f"The computer {self.__red_circle}  made it's turn!")
        self.press_key()
        
        if self.__game.game_over:
            return
        
        self.__game.change_player()
        
    def ai_turn(self):
        self.clear_console()
        row, column = self.__ai.computer_move()
        self.__ai.add_move(row, column, 1)
        self.__ai.is_winner(1)
        self.print_board(self.__ai.board)
        print(f"The AI {self.__red_circle}  made it's turn!")
        self.press_key()
        
        if self.__ai.game_over:
            return
        self.__ai.change_player()
        
    def print_board(self, board = None):
        if board is None:
            board = self.__game.board
        
        header = [f"{i + 1}" for i in range(self.__game.board_width)]
        padded_header = [f"{item:<2}" for item in header]

        table_data = []

        for i, row in enumerate(board):
            row_display = [f"{i + 1}"]
            row_display.extend([f"{self.__blue_circle}" if cell == 0 else f"{self.__red_circle}" if cell == 1 else ' ' for cell in row])
            table_data.append(row_display)

        print(tabulate(table_data, headers = padded_header, tablefmt = "pretty", numalign = "center"))
    
    def play_with_computer(self):
        while not self.__game.game_over:
            self.player_turn_computer()
            if not self.__game.game_over:
                self.computer_turn()
        self.print_winner()
        
    def play_with_ai(self):
        self.__is_ai = True
        while not self.__ai.game_over:
            self.player_turn_ai()
            if not self.__ai.game_over:
                self.ai_turn()
        self.print_winner()
    
    def run(self):
        self.print_welcome()
        self.press_key()
        self.print_options()
        
        option = self.get_option()
        
        if option == "1":
            self.play_with_computer()
        elif option == "2":
            self.play_with_ai()
        elif option == "3":
            sys.exit()
        else:
            self.print_invalid_option()
            self.run()