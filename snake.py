import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_green = (0, 180, 0)
yellow = (255, 255, 0)
eye_white = (255, 255, 255)


dis_width = 800
dis_height = 600


dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()
snake_block = 20
snake_speed = 9


font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)



def your_score(score):
    value = score_font.render("Ваш счет: " + str(score), True, black)
    dis.blit(value, [0, 0])



def our_snake(snake_block, snake_list, x1_change, y1_change):
    for i, segment in enumerate(snake_list):
        if i % 2 == 0:
            segment_color = green
        else:
            segment_color = dark_green

        pygame.draw.rect(dis, segment_color,
                         [segment[0], segment[1], snake_block, snake_block])
        if i == len(snake_list) - 1:
            draw_eyes(segment[0], segment[1], snake_block, x1_change, y1_change)


def draw_eyes(x, y, block_size, x_change, y_change):
    eye_size = block_size // 4
    pupil_size = eye_size // 2
    if x_change > 0:
        left_eye_pos = (x + block_size * 3 // 4, y + block_size // 4)
        right_eye_pos = (x + block_size * 3 // 4, y + block_size * 3 // 4)
        pupil_offset = eye_size // 3
    elif x_change < 0:
        left_eye_pos = (x + block_size // 4, y + block_size // 4)
        right_eye_pos = (x + block_size // 4, y + block_size * 3 // 4)
        pupil_offset = -eye_size // 3
    elif y_change > 0:
        left_eye_pos = (x + block_size // 4, y + block_size * 3 // 4)
        right_eye_pos = (x + block_size * 3 // 4, y + block_size * 3 // 4)
        pupil_offset = eye_size // 3
    else:
        left_eye_pos = (x + block_size // 4, y + block_size // 4)
        right_eye_pos = (x + block_size * 3 // 4, y + block_size // 4)
        pupil_offset = -eye_size // 3

    pygame.draw.circle(dis, eye_white, left_eye_pos, eye_size)
    pygame.draw.circle(dis, eye_white, right_eye_pos, eye_size)

    pygame.draw.circle(dis, black,
                       (left_eye_pos[0] + pupil_offset, left_eye_pos[1]), pupil_size)
    pygame.draw.circle(dis, black,
                       (right_eye_pos[0] + pupil_offset, right_eye_pos[1]), pupil_size)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    while not game_over:
        while game_close:
            dis.fill(white)
            message("Вы проиграли! Нажмите Q-выход или C-играть снова", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change <= 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change >= 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change <= 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change >= 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(white)

        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, (255, 100, 100), [foodx + 2, foody + 2, snake_block - 4, snake_block - 4])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List, x1_change, y1_change)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()