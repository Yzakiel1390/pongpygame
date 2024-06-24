import pygame as py, sys, random
from time import sleep

WINDOW_SIZE: tuple[int, ...] = (1200, 700)
PADDLE_SIZE: tuple[int, ...] = (20, 100)
BALL_SIZE: int = 20
BALL_SPEED, PADDLE_SPEED = 7, 7
COLORS: dict[str, tuple[int, ...]] = {
    "BLACK": (0, 0, 0),
    "GRAY": (200, 200, 200),
    "WHITE": (255, 255, 255),
    "BLUE": (0, 0, 255),
    "GREEN": (0, 255, 0)
}

py.init()
clock: py.time.Clock = py.time.Clock()
screen: py.Surface = py.display.set_mode((WINDOW_SIZE))
py.display.set_caption("Pong")

ball: py.Rect = py.Rect(screen.get_width() / 2 - BALL_SIZE / 2, screen.get_height() / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)
player1: py.Rect = py.Rect(PADDLE_SIZE[0] / 2, screen.get_height() / 2 - PADDLE_SIZE[1] / 2, PADDLE_SIZE[0], PADDLE_SIZE[1])
player2: py.Rect = py.Rect(screen.get_width() - (PADDLE_SIZE[0] + PADDLE_SIZE[0] / 2), screen.get_height() / 2 - PADDLE_SIZE[1] / 2, PADDLE_SIZE[0], PADDLE_SIZE[1])
ball_speed_x, ball_speed_y = BALL_SPEED * random.choice((1, -1)), 7 * random.choice((1, -1))
player_speed: int = PADDLE_SPEED
player1_points, player2_points = 0, 0

def ball_animation() -> None:
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if (ball.bottom >= screen.get_height() or ball.top <= 0):
        ball_speed_y *= -1

    if (ball.right >= screen.get_width() or ball.left <= 0):
        ball_reset()
    
    if (ball.colliderect(player1) or ball.colliderect(player2)):
        ball_speed_x *= -1

def ball_reset() -> None:
    global ball_speed_x, ball_speed_y, player1_points, player2_points
    player2_points += 1 if ball.left <= 0 else 0
    player1_points += 1 if ball.right >= screen.get_width() else 0
    update_points()
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))
    ball.center = (screen.get_width()/2, screen.get_height()/2)

def player1_animation(keys: py.key.ScancodeWrapper) -> None:
    if keys[py.K_w] and player1.top >= 0:
        player1.y -= player_speed
    if keys[py.K_s] and player1.bottom <= screen.get_height():
        player1.y += player_speed

def player2_animation(keys: py.key.ScancodeWrapper, gamemode: int) -> None:
    if (gamemode == 1):
        if keys[py.K_UP] and player2.top >= 0:
            player2.y -= player_speed
        if keys[py.K_DOWN] and player2.bottom <= screen.get_height():
            player2.y += player_speed
        return
    if (ball.top <= player2.top and player2.top >= 0):
        player2.y -= player_speed - random.uniform(0, 1)
    elif (ball.bottom >= player2.bottom and player2.bottom <= screen.get_height()):
        player2.y += player_speed - random.uniform(0, 1)

def update_points() -> None:
    global run, winner, max_points
    print(f"\033[1;36m{player1_points:^3} \033[1;30m|\033[m \033[1;32m{player2_points:^3}\033[m")
    if (player1_points >= max_points or player2_points >= max_points):
        run = False
        winner = "Player1" if player1_points > player2_points else "Player2"

def draw() -> None:
    screen.fill(COLORS["BLACK"])
    py.draw.aaline(screen, COLORS["GRAY"], (screen.get_width() / 2, 0), (screen.get_width() / 2, screen.get_height()))
    py.draw.rect(screen, COLORS["BLUE"], player1)
    py.draw.rect(screen, COLORS["GREEN"], player2)
    py.draw.ellipse(screen, COLORS["WHITE"], ball)

def main() -> None:
    print("\033[0;30m- Choose a gamemode: \n \033[m\033[0;37m1 - \033[m\033[1;35mPlayer vs Player\033[m \n \033[0;37m2 - \033[m\033[1;34mPlayer vs IA\033[m")
    gamemode = int(input("\033[1;30m=: \033[m\033[1;32m"))
    while gamemode not in [1, 2]:
        print("\033[0;30m- Choose a gamemode: \n \033[m\033[0;37m1 - \033[m\033[1;35mPlayer vs Player\033[m \n \033[0;37m2 - \033[m\033[1;34mPlayer vs IA\033[m")
        gamemode = int(input("\033[1;30m=: \033[m\033[1;32m"))

    global max_points
    max_points = int(input("\033[0;30m- \033[m\033[1;31mPoints\033[m\033[0;30m required for a player to \033[m\033[1;32mwin\033[m\033[0;30m: \033[m\033[1;36m"))
    global winner
    winner = ""

    input("\033[0;37m- Press any button to get started: \033[m")
    print("\033[1;33mScoreboard: \033[m")

    sleep(3)

    global run
    run = True
    while run:
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
        clock.tick(60)

        draw()
        ball_animation()
        key: py.key.ScancodeWrapper = py.key.get_pressed()
        player1_animation(key)
        player2_animation(key, gamemode)
        
        py.display.flip()

    print("=" * 50)
    print(f"\033[0;30mThe \033[m\033[1;32mWinner\033[m\033[0;30m was the \033[m\033[1;33m{winner}\033[m\033[0;30m!\033[m")
    print(f"\033[1;33mFinal Scoreboard: \033[m\n\033[1;36m{player1_points:^3} \033[1;30m|\033[m \033[1;32m{player2_points:^3}\033[m")

    py.quit()
    sys.exit()

if __name__ == "__main__":
    main()