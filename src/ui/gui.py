from services.game import Game
from ui.components.button import Button
import sys
import pygame
import pygame.gfxdraw # for drawing anti-aliased shapes
from services.ai import AI

class GUI:
    def __init__(self):
        self.__game = Game()
        self.__ai = AI()
        self.BACKGROUND_IMAGE = pygame.image.load("../src/static/images/background.jpeg")
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (200, 0, 0)
        self.BLUE = (0, 0, 200)
        self.CELL_SIZE = 40
        self.BOARD_SIZE = 15
        self.play_ai_button = None
        self.play_computer_button = None
        self.__version = "computer"
        self.WIDTH, self.HEIGHT = self.CELL_SIZE * (self.BOARD_SIZE), self.CELL_SIZE * (self.BOARD_SIZE)
        self.window_size = (700, 700)
        self.__screen = pygame.display.set_mode(self.window_size)
        self.board_pos = ((self.window_size[0] - self.WIDTH) // 2, (self.window_size[1] - self.HEIGHT) // 2)
        self.init_window()
    
    def init_window(self):
        pygame.init()
        pygame.display.set_caption("Gomoku")
        self.clear_screen()
        pygame.display.update()
        
    def clear_screen(self):
        self.__screen.blit(self.BACKGROUND_IMAGE, (-100, -100))

    def display_board(self):
        self.clear_screen()
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                pygame.draw.rect(
                                self.__screen, 
                                self.WHITE, 
                                (
                                    self.board_pos[0] + col * self.CELL_SIZE, 
                                    self.board_pos[1] + row * self.CELL_SIZE, 
                                    self.CELL_SIZE, 
                                    self.CELL_SIZE
                                ), 
                                1
                                )

        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.__version == "computer":
                    if self.__game.board[row][col] == 0:
                        pygame.gfxdraw.filled_circle(
                                                    self.__screen, 
                                                    self.board_pos[0] + col * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                    self.board_pos[1] + row * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                    self.CELL_SIZE // 2 - 2, 
                                                    self.RED
                                                    )
                        pygame.gfxdraw.aacircle(
                                                    self.__screen, 
                                                    self.board_pos[0] + col * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                    self.board_pos[1] + row * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                    self.CELL_SIZE // 2 - 2, 
                                                    self.RED
                                                )
                    elif self.__game.board[row][col] == 1:
                        pygame.gfxdraw.filled_circle(
                                                    self.__screen, 
                                                    self.board_pos[0] + col * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                    self.board_pos[1] + row * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                    self.CELL_SIZE // 2 - 2, 
                                                    self.BLUE
                                                    )
                        pygame.gfxdraw.aacircle(
                                                self.__screen, 
                                                self.board_pos[0] + col * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                self.board_pos[1] + row * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                self.CELL_SIZE // 2 - 2, 
                                                self.BLUE
                                                )
                        
                else:
                    if self.__ai.board[row][col] == 0:
                        pygame.gfxdraw.filled_circle(
                                                self.__screen, 
                                                self.board_pos[0] + col * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                self.board_pos[1] + row * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                self.CELL_SIZE // 2 - 2, 
                                                self.RED)
                        pygame.gfxdraw.aacircle(
                                                self.__screen, 
                                                self.board_pos[0] + col * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                self.board_pos[1] + row * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                self.CELL_SIZE // 2 - 2, 
                                                self.RED
                                                )
                    elif self.__ai.board[row][col] == 1:
                        pygame.gfxdraw.filled_circle(
                                                    self.__screen, 
                                                     self.board_pos[0] + col * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                     self.board_pos[1] + row * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                     self.CELL_SIZE // 2 - 2, self.BLUE
                                                    )
                        pygame.gfxdraw.aacircle(
                                                self.__screen, 
                                                self.board_pos[0] + col * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                self.board_pos[1] + row * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                self.CELL_SIZE // 2 - 2, self.BLUE
                                                )
                        
        pygame.display.flip()
        
    def display_start_menu(self):
        font = pygame.font.Font(None, 40)
        self.clear_screen()
        self.__game = Game()
        self.__ai = AI()

        welcome_text = font.render('Welcome to Gomoku', True, self.WHITE)
        play_computer_text = font.render('Play against Computer', True, self.WHITE)
        play_ai_text = font.render('Play against AI', True, self.WHITE)

        welcome_text_pos = ((self.window_size[0] - welcome_text.get_width()) // 2, 50)
        button_width = max(play_computer_text.get_width(), play_ai_text.get_width()) + 20
        button_height = 60
        play_computer_button_pos = ((self.window_size[0] - button_width) // 2, 200)
        play_ai_button_pos = ((self.window_size[0] - button_width) // 2, 300)

        self.play_computer_button = Button(
                                            play_computer_button_pos[0], 
                                            play_computer_button_pos[1], 
                                            button_width, 
                                            button_height, 
                                            self.RED, 
                                            'Play with Computer'
                                            )
        self.play_ai_button = Button(
                                    play_ai_button_pos[0], 
                                    play_ai_button_pos[1], 
                                    button_width, 
                                    button_height, 
                                    self.RED, 
                                    'Play with AI'
                                    )

        self.__screen.blit(welcome_text, welcome_text_pos)
        self.play_computer_button.draw(self.__screen)
        self.play_ai_button.draw(self.__screen)

        pygame.display.flip()
        
    def display_winner(self):
        rect_width = 300
        rect_height = 250
        rect_x = (self.window_size[0] - rect_width) // 2
        rect_y = (self.window_size[1] - rect_height) // 2

        pygame.draw.rect(self.__screen, self.BLACK, (rect_x, rect_y, rect_width, rect_height))

        font = pygame.font.Font(None, 50)
        if self.__version == "computer":
            text_surface = font.render("You won!" if self.__game.player == 0
                                        else "Computer won!", 
                                        True, 
                                        self.WHITE
                                        )
        elif self.__version == "ai":
            text_surface = font.render("You won!" if self.__ai.player == 0
                                        else "AI won!", 
                                        True, 
                                        self.WHITE
                                        )

        text_rect = text_surface.get_rect()
        text_rect.center = (rect_x + rect_width // 2, rect_y + 80)

        self.__screen.blit(text_surface, text_rect)
        
        button_width = 100
        button_height = 50
        button_space = 20
        total_button_width = 2 * button_width + button_space

        exit_button = Button(
                            rect_x + (rect_width - total_button_width) // 2, 
                            rect_y + 150, button_width, 
                            button_height, 
                            self.RED, 
                            'Exit', 
                            self.WHITE
                            )
        
        menu_button = Button(
                            exit_button.x + button_width + button_space, 
                            rect_y + 150, 
                            button_width, 
                            button_height, 
                            self.BLUE, 
                            'Menu', 
                            self.WHITE
                            )

        exit_button.draw(self.__screen)
        menu_button.draw(self.__screen)
        
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.is_over(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif menu_button.is_over(event.pos):
                        self.display_start_menu()
                        return
            
    def get_clicked_cell(self, pos):
        row = pos[1] // self.CELL_SIZE - 1
        col = pos[0] // self.CELL_SIZE - 1
        return row, col
    
    def play_with_computer(self):
        self.__version = "computer"
        self.display_board()
        
        while not self.__game.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_cell(pos)
                    if self.__game.is_valid_move(row, col):
                        self.__game.add_move(row, col)
                        if not self.__game.is_winner(row, col, 0):
                            self.__game.change_player()
                        self.display_board()
                        if not self.__game.game_over:
                            self.__game.make_computer_move()
                            if not self.__game.game_over:
                                self.__game.change_player()
                            else:
                                self.__game.player = 1
                        self.display_board()
        self.display_winner()
        
    def play_with_ai(self):
        self.__version = "ai"
        self.display_board()
        
        while not self.__ai.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_cell(pos)
                    if self.__ai.is_valid_move(row, col):
                        self.__ai.add_move(row, col, 0)
                        if not self.__ai.is_winner(0):
                            self.__ai.change_player()
                        self.display_board()
                        if not self.__ai.game_over:
                            row, col = self.__ai.search_winning_move()
                            if row is None or col is None:
                                row, col = self.__ai.search_blocking_move()
                                if row is None or col is None:
                                    row, col = self.__ai.computer_move()
                            self.__ai.add_move(row, col, 1)
                            if not self.__ai.is_winner(1):
                                self.__ai.change_player()
                            self.display_board()
        self.display_winner()
    
    def run(self):
        self.display_start_menu()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.play_computer_button.is_over(mouse_pos):
                        self.play_with_computer()
                    elif self.play_ai_button.is_over(mouse_pos):
                        self.play_with_ai()