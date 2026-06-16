import pygame
import random
import sys

WIDTH, HEIGHT = 800, 500
FPS = 60

PADDLE_W, PADDLE_H = 15, 100
BALL_SIZE = 15

PLAYER_SPEED = 7
BALL_SPEED = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def reset_ball(ball):
    ball.center = (WIDTH // 2, HEIGHT // 2)
    dx = random.choice([-BALL_SPEED, BALL_SPEED])
    dy = random.choice([-BALL_SPEED, BALL_SPEED])
    return dx, dy

def draw_text(screen, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

def menu(screen):
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)
        draw_text(screen, "PONG GAME", 60, 260, 80)
        draw_text(screen, "1 - Easy", 40, 330, 200)
        draw_text(screen, "2 - Normal", 40, 330, 250)
        draw_text(screen, "3 - Hard", 40, 330, 300)
        draw_text(screen, "Press 1/2/3 to start", 30, 250, 380)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                if event.key == pygame.K_2:
                    return "normal"
                if event.key == pygame.K_3:
                    return "hard"

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Game")

    difficulty = menu(screen)

    # Difficulty tuning (THIS is what makes it winnable)
    if difficulty == "easy":
        AI_SPEED = 3
        AI_REACTION = 0.6   # AI is sloppy
        BALL_SPEED_MULT = 0.9
    elif difficulty == "normal":
        AI_SPEED = 5
        AI_REACTION = 0.85
        BALL_SPEED_MULT = 1.0
    else:
        AI_SPEED = 7
        AI_REACTION = 1.0   # near-perfect tracking
        BALL_SPEED_MULT = 1.1

    clock = pygame.time.Clock()

    player = pygame.Rect(WIDTH - 40, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
    ai = pygame.Rect(25, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)

    ball_dx, ball_dy = reset_ball(ball)
    ball_dx *= BALL_SPEED_MULT
    ball_dy *= BALL_SPEED_MULT

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

        # Player
        if keys[pygame.K_UP]:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            player.y += PLAYER_SPEED

        player.y = max(0, min(HEIGHT - PADDLE_H, player.y))

        # AI with imperfection
        if random.random() < AI_REACTION:
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

        # Paddle collisions
        if ball.colliderect(player) and ball_dx > 0:
            ball.right = player.left
            ball_dx *= -1

        if ball.colliderect(ai) and ball_dx < 0:
            ball.left = ai.right
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
        pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)

        screen.blit(font.render(str(player_score), True, WHITE), (WIDTH//2 + 40, 20))
        screen.blit(font.render(str(ai_score), True, WHITE), (WIDTH//2 - 60, 20))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
