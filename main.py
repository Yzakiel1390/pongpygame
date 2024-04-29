import pygame as py, sys, random
from time import sleep

print("\033[0;30m- Escolha um Modo: \n \033[m\033[0;37m1 - \033[m\033[1;35mPlayer vs Player\033[m \n \033[0;37m2 - \033[m\033[1;34mPlayer vs IA\033[m")
gamemode = int(input("\033[1;30m=: \033[m\033[1;32m"))

while gamemode not in [1, 2]:
    print("\033[0;30m- Escolha um Modo: \n \033[m\033[0;37m1 - \033[m\033[1;35mPlayer vs Player\033[m \n \033[0;37m2 - \033[m\033[1;34mPlayer vs IA\033[m")
    gamemode = int(input("\033[1;30m=: \033[m\033[1;32m"))

max_points = int(input("\033[0;30m- \033[m\033[1;31mPontos\033[m\033[0;30m para a \033[m\033[1;32mVitória\033[m\033[0;30m: \033[m\033[1;36m"))
winner = ""

input("\033[0;37m- Aperte qualquer botão para começar: \033[m")

print("\033[1;33mPlacar: \033[m")

py.init()
clock = py.time.Clock()

def ball_animation() -> None:
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if (ball.bottom >= screen.get_height() or ball.top <= 0): #Colisão com a Parede (Vertical)
        ball_speed_y *= -1

    if (ball.right >= screen.get_width() or ball.left <= 0): # Reset do Movimento
        ball_reset()
    
    if (ball.colliderect(player1) or ball.colliderect(player2)): # Colisão com os Players
        ball_speed_x *= -1

def ball_reset() -> None:
    global ball_speed_x, ball_speed_y, player1_points, player2_points
    player2_points += 1 if ball.left <= 0 else 0
    player1_points += 1 if ball.right >= screen.get_width() else 0
    update_points()
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))
    ball.center = (screen.get_width()/2, screen.get_height()/2)

def player1_animation() -> None:
    if key[py.K_w] and player1.top >= 0:
        player1.y -= player_speed
    if key[py.K_s] and player1.bottom <= screen.get_height():
        player1.y += player_speed

def player2_animation() -> None:
    if (gamemode == 1):
        if key[py.K_UP] and player2.top >= 0:
            player2.y -= player_speed
        if key[py.K_DOWN] and player2.bottom <= screen.get_height():
            player2.y += player_speed
    else:
        if (ball.top <= player2.top and player2.top >= 0):
            player2.y -= player_speed - random.choice((0, 0.1, 0.12, 0.13, -0.14, 0.15, 0.16, -0.2, 0.22, 0.23, 1))
        elif (ball.bottom >= player2.bottom and player2.bottom <= screen.get_height()):
            player2.y += player_speed - random.choice((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))

def update_points() -> None:
    global run, winner
    print(f"\033[1;36m{player1_points:^3} \033[1;30m|\033[m \033[1;32m{player2_points:^3}\033[m")
    if (player1_points >= max_points or player2_points >= max_points):
        run = False
        winner = "Player1" if player1_points > player2_points else "Player2"

window = (1200, 700)

screen = py.display.set_mode((window))
py.display.set_caption("Pong")

ball = py.Rect(screen.get_width()/2 - 10, screen.get_height()/2 - 10, 20, 20)
player1 = py.Rect(10, screen.get_height()/2 - 20, 20, 100)
player2 = py.Rect(screen.get_width() - 30, screen.get_height()/2 - 20, 20, 100)

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 7
player1_points = 0
player2_points = 0

sleep(3)

run = True
while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
    
    clock.tick(60)
    
    screen.fill((0, 0, 0))
    py.draw.aaline(screen, (200, 200, 200), (screen.get_width()/2, 0), (screen.get_width()/2, screen.get_height()))
    py.draw.rect(screen, (0, 0, 255), player1)
    py.draw.rect(screen, (0, 255, 0), player2)
    py.draw.ellipse(screen, (255, 255, 255), ball)

    ball_animation()

    key = py.key.get_pressed()
    player1_animation()
    player2_animation()

    py.display.flip()

print("=" * 50)
print(f"\033[0;30mO \033[m\033[1;32mVencedor\033[m\033[0;30m foi o \033[m\033[1;33m{winner}\033[m\033[0;30m!\033[m")
print(f"\033[1;33mPlacar final: \033[m\n\033[1;36m{player1_points:^3} \033[1;30m|\033[m \033[1;32m{player2_points:^3}\033[m")

py.quit()
sys.exit()