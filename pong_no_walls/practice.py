import pygame
import random

pygame.init()
# pygame.mixer.init()
pygame.display.set_caption("Pong")

# simple colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# screen size
WIDTH = 1000
HEIGHT = 500

# images
ball_image = pygame.image.load('ball.png')
player_image = pygame.image.load('player_paddle.png')
player_image2 = pygame.image.load('player_paddle2.png')
computer_image = pygame.image.load('computer_paddle.png')
computer_image2 = pygame.image.load('computer_paddle2.png')

# directory = os.getcwd()
# collision_sound = directory + "/sounds/ping_pong_8bit_plop.ogg"
# point_sound = directory + "/sounds/ping_pong_8bit_beeep.ogg"


class Player(pygame.sprite.Sprite):

    def __init__(self, x, key_up, key_down):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 260
        self.points = 0
        self.key_up = key_up
        self.key_down = key_down

    def update(self):
        if pygame.key.get_pressed()[self.key_down]:
            if self.rect.bottom < 600:
                self.rect.y += 5

        if pygame.key.get_pressed()[self.key_up]:
            if self.rect.top > 0:
                self.rect.y -= 5

        Pong().screen.blit(self.image, (self.rect.x, self.rect.y))


class Computer(pygame.sprite.Sprite):

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 260
        self.points = 0

    def update(self, ball_x, ball_y):
        if ball_x:
            if self.rect.bottom < 600:
                self.rect.y += 5

        if ball_y:
            if self.rect.top > 0:
                self.rect.y -= 5

        Pong().screen.blit(self.image, (self.rect.x, self.rect.y))


class Ball(pygame.sprite.Sprite):
    def __init__(self, direction, speed=2):
        pygame.sprite.Sprite.__init__(self)
        self.image = ball_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2
        self.rect.y = HEIGHT/2
        self.direction_x = direction
        self.direction_y = direction
        self.speed = speed

    def update(self):
        if self.rect.y >= 600 or self.rect.y <= 0:
            # pygame.mixer.music.load(collision_sound)
            # pygame.mixer.music.play()
            self.direction_y *= -1

        self.rect.y += self.direction_y * self.speed
        self.rect.x += self.direction_x * self.speed

        Pong().screen.blit(self.image, (self.rect.x, self.rect.y))


class Pong:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player = Player(10, pygame.K_UP, pygame.K_DOWN)
        self.computer = Computer(780)
        self.ball = Ball(random.choice([1, -1]))
        self.clock = pygame.time.Clock()

    def update(self):
        self.screen.fill(BLACK)
        self.player.update()
        self.computer.update(self.ball.rect.right, self.ball.rect.left)
        self.ball.update()
        self.show_points()
        self.check_collisions()
        self.check_point()
        pygame.draw.rect(self.screen, WHITE, (400, 0, 3, 800))
        pygame.display.update()

    def check_collisions(self):
        if pygame.sprite.collide_rect(self.player, self.ball) or\
                pygame.sprite.collide_rect(self.computer, self.ball):
            # pygame.mixer.music.load(collision_sound)
            # pygame.mixer.music.play()
            self.ball.direction_x *= -1
            self.ball.speed += 0.5

    def check_point(self):
        if self.ball.rect.left < 10:
            # pygame.mixer.music.load(point_sound)
            # pygame.mixer.music.play()
            self.computer.points += 1
            self.ball = Ball(1)

        if self.ball.rect.right > 790:
            #pygame.mixer.music.load(point_sound)
            #pygame.mixer.music.play()
            self.player.points += 1
            self.ball = Ball(-1)

    def show_points(self):
        p1_points = str(self.player.points)
        p2_points = str(self.computer.points)
        font = pygame.font.Font(None, 80)
        text1 = font.render(p1_points, True, WHITE)
        text2 = font.render(p2_points, True, WHITE)

        text1_rect = text1.get_rect(center=(200, 50))
        text2_rect = text2.get_rect(center=(600, 50))

        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)

    def main(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.update()
            self.clock.tick(120)

    def start(self):
        group = pygame.sprite.Group()
        group.add(Ball(-1))
        group.add(Ball(1))

        running = True
        font = pygame.font.Font(None, 110)

        title = font.render("Pong", True, WHITE)
        title_rect = title.get_rect(center=(400, 200))

        font = pygame.font.Font(None, 20)

        subtitle = font.render("Press SPACE to start", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(400, 300))

        while running:
            self.screen.fill(BLACK)
            self.screen.blit(title, title_rect)
            self.screen.blit(subtitle, subtitle_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    break

                for b in group:
                    if b.rect.x <= 0 or b.rect.x >= 800:
                        b.direction_x *= -1

                    if b.rect.y >= 600 or b.rect.y <= 0:
                        b.direction_y *= -1

                    b.rect.y += b.direction_y * b.speed
                    b.rect.x += b.direction_x * b.speed
                    self.screen.blit(b.image, b.rect)

                pygame.display.update()

            if running:
                self.main()
            else:
                pygame.quit()

Pong().start()
