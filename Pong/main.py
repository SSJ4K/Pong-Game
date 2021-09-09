import pygame as py
import sys
import random

py.init()

running = True
width, height = 800, 600
py.display.set_caption("Pong")
screen = py.display.set_mode((width, height))
colours = {"White": (245, 245, 245), "Black": (0, 0, 0), "Green": (0, 255, 0)}
FPS = 60
time = py.time.Clock()
time_2 = 0
speed_stop = False


class Players:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.y_move = 0
        self.up_pressed = False
        self.down_pressed = False
        self.w_pressed = False
        self.s_pressed = False
        self.rect = py.draw.rect(screen, colours["White"], (self.x, self.y, 10, 100))

    def move(self, speed):
        if self.up_pressed or self.w_pressed:
            self.y_move = -speed
        if self.down_pressed or self.s_pressed:
            self.y_move = speed

        self.y += self.y_move
        self.rect = py.draw.rect(screen, colours["White"], (self.x, self.y, 10, 100))

        # collision


class Ball:
    def __init__(self, ball_x, ball_y):
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.dy = 1
        self.dx = 1
        self.bll = py.draw.rect(screen, colours["White"], (self.ball_x, self.ball_y, 20, 20))
        self.speed = 5
        self.pl_1score = 0
        self.pl_2score = 0

    def move(self):
        self.ball_x += self.speed * self.dx
        self.ball_y -= self.speed * self.dy

        self.bll = py.draw.rect(screen, colours["White"], (self.ball_x, self.ball_y, 20, 20))


def walls():
    wall_top = py.draw.rect(screen, colours["White"], (10, 20, 780, 20))
    wall_bottom = py.draw.rect(screen, colours["White"], (10, 550, 780, 20))
    py.draw.rect(screen, colours["White"], (380, 20, 10, 550))
    paddle_hit = py.mixer.Sound("sounds/paddle_hit.wav")
    wall_hit = py.mixer.Sound("sounds/wall_hit.wav")

    if pl_1.y <= 60:
        pl_1.y = 60
    elif pl_1.y >= 430:
        pl_1.y = 430
    if pl_2.y <= 60:
        pl_2.y = 60
    elif pl_2.y >= 430:
        pl_2.y = 430

    if ball.bll.colliderect(wall_top):
        ball.dy = -1
        py.mixer.Sound.play(wall_hit)
    elif ball.bll.colliderect(wall_bottom):
        ball.dy = 1
        py.mixer.Sound.play(wall_hit)
    if ball.bll.colliderect(pl_1.rect):
        ball.dx = 1
        py.mixer.Sound.play(paddle_hit)
    elif ball.bll.colliderect(pl_2.rect):
        ball.dx = -1
        py.mixer.Sound.play(paddle_hit)

    if ball.ball_x >= 790:
        ball.ball_x = random.randrange(300, 500)
        ball.ball_y = random.randrange(200, 400)
        ball.pl_1score += 1
    elif ball.ball_x <= 0:
        ball.ball_x = random.randrange(300, 500)
        ball.ball_y = random.randrange(200, 400)
        ball.pl_2score += 1


def winner(text, size):
    global time_2, speed_stop
    # ball.ball_y = 7000
    ball.speed = 0
    speed_stop = True
    font = py.font.Font("font/New Athletic M54.ttf", size)
    show = font.render(text, True, colours["Green"])
    restart = font.render("Press R", True, colours["Green"])
    screen.blit(show, (200, 100))
    screen.blit(restart, (300, 300))

    pressed = py.key.get_pressed()
    if pressed[py.K_r]:
        # ball.ball_y = random.randrange(200, 400)
        ball.pl_1score = 0
        ball.pl_2score = 0
        time_2 = 0
        ball.speed = 5
        speed_stop = False


def score(score, size, x):
    font = py.font.Font("font/New Athletic M54.ttf", size)
    show = font.render(str(score), True, colours["White"])
    screen.blit(show, (x, 250))


pl_1 = Players(150, 10)
pl_2 = Players(150, 780)
ball = Ball(random.randrange(300, 500), random.randrange(200, 400))

while running:
    time_2 += 1
    print(time_2)

    if time_2 >= 1000 and not speed_stop:
        ball.speed = 6
    if time_2 >= 2000 and not speed_stop:
        ball.speed = 7
    if time_2 >= 3000 and not speed_stop:
        ball.speed = 8
    if time_2 >= 4000 and not speed_stop:
        ball.speed = 9

    time.tick(FPS)
    screen.fill(colours["Black"])

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

        if event.type == py.KEYDOWN:
            if event.key == py.K_UP:
                pl_2.up_pressed = True
            if event.key == py.K_DOWN:
                pl_2.down_pressed = True

            if event.key == py.K_w:
                pl_1.w_pressed = True
            if event.key == py.K_s:
                pl_1.s_pressed = True

        if event.type == py.KEYUP:
            if event.key == py.K_UP:
                pl_2.up_pressed = False
                pl_2.y_move = 0
            if event.key == py.K_w:
                pl_1.w_pressed = False
                pl_1.y_move = 0
            if event.key == py.K_DOWN:
                pl_2.down_pressed = False
                pl_2.y_move = 0
            if event.key == py.K_s:
                pl_1.s_pressed = False
                pl_1.y_move = 0

    walls()
    score(ball.pl_1score, 60, 200)
    score(ball.pl_2score, 60, 550)
    ball.move()
    pl_1.move(7)
    pl_2.move(7)

    if ball.pl_1score >= 10:
        winner("Player 1 wins", 70)
    elif ball.pl_2score >= 10:
        winner("Player 2 wins", 70)
    py.display.update()

py.quit()
sys.exit()
