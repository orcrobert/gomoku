import pygame

class Button:
    def __init__(self, x, y, width, height, color, text = '', text_color = (255, 255, 255)):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__color = color
        self.__text = text
        self.__text_color = text_color

    @property
    def x(self):
        return self.__x

    @property
    def width(self):
        return self.__width
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.__color, (self.__x, self.__y, self.__width, self.__height), 0, 5)
        if self.__text != '':
            font = pygame.font.SysFont(None, 30)
            text = font.render(self.__text, 1, self.__text_color)
            screen.blit(text, (self.__x + (self.__width / 2 - text.get_width() / 2), self.__y + (self.__height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.__x < pos[0] < self.__x + self.__width:
            if self.__y < pos[1] < self.__y + self.__height:
                return True
        return False