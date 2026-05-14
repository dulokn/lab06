import sys
import random
import pygame

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

BLACK = (15, 15, 40)
WHITE = (0, 220, 255)
GRAY  = (100, 180, 220)

FPS          = 60
PADDLE_W     = 12
PADDLE_H     = 90
BALL_SIZE    = 14
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
WIN_SCORE    = 7

clock      = pygame.time.Clock()
font_big   = pygame.font.SysFont("monospace", 72, bold=True)
font_small = pygame.font.SysFont("monospace", 28)


def make_paddle(x, y):
    return pygame.Rect(x, y, PADDLE_W, PADDLE_H)


def reset_ball():
    rect  = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                        HEIGHT // 2 - BALL_SIZE // 2,
                        BALL_SIZE, BALL_SIZE)
    vel_x = BALL_SPEED_X * random.choice([-1, 1])
    vel_y = BALL_SPEED_Y * random.choice([-1, 1])
    return rect, vel_x, vel_y


def main():
    paddle_left  = make_paddle(20, HEIGHT // 2 - PADDLE_H // 2)
    paddle_right = make_paddle(WIDTH - 20 - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2)
    ball, vel_x, vel_y = reset_ball()

    score_left  = 0
    score_right = 0
    game_over   = False
    winner      = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return

        keys = pygame.key.get_pressed()

        if not game_over:
            if keys[pygame.K_w] and paddle_left.top > 0:
                paddle_left.y -= PADDLE_SPEED
            if keys[pygame.K_s] and paddle_left.bottom < HEIGHT:
                paddle_left.y += PADDLE_SPEED
            if keys[pygame.K_UP] and paddle_right.top > 0:
                paddle_right.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and paddle_right.bottom < HEIGHT:
                paddle_right.y += PADDLE_SPEED

            ball.x += vel_x
            ball.y += vel_y

            if ball.top <= 0 or ball.bottom >= HEIGHT:
                vel_y *= -1

            if ball.colliderect(paddle_left) and vel_x < 0:
                vel_x *= -1
                ball.left = paddle_left.right
            if ball.colliderect(paddle_right) and vel_x > 0:
                vel_x *= -1
                ball.right = paddle_right.left

            if ball.right < 0:
                score_right += 1
                ball, vel_x, vel_y = reset_ball()
            elif ball.left > WIDTH:
                score_left += 1
                ball, vel_x, vel_y = reset_ball()

            if score_left >= WIN_SCORE:
                game_over = True
                winner = "Left Player"
            elif score_right >= WIN_SCORE:
                game_over = True
                winner = "Right Player"

        screen.fill(BLACK)

        for y in range(0, HEIGHT, 20):
            pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 2, y, 4, 10))

        ls = font_big.render(str(score_left),  True, WHITE)
        rs = font_big.render(str(score_right), True, WHITE)
        screen.blit(ls, (WIDTH // 4 - ls.get_width() // 2, 20))
        screen.blit(rs, (3 * WIDTH // 4 - rs.get_width() // 2, 20))

        hint = font_small.render("W/S  vs  UP/DOWN  |  R = restart", True, GRAY)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 36))

        pygame.draw.rect(screen, WHITE, paddle_left,  border_radius=4)
        pygame.draw.rect(screen, WHITE, paddle_right, border_radius=4)
        pygame.draw.rect(screen, WHITE, ball,         border_radius=3)

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            ws = font_big.render(f"{winner} Wins!", True, WHITE)
            screen.blit(ws, (WIDTH // 2 - ws.get_width() // 2, HEIGHT // 2 - 60))
            rs2 = font_small.render("Press R to play again", True, GRAY)
            screen.blit(rs2, (WIDTH // 2 - rs2.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
