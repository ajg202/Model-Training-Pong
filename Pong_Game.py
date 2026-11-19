import random

import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 15
BALL_RADIUS = 7.5
MAX_SPEED = 15
ACCELERATION = 0.001


def reset_ball():
    return 395, 295, random.choice((-3, 3)), random.choice((-3, 3))


def resolve_paddle_collisions(
    ball_x,
    ball_y,
    previous_x,
    previous_y,
    x_speed,
    y_speed,
    paddles,
):
    for paddle_x, paddle_y in paddles:
        paddle_right = paddle_x + PADDLE_WIDTH
        paddle_bottom = paddle_y + PADDLE_HEIGHT
        overlaps_paddle_height = (
            ball_y + BALL_RADIUS >= paddle_y
            and ball_y - BALL_RADIUS <= paddle_bottom
        )
        overlaps_paddle_width = (
            ball_x + BALL_RADIUS >= paddle_x
            and ball_x - BALL_RADIUS <= paddle_right
        )

        if (
            x_speed > 0
            and previous_x + BALL_RADIUS <= paddle_x
            and ball_x + BALL_RADIUS >= paddle_x
            and overlaps_paddle_height
        ):
            ball_x = paddle_x - BALL_RADIUS
            x_speed = -abs(x_speed)
        elif (
            x_speed < 0
            and previous_x - BALL_RADIUS >= paddle_right
            and ball_x - BALL_RADIUS <= paddle_right
            and overlaps_paddle_height
        ):
            ball_x = paddle_right + BALL_RADIUS
            x_speed = abs(x_speed)
        elif (
            y_speed > 0
            and previous_y + BALL_RADIUS <= paddle_y
            and ball_y + BALL_RADIUS >= paddle_y
            and overlaps_paddle_width
        ):
            ball_y = paddle_y - BALL_RADIUS
            y_speed = -abs(y_speed)
        elif (
            y_speed < 0
            and previous_y - BALL_RADIUS >= paddle_bottom
            and ball_y - BALL_RADIUS <= paddle_bottom
            and overlaps_paddle_width
        ):
            ball_y = paddle_bottom + BALL_RADIUS
            y_speed = abs(y_speed)

    return ball_x, ball_y, x_speed, y_speed


def move_paddles(keys, player1_y, player2_y):
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        player1_y += PADDLE_SPEED
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        player2_y += PADDLE_SPEED

    return player1_y, player2_y


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 36)

    ball_x, ball_y, x_speed, y_speed = reset_ball()
    player1_x, player1_y = 50, 250
    player2_x, player2_y = 740, 250
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        clock.tick(FPS)
        ball_speed = (x_speed**2 + y_speed**2) ** 0.5
        speed_text = font.render(f"Speed: {ball_speed:.2f}", True, WHITE)
        screen.blit(speed_text, (300, 0))

        pygame.draw.rect(
            screen,
            WHITE,
            (player1_x, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT),
        )
        pygame.draw.rect(
            screen,
            WHITE,
            (player2_x, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT),
        )
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
        pygame.display.flip()

        previous_x, previous_y = ball_x, ball_y
        ball_x += x_speed
        ball_y += y_speed

        if ball_x - BALL_RADIUS <= 0:
            pygame.display.set_caption("Player 2 Wins!")
            game_over = True
        elif ball_x + BALL_RADIUS >= SCREEN_WIDTH:
            pygame.display.set_caption("Player 1 Wins!")
            game_over = True

        paddles = ((player1_x, player1_y), (player2_x, player2_y))
        ball_x, ball_y, x_speed, y_speed = resolve_paddle_collisions(
            ball_x,
            ball_y,
            previous_x,
            previous_y,
            x_speed,
            y_speed,
            paddles,
        )

        keys = pygame.key.get_pressed()
        player1_y, player2_y = move_paddles(keys, player1_y, player2_y)

        if game_over:
            pygame.time.delay(2000)
            ball_x, ball_y, x_speed, y_speed = reset_ball()
            game_over = False
            pygame.display.set_caption("Pong")

        if ball_y - BALL_RADIUS <= 0:
            ball_y = BALL_RADIUS
            y_speed = abs(y_speed)
        elif ball_y + BALL_RADIUS >= SCREEN_HEIGHT:
            ball_y = SCREEN_HEIGHT - BALL_RADIUS
            y_speed = -abs(y_speed)

        if x_speed**2 + y_speed**2 < MAX_SPEED**2:
            x_speed += ACCELERATION if x_speed > 0 else -ACCELERATION
            y_speed += ACCELERATION if y_speed > 0 else -ACCELERATION

    pygame.quit()


if __name__ == "__main__":
    main()
