"""
CPSC 386-01
Programmed by Dayton Schuh

Author notes:
    o- Classes would clean up the code
    o-
"""

import pygame
from pygame import *
import random
import sys

# initialize
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()

# screen size
WIDTH = 1600
HEIGHT = 800

# global variables
PLAYER_MOVERATE = 8
COMPUTER_MOVERATE = 5

# lists for randomizing
speed_list = [-10, 10]
angle_list = [-5, -3, 0, 3, 5]
angle_list_bot = [1, 3, 5]
angle_list_top = [-5, -3,  -1]
BALL_SPEED = random.choice(speed_list)
BALL_ANGLE = random.choice(angle_list)

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# input keys
LEFT_KEY = [K_LEFT]
RIGHT_KEY = [K_RIGHT]
UP_KEY = [K_UP]
DOWN_KEY = [K_DOWN]

# load up sounds
ping = pygame.mixer.Sound("ping.wav")
player_scored = pygame.mixer.Sound("player_scored.wav")
computer_scored = pygame.mixer.Sound("computer_scored.wav")
round_over = pygame.mixer.Sound("round_over.wav")
game_over = pygame.mixer.Sound("game_over.wav")

pygame.mixer.music.load("summer.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

'''****************************************************************
function:
    terminate()

description:
    When called, this function closes the application.
    
TODO:
    None.
****************************************************************'''


def terminate():
    pygame.quit()
    sys.exit()


'''****************************************************************
function:
    wait_for_player_to_press_key()

description:
    When called, this function waits for any user input before
    returning true. If the escape key is pressed, it exits the
    application.

TODO:
    None.
****************************************************************'''


def wait_for_player_to_press_key():
    pressed = False
    while not pressed:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    terminate()
                return  # start game for any other key down


'''****************************************************************
function:
    draw_text()

description:
    This function takes a string, font type, screen display,
    and coordinates to print some text on the screen.

TODO:
    None.
****************************************************************'''


def draw_text(text, font1, surface, x, y):
    text_obj = font1.render(text, 1, WHITE)
    text_rect = text_obj.get_rect()
    text_rect.topleft = x, y
    surface.blit(text_obj, text_rect)


'''****************************************************************
function:
    ball_hits_paddle()

description:
    This function takes the ball and all paddles as parameters. It
    then checks if the ball has collided with any of the generated
    collision rectangles. If there is a collision, it returns true
    -- else it returns false.

TODO:
    None.
****************************************************************'''


def ball_hits_paddle(ball, player_rect_side, player_rect_top, player_rect_bot,
                     computer_rect_side, computer_rect_top, computer_rect_bot):
    if ball.colliderect(player_rect_side) or ball.colliderect(player_rect_top)\
            or ball.colliderect(player_rect_bot) or ball.colliderect(computer_rect_side)\
            or ball.colliderect(computer_rect_top) or ball.colliderect(computer_rect_bot):
        return True
    else:
        return False


'''****************************************************************
function:
    ball_went_out()

description:
    This function uses the ball's coordinates to check if the ball
    is still in the boundary.

TODO:
    None.
****************************************************************'''


def ball_went_out(horizontal, vertical):
    if horizontal < 0 or horizontal > WIDTH:
        return True
    elif vertical < 0 or vertical > HEIGHT:
        return True
    else:
        return False


'''****************************************************************
function:
    reset_ball()

description:
    Simply changes the ball's position to the middle of the screen.
    (used in conjunction with ball_went_out() -- alternatively, we
    can throw this simple code into ball_went_out)

TODO:
    None.
****************************************************************'''


def reset_ball(ball):
    ball.x = WIDTH/2
    ball.y = HEIGHT/2


'''****************************************************************
function:
    get_rect()

description:
    When called, this function creates a rectangle object from the
    pygame library.

TODO:
    None.
****************************************************************'''


def get_rect(self):
    return pygame.Rect(self.x, self.y, self.width, self.height)


'''****************************************************************
function:
    render_round_wins()

description:
    This function draws a visual indication for the user to see
    how many rounds have been won or lost. 

TODO:
    None.
****************************************************************'''


def render_round_wins(surf, play_win, comp_win, horz):

    for x in range(play_win):
        pygame.draw.circle(surf, WHITE, (horz, 50), 10)
        pygame.draw.circle(surf, BLUE, (horz, 50), 8)
        horz += 20

    for y in range(comp_win):
        pygame.draw.circle(surf, WHITE, (horz, 50), 10)
        pygame.draw.circle(surf, RED, (horz, 50), 8)
        horz += 20


'''****************************************************************
function:
    play()

description:
    This is where the magic happens.

TODO:
    None.
****************************************************************'''


def play():
    global BALL_SPEED, BALL_ANGLE

    pygame.init()
    main_clock = pygame.time.Clock()
    surf = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pong No Walls')
    pygame.mouse.set_visible(False)

    font1 = pygame.font.Font(None, 48)

    # load in all images
    ball_image = pygame.image.load('ball.png')
    player_image = pygame.image.load('player_paddle.png')
    player_image2 = pygame.image.load('player_paddle2.png')
    computer_image = pygame.image.load('computer_paddle.png')
    computer_image2 = pygame.image.load('computer_paddle2.png')

    # create objects
    player_rect_side = player_image.get_rect()
    player_rect_top = player_image2.get_rect()
    player_rect_bot = player_image2.get_rect()
    computer_rect_side = computer_image.get_rect()      # I wish I could've created sprite masks for pixel perfect
    computer_rect_top = computer_image2.get_rect()      # collision between all the objects. I just couldn't get it
    computer_rect_bot = computer_image2.get_rect()      # to work.
    ball = ball_image.get_rect()

    # start screen
    surf.fill(BLACK)
    draw_text('Pong No Walls', font1, surf, WIDTH / 2 - 100, HEIGHT / 3 + 50)
    draw_text('Press any key to start.', font1, surf, WIDTH / 2 - 150, HEIGHT / 2)
    pygame.display.update()
    wait_for_player_to_press_key()

    play_game_again = True
    while play_game_again:
        player_score = 0
        computer_score = 0
        play_win = 0
        comp_win = 0
        rnd = 1
        horz = 760

        # initial starting points
        player_rect_side.center = WIDTH, HEIGHT/2
        player_rect_top.center = WIDTH/4 + WIDTH/2, HEIGHT
        player_rect_bot.center = WIDTH/4 + WIDTH/2, 0
        computer_rect_side.center = 0, HEIGHT/2
        computer_rect_top.center = WIDTH/4, HEIGHT
        computer_rect_bot.center = WIDTH/4, 0
        ball.center = WIDTH/2, HEIGHT/2

        # player isn't moving
        move_left = move_right = move_up = move_down = False

        play_game = True
        while play_game:
            for e in pygame.event.get():
                if e.type == QUIT:
                    terminate()

                if e.type == KEYDOWN:

                    move_left = e.key in LEFT_KEY
                    move_right = e.key in RIGHT_KEY
                    move_up = e.key in UP_KEY
                    move_down = e.key in DOWN_KEY

                if e.type == KEYUP:
                    if e.key == K_ESCAPE:
                        terminate()

                    # i think this is what causes a little bit of clunky movement
                    move_left = move_right = move_up = move_down = False

            # controls for player movement (unnaturally clunky)
            if move_up and player_rect_side.top > 0:
                player_rect_side.centery -= PLAYER_MOVERATE
            if move_down and player_rect_side.bottom < HEIGHT:
                player_rect_side.centery += PLAYER_MOVERATE
            if move_left and player_rect_top.left > WIDTH/2 - 1:
                player_rect_top.centerx -= PLAYER_MOVERATE
                player_rect_bot.centerx -= PLAYER_MOVERATE
            if move_right and player_rect_top.right < WIDTH:
                player_rect_top.centerx += PLAYER_MOVERATE
                player_rect_bot.centerx += PLAYER_MOVERATE

            # This is the AI
            # if the ball is on computer side, move paddles
            if ball.centerx < WIDTH/2:
                # if the ball passes the paired paddles, move
                if ball.x < computer_rect_top.left:
                    computer_rect_bot.left -= COMPUTER_MOVERATE
                    computer_rect_top.left -= COMPUTER_MOVERATE
                if ball.x > computer_rect_top.right:
                    computer_rect_top.right += COMPUTER_MOVERATE
                    computer_rect_bot.right += COMPUTER_MOVERATE

                # if the ball is above / below the paddle, move
                if ball.centery > computer_rect_side.bottom < HEIGHT:
                    computer_rect_side.centery += COMPUTER_MOVERATE
                elif ball.centery < computer_rect_side.top > 0:
                    computer_rect_side.centery -= COMPUTER_MOVERATE

            # create black background
            surf.fill(BLACK)

            # draw scores to screen
            draw_text(str(player_score), font1, surf, WIDTH/2 + 35, 0)
            draw_text(str(computer_score), font1, surf, WIDTH/2 - 50, 0)

            # we can probably use a class to create all paddles
            surf.blit(player_image, player_rect_side)
            surf.blit(player_image2, player_rect_bot)
            surf.blit(player_image2, player_rect_top)
            surf.blit(computer_image, computer_rect_side)
            surf.blit(computer_image2, computer_rect_bot)
            surf.blit(computer_image2, computer_rect_top)

            # extra fluff for circles in center
            pygame.draw.circle(surf, WHITE, (800, 400), 100)    # unexpected float when using WIDTH / 2 or
            pygame.draw.circle(surf, BLACK, (800, 400), 98)     # HEIGHT / 2, so we're just setting it to a point

            # draw the center line
            for x in range(100):
                # pygame.draw.line(..., ..., (x, y) starting point, (x, y) ending point, ...)
                # if we update start and end point, we can create dashes
                # this current line just creates a dotted line, but serves its purpose
                pygame.draw.line(surf, WHITE, (WIDTH/2, x*10), (WIDTH/2, x*10), 2)

            # ball comes last, because we want it on top of the other stuff
            surf.blit(ball_image, ball)

            ball.x += BALL_SPEED
            ball.y += BALL_ANGLE

            if ball.colliderect(player_rect_side) or ball.colliderect(computer_rect_side):
                # we can use channels to play different sounds on top of one another
                pygame.mixer.Channel(0).play(ping)
                BALL_ANGLE = random.choice(angle_list)
                BALL_SPEED *= -1

            if ball.colliderect(player_rect_top) or ball.colliderect(computer_rect_top):
                pygame.mixer.Channel(0).play(ping)
                BALL_ANGLE = random.choice(angle_list_top)

            if ball.colliderect(player_rect_bot) or ball.colliderect(computer_rect_bot):
                pygame.mixer.Channel(0).play(ping)
                BALL_ANGLE = random.choice(angle_list_bot)

            if ball_went_out(ball.x, ball.y):
                # ball went out on computer side
                if ball.x < WIDTH / 2:
                    player_score += 1
                    pygame.mixer.Channel(1).play(player_scored)

                    '''*****************************************************
                    if player has at least 2 more points, they win the round
                    either represented by player_score > computer_score + 1
                    or player_score >= computer_score + 2
                    *****************************************************'''
                    if 11 <= player_score > computer_score + 1:
                        rnd += 1
                        play_win += 1
                        player_score = 0
                        computer_score = 0
                        pygame.mixer.Channel(1).stop()
                        pygame.mixer.Channel(3).play(round_over)
                        if play_win == 3:
                            pygame.mixer.Channel(3).stop()
                            pygame.mixer.Channel(4).play(game_over)
                            surf.fill(BLACK)
                            draw_text('You win!', font1, surf, WIDTH / 3 + 205, HEIGHT / 3 + 50)
                            draw_text('Press any key to play again.', font1, surf, WIDTH / 3 + 50,
                                      HEIGHT / 2)
                            surf.blit(player_image2, (WIDTH / 3 + 85, HEIGHT / 2 - 60))
                            pygame.display.update()
                            wait_for_player_to_press_key()
                            break
                        surf.fill(BLACK)
                        draw_text('Round Won!', font1, surf, WIDTH / 3 + 175, HEIGHT / 3 + 50)
                        draw_text('Press any key to start the next round.', font1, surf, WIDTH / 3 - 25, HEIGHT / 2)
                        surf.blit(player_image2, (WIDTH / 3 + 85, HEIGHT / 2 - 60))
                        pygame.display.update()
                        wait_for_player_to_press_key()

                # ball went out on player side
                else:
                    computer_score += 1
                    pygame.mixer.Channel(2).play(computer_scored)
                    if 11 <= computer_score > player_score + 1:
                        rnd += 1
                        comp_win += 1
                        player_score = 0
                        computer_score = 0
                        pygame.mixer.Channel(2).stop()
                        pygame.mixer.Channel(3).play(round_over)
                        if comp_win == 3:
                            pygame.mixer.Channel(3).stop()
                            pygame.mixer.Channel(4).play(game_over)
                            surf.fill(BLACK)
                            draw_text('You lose!', font1, surf, WIDTH / 3 + 200, HEIGHT / 3 + 50)
                            draw_text('Press any key to play again.', font1, surf, WIDTH / 3 + 50,
                                      HEIGHT / 2)
                            surf.blit(computer_image2, (WIDTH / 3 + 85, HEIGHT / 2 - 60))
                            pygame.display.update()
                            wait_for_player_to_press_key()
                            break
                        surf.fill(BLACK)
                        draw_text('Round Lost!', font1, surf, WIDTH / 3 + 170, HEIGHT / 3 + 50)
                        draw_text('Press any key to start the next round.', font1, surf, WIDTH / 3 - 25, HEIGHT / 2)
                        surf.blit(computer_image2, (WIDTH / 3 + 85, HEIGHT / 2 - 60))
                        pygame.display.update()
                        wait_for_player_to_press_key()

                reset_ball(ball)
                BALL_ANGLE = random.choice(angle_list)
                BALL_SPEED = random.choice(speed_list)

            render_round_wins(surf, play_win, comp_win, horz)

            pygame.display.update()
            main_clock.tick(60)  # end of main game loop

        pygame.display.update()
        main_clock.tick(40)  # end of play again loop


play()
