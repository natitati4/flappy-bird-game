import random
import math

import pygame as pg
import sys
import pygame.display
from text_rendering import text_rendering


framepersecond_clock = pygame.time.Clock()

pg.init()

WIDTH = 900
HEIGHT = 501

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MARGARITA_YELLOW = (176, 194, 74)
POMPADOUR_PURPLE = (106, 31, 68)

SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.set_caption('fb game')

# load images
bg_img = pg.image.load("images\\bg.png").convert()
player_img = pg.image.load("images\\flappy_bird_img.png").convert_alpha()
up_pipe_img = pg.image.load("images\\up_pipe_img.png").convert_alpha()
down_pipe_img = pg.image.load("images\\down_pipe_img.png").convert_alpha()

# blit bg and player

pg.display.flip()


def start_screen():

    # background and title
    SCREEN.blit(bg_img, (0, 0))
    SCREEN.blit(player_img, (WIDTH // 2 - 100, HEIGHT // 2 - 70))

    # title
    title_text_x, title_text_y = WIDTH // 2, 100
    text_rendering.draw_all_text(title_text_x, title_text_y, "Flappy Bird", BLACK, WHITE, 80, "Cooper Black", SCREEN, "center")

    # Press any key
    text_x, text_y = WIDTH // 2, 400
    text_rendering.draw_all_text(text_x, text_y, "Press any key to start", BLACK, WHITE, 35, "Cooper Black", SCREEN, "center")

    pygame.display.flip()


def end_screen(up_pipes, down_pipes, player_x, player_y, rotated, score):
    # blit everything except score at top left...
    SCREEN.blit(bg_img, (0, 0))

    # blit up pipes
    for pipe in up_pipes:
        SCREEN.blit(up_pipe_img, (pipe["x"], pipe["y"]))

    # blit down pipes
    for pipe in down_pipes:
        SCREEN.blit(down_pipe_img, (pipe["x"], pipe["y"]))

    # blit player
    SCREEN.blit(rotated, (player_x, player_y))

    # title
    title_text_x, title_text_y = WIDTH // 2, HEIGHT // 8
    text_rendering.draw_all_text(title_text_x, title_text_y, "Game over!", BLACK, WHITE, 100, "Cooper Black", SCREEN, "center")

    # score
    title_text_x, title_text_y = WIDTH // 2, HEIGHT // 2
    text_rendering.draw_all_text(title_text_x, title_text_y, f"Final score: {score}",
                                 POMPADOUR_PURPLE, MARGARITA_YELLOW, 60, "Cooper Black", SCREEN, "center")

    # Press any key
    text_x, text_y = WIDTH // 2, 400
    text_rendering.draw_all_text(text_x, text_y, "Press any key to play again", BLACK, WHITE, 35, "Cooper Black", SCREEN, "center")

    pygame.display.flip()


def blit_everything(up_pipes, down_pipes, player_x, player_y, rotated, score):
    SCREEN.blit(bg_img, (0, 0))

    # blit up pipes
    for pipe in up_pipes:
        SCREEN.blit(up_pipe_img, (pipe["x"], pipe["y"]))

    # blit down pipes
    for pipe in down_pipes:
        SCREEN.blit(down_pipe_img, (pipe["x"], pipe["y"]))

    # blit player
    SCREEN.blit(rotated, (player_x, player_y))

    text_rendering.draw_all_text(10, 0, f"Score: {score}", POMPADOUR_PURPLE, MARGARITA_YELLOW, 35, "Cooper Black", SCREEN)

    pygame.display.flip()


def create_pipe():
    difference_between_pipes = 180  # space between up and down pipes
    up_pipe_height = up_pipe_img.get_height()  # height of up pipe
    y_of_up_pipe = random.randrange(-up_pipe_height, HEIGHT - difference_between_pipes - up_pipe_height)  # y of the up, between top of screen and 200 before bottom.
    y_of_down_pipe = y_of_up_pipe + up_pipe_height + difference_between_pipes  # y of down is y of up + height of up + space between them

    x_of_pipes = WIDTH + 10  # generate outside of right of screen

    whole_pipe = [
        [x_of_pipes, y_of_up_pipe],  # upper pipe
        [x_of_pipes, y_of_down_pipe]  # lower pipe
    ]

    return whole_pipe


def add_score(bird_x, pipe_x):
    if pipe_x + up_pipe_img.get_width() <= bird_x <= pipe_x + up_pipe_img.get_width() + 2:
        return True


def game_over(bird_x, bird_y, pipe_x, down_pipe_y, up_pipe_y):
    # check if bird in range of the pipe
    if pipe_x <= bird_x - 5 <= pipe_x + up_pipe_img.get_width() or pipe_x <= bird_x + player_img.get_width() + 5 <= pipe_x + up_pipe_img.get_width():
        if bird_y + 10 <= up_pipe_y + up_pipe_img.get_height() or down_pipe_y <= bird_y + player_img.get_height() - 5:
            return True
    return False


def flappy_game():
    score = 0

    # move bird back to starting state
    global player_img
    player_img = pg.transform.scale(player_img, (57.25, 40))

    # redraw bg
    SCREEN.blit(bg_img, (0, 0))

    # initialize player
    player_x = 325
    player_y = 200

    bird_velocity_y = 0  # bird velocity
    bird_acceleration_y = 0.9  # bird acceleration (gravity)

    # velocity while flapping
    bird_flap_velocity = -10  # velocity when bird flappes

    # true only when the bird is flapping
    bird_flapped = False

    first_pipe = create_pipe()
    second_pipe = create_pipe()

    # just difference between pipes on X axis, achieved by trial and failure
    difference_between_pipes_x = WIDTH // 2 + up_pipe_img.get_width() // 2

    # make difference between pipes in x axis
    second_pipe[0][0] += difference_between_pipes_x
    second_pipe[1][0] += difference_between_pipes_x

    up_pipes = [{"x": first_pipe[0][0], "y": first_pipe[0][1]}, {"x": second_pipe[0][0], "y": second_pipe[0][1]}]
    down_pipes = [{"x": first_pipe[1][0], "y": first_pipe[1][1]}, {"x": second_pipe[1][0], "y": second_pipe[1][1]}]

    pipe_moving_velocity = -4

    while True:

        # Handling the key pressing events
        for ev in pg.event.get():

            if ev.type == pg.QUIT:
                pygame.quit()
                sys.exit()

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if ev.key == pygame.K_SPACE:
                    # if the player's y is above 0 when he presses flap., he is in screen, do stuff.
                    # -20 and not 0 cause the actual bird image starts at about 20...
                    if player_y > -20:
                        bird_velocity_y = bird_flap_velocity
                        bird_flapped = True

        # bird falling - the velocity increases by 1 (every second?)
        if not bird_flapped:
            bird_velocity_y += bird_acceleration_y

        # reset bird flapped
        if bird_flapped:
            bird_flapped = False

        # only continue game if player not touched ground. if player touches ground, stop the game

        if player_y + player_img.get_height() < HEIGHT:
            player_y = player_y + bird_velocity_y
        else:
            player_y = HEIGHT - player_img.get_height()
            end_screen(up_pipes, down_pipes, player_x, player_y, rotated_img, score)
            return

        # if the player is about to go out of the top, move him back to the top.
        if player_y < 0:
            player_y = 0

        # moving up pipes left
        for pipe in up_pipes:
            pipe["x"] += pipe_moving_velocity

        # moving down pipes left
        for pipe in down_pipes:
            pipe["x"] += pipe_moving_velocity

        rotated_img = pygame.transform.rotate(player_img, math.degrees(-math.atan(bird_velocity_y)) * 0.5)

        if add_score(player_x, up_pipes[0]["x"]):
            score += 1

        # if left pipe is just out of screen, remove it and create new pipe
        if up_pipes[0]["x"] < -up_pipe_img.get_width():

            del up_pipes[0]
            del down_pipes[0]

            new_pipe = create_pipe()

            # pipe is a dict
            up_pipes.append({"x": new_pipe[0][0], "y": new_pipe[0][1]})
            down_pipes.append({"x": new_pipe[1][0], "y": new_pipe[1][1]})

        # draw everything
        blit_everything(up_pipes, down_pipes, player_x, player_y, rotated_img, score)

        if game_over(player_x, player_y, up_pipes[0]["x"], down_pipes[0]["y"], up_pipes[0]["y"]):
            end_screen(up_pipes, down_pipes, player_x, player_y, rotated_img, score)
            return

        framepersecond_clock.tick(40)


running = True
while running:

    start_screen()

    while True:
        for event in pg.event.get():

            # if user clicks on X or presses esc, close the game
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                # Exit the program
                sys.exit()

            elif event.type == pg.KEYDOWN:
                flappy_game()

# deactivates the pygame library
pg.quit()
