import pygame
from pygame.math import Vector2

from utils.constants import CELL_NUMBER, CELL_SIZE, DIRECTIONS

INITIAL_BODY_BLOCKS = 3


class Snake:
    __left_vector = Vector2(-1, 0)
    __right_vector = Vector2(1, 0)
    __up_vector = Vector2(0, -1)
    __down_vector = Vector2(0, 1)

    # Head parts
    __head_up = pygame.image.load("graphics/head_up.png")
    __head_down = pygame.image.load("graphics/head_down.png")
    __head_left = pygame.image.load("graphics/head_left.png")
    __head_right = pygame.image.load("graphics/head_right.png")

    # Tails parts
    __tail_up = pygame.image.load("graphics/tail_up.png")
    __tail_down = pygame.image.load("graphics/tail_down.png")
    __tail_left = pygame.image.load("graphics/tail_left.png")
    __tail_right = pygame.image.load("graphics/tail_right.png")

    # Body parts
    __body_vertical = pygame.image.load("graphics/body_vertical.png")
    __body_horizontal = pygame.image.load("graphics/body_horizontal.png")
    __body_tr = pygame.image.load("graphics/body_topright.png")
    __body_tl = pygame.image.load("graphics/body_topleft.png")
    __body_br = pygame.image.load("graphics/body_bottomright.png")
    __body_bl = pygame.image.load("graphics/body_bottomleft.png")

    def __init__(self):
        self.reset()
        self.__crunch_sound = pygame.mixer.Sound('audio/food.wav')
        self.__lose_sound = pygame.mixer.Sound('audio/lose.wav')

    def reset(self):
        self.body = [Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.__direction = Vector2(0, 0)

    def draw_snake(self, window):
        self.__update_head_graphic()
        self.__update_tail_graphic()
        self.__update_body_part_graphics(window)

    def move(self):
        if self.__direction != Vector2(0, 0):
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.__direction)
            self.body = body_copy[:]

    def change_direction(self, direction):
        if direction == DIRECTIONS["UP"] and self.__direction != self.__down_vector:
            self.__direction = self.__up_vector

        elif direction == DIRECTIONS["DOWN"] and self.__direction != self.__up_vector:
            self.__direction = self.__down_vector

        elif (
            direction == DIRECTIONS["RIGHT"] and self.__direction != self.__left_vector
        ):
            self.__direction = self.__right_vector

        elif (
            direction == DIRECTIONS["LEFT"] and self.__direction != self.__right_vector
        ):
            self.__direction = self.__left_vector
        

    def get_score(self):
        return str(len(self.body) - INITIAL_BODY_BLOCKS)

    def add_block(self):
        new_block = self.body[-1]
        self.body.insert(-1, new_block)

    def hits_wall(self):
        snake_head = self.body[0]
        is_snake_in_board_x = 0 <= int(snake_head.x) < CELL_NUMBER
        is_snake_in_board_y = 0 <= int(snake_head.y) < CELL_NUMBER

        return not is_snake_in_board_x or not is_snake_in_board_y

    def hits_itself(self):
        head, *body_parts = self.body[:]
        
        for block in body_parts:
            if block == head:
                return True
        return False

    def __update_head_graphic(self):
        head_movement = self.body[1] - self.body[0]

        if head_movement == self.__right_vector:
            self.__head_graphic = self.__head_left

        elif head_movement == self.__left_vector:
            self.__head_graphic = self.__head_right

        elif head_movement == self.__up_vector:
            self.__head_graphic = self.__head_down

        elif head_movement == self.__down_vector:
            self.__head_graphic = self.__head_up

    def __update_tail_graphic(self):
        tail_movement = self.body[-2] - self.body[-1]

        if tail_movement == self.__right_vector:
            self.__tail_graphic = self.__tail_left

        elif tail_movement == self.__left_vector:
            self.__tail_graphic = self.__tail_right

        elif tail_movement == self.__up_vector:
            self.__tail_graphic = self.__tail_down

        elif tail_movement == self.__down_vector:
            self.__tail_graphic = self.__tail_up

    def __update_body_part_graphics(self, window):
        for index, block in enumerate(self.body):
            rect_x_pos, rect_y_pos = block.x * CELL_SIZE, block.y * CELL_SIZE
            block_rect = pygame.Rect(rect_x_pos, rect_y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:
                # Head of snake
                window.blit(self.__head_graphic, block_rect)
            elif index == len(self.body) - 1:
                window.blit(self.__tail_graphic, block_rect)
            else:
                prev_block_move_vector = self.body[index + 1] - block
                next_block_move_vector = self.body[index - 1] - block

                if prev_block_move_vector.x == next_block_move_vector.x:
                    window.blit(self.__body_vertical, block_rect)

                elif prev_block_move_vector.y == next_block_move_vector.y:
                    window.blit(self.__body_horizontal, block_rect)

                else:
                    if (
                        prev_block_move_vector.x == -1
                        and next_block_move_vector.y == -1
                    ) or (
                        prev_block_move_vector.y == -1
                        and next_block_move_vector.x == -1
                    ):
                        window.blit(self.__body_tl, block_rect)
                    if (
                        prev_block_move_vector.x == -1 and next_block_move_vector.y == 1
                    ) or (
                        prev_block_move_vector.y == 1 and next_block_move_vector.x == -1
                    ):
                        window.blit(self.__body_bl, block_rect)
                    if (
                        prev_block_move_vector.x == 1 and next_block_move_vector.y == -1
                    ) or (
                        prev_block_move_vector.y == -1 and next_block_move_vector.x == 1
                    ):
                        window.blit(self.__body_tr, block_rect)
                    if (
                        prev_block_move_vector.x == 1 and next_block_move_vector.y == 1
                    ) or (
                        prev_block_move_vector.y == 1 and next_block_move_vector.x == 1
                    ):
                        window.blit(self.__body_br, block_rect)

    def play_lose_sound(self):
        self.__lose_sound.play()

    def play_eat_food_sound(self):
        self.__crunch_sound.play()