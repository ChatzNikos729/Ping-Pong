import pygame
import random

WIDTH, HEIGHT = 800, 500
FPS = 60

PADDLE_W, PADDLE_H = 15, 100
BALL_SIZE = 15

PLAYER_SPEED = 7
AI_SPEED = 5
BALL_SPEED = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def reset_ball(ball):
    ball.center = (WIDTH // 2, HEIGHT // 2)
    dx = random.choice([-BALL_SPEED, BALL_SPEED])
    dy = random.choice([-BALL_SPEED, BALL_SPEED])
    return dx, dy


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Game")
    clock = pygame.time.Clock()

    player = pygame.Rect(WIDTH - 40, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
    ai = pygame.Rect(25, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)

    ball_dx, ball_dy = reset_ball(ball)

    player_score = 0
    ai_score = 0

    font = pygame.font.SysFont(None, 50)

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Player controls (RIGHT paddle)
        if keys[pygame.K_UP]:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            player.y += PLAYER_SPEED

        player.y = max(0, min(HEIGHT - PADDLE_H, player.y))

        # AI (LEFT paddle)
        if ai.centery < ball.centery:
            ai.y += AI_SPEED
        else:
            ai.y -= AI_SPEED

        ai.y = max(0, min(HEIGHT - PADDLE_H, ai.y))

        # Ball movement
        ball.x += ball_dx
        ball.y += ball_dy

        # Wall bounce
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Paddle collision
        if ball.colliderect(player) and ball_dx > 0:
            ball_dx *= -1
        if ball.colliderect(ai) and ball_dx < 0:
            ball_dx *= -1

        # Score
        if ball.left <= 0:
            player_score += 1
            ball_dx, ball_dy = reset_ball(ball)

        if ball.right >= WIDTH:
            ai_score += 1
            ball_dx, ball_dy = reset_ball(ball)

        # Draw
        screen.fill(BLACK)

        pygame.draw.rect(screen, WHITE, player)
        pygame.draw.rect(screen, WHITE, ai)
        pygame.draw.ellipse(screen, WHITE, ball)

        # center line
        pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)

        # score
        p_text = font.render(str(player_score), True, WHITE)
        a_text = font.render(str(ai_score), True, WHITE)

        screen.blit(p_text, (WIDTH//2 + 40, 20))
        screen.blit(a_text, (WIDTH//2 - 60, 20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()