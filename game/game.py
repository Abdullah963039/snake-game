import pygame
from game.fruit import Fruit, apple_image
from game.snake import Snake
from utils.constants import (
    CELL_NUMBER,
    CELL_SIZE,
    DIRECTIONS,
    FONT_COLOR,
    GRASS_COLOR,
    SCORE_BG_COLOR,
    SCREEN_HIGHT,
    SCREEN_WIDTH,
    BACKGROUND_COLOR,
)


pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

SCORE_FONT = pygame.font.Font(None, 40)
HEADING_FONT = pygame.font.Font(None, 80)
FPS = 60
SCREEN_UPDATE = pygame.USEREVENT


class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))

    def start_game(self):
        game_loop = True

        pygame.display.set_caption("Snake Game")
        clock = pygame.time.Clock()
        pygame.time.set_timer(SCREEN_UPDATE, 200)

        while game_loop:
            clock.tick(FPS)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_loop = False
                if event.type == SCREEN_UPDATE:
                    self.__update()
                if event.type == pygame.KEYDOWN:
                    self.__handle_snake_move(event.key)

            self.screen.fill(BACKGROUND_COLOR)
            self.__render_game()

        pygame.quit()

    def __render_game(self):
        self.__draw_grass()
        self.__draw_score()
        self.fruit.draw_food(self.screen)
        self.snake.draw_snake(self.screen)

    def __update(self):
        self.snake.move()
        self.__check_collision()
        self.__check_lose()

    def __handle_snake_move(self, key):
        if key == pygame.K_UP:
            self.snake.change_direction(DIRECTIONS["UP"])
        if key == pygame.K_DOWN:
            self.snake.change_direction(DIRECTIONS["DOWN"])
        if key == pygame.K_LEFT:
            self.snake.change_direction(DIRECTIONS["LEFT"])
        if key == pygame.K_RIGHT:
            self.snake.change_direction(DIRECTIONS["RIGHT"])

    def __check_collision(self):
        if self.fruit.position == self.snake.body[0]:
            self.fruit.randomize_position()
            self.snake.add_block()
            self.snake.play_eat_food_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.position:
                self.fruit.randomize_position()

    def __check_lose(self):
        # Check if snake hits the edges or hit itself
        if self.snake.hits_wall() or self.snake.hits_itself():
            self.__game_over()

    def __draw_grass(self):
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE
                        )
                        pygame.draw.rect(self.screen, GRASS_COLOR, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE
                        )
                        pygame.draw.rect(self.screen, GRASS_COLOR, grass_rect)

    def __draw_score(self):
        score_text = self.snake.get_score()
        score_surface = SCORE_FONT.render(score_text, True, FONT_COLOR)

        score_x = (CELL_SIZE * CELL_NUMBER) - 40
        score_y = (CELL_SIZE * CELL_NUMBER) - 40
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        apple_rect = apple_image.get_rect(
            midright=(score_rect.left, score_rect.centery)
        )
        bg_rect = pygame.Rect(
            apple_rect.left,
            apple_rect.top,
            apple_rect.width + score_rect.width + 10,
            apple_rect.height,
        )

        pygame.draw.rect(self.screen, SCORE_BG_COLOR, bg_rect)
        self.screen.blit(score_surface, score_rect)
        self.screen.blit(apple_image, apple_rect)
        pygame.draw.rect(self.screen, FONT_COLOR, bg_rect, 2)

    def __game_over(self):
        self.snake.reset()
        self.snake.play_lose_sound()
