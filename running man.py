import pygame
import sys
import random

# setup
pygame.init()

# konstanter
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -14
PLAYER_SPEED = 4
GROUND_Y = SCREEN_HEIGHT - 50

# Hinderkonstanter
OBSTACLE_SPEED = 4          # hur snabbt hindren rör sig
OBSTACLE_SPAWN_TIME = 120   # frames mellan varje hinder (2 sek vid 60fps)
OBSTACLE_MIN_HEIGHT = 30
OBSTACLE_MAX_HEIGHT = 80

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Run and Jump stage 1")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Arial", 20)

# Bilder
player_image = pygame.image.load("modul-7-instruktioner/player1.png").convert_alpha()


def draw_player(surface, x, y):
    """Draw the player at (x, y) where y is the feet position."""
    draw_x = x - player_image.get_width() // 2
    draw_y = y - player_image.get_height()
    surface.blit(player_image, (draw_x, draw_y))


def draw_background(surface):
    surface.fill("skyblue")

    # Sol
    pygame.draw.circle(surface, "yellow", (680, 70), 40)

    # Mark
    pygame.draw.rect(surface, "springgreen4", (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
    pygame.draw.rect(surface, "burlywood4", (0, GROUND_Y + 8, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y - 8))


def draw_hud(surface, score):
    label = font_small.render("Arrow Keys / WASD  |  Space / Up = Jump", True, "black")
    surface.blit(label, (50, 14))

    score_label = font_small.render(f"Poäng: {score}", True, "black")
    surface.blit(score_label, (SCREEN_WIDTH - 150, 14))


def draw_obstacle(surface, obstacle):
    """Rita ett hinder. obstacle = {"rect": pygame.Rect, "color": str}"""
    pygame.draw.rect(surface, obstacle["color"], obstacle["rect"])
    # Lite detalj på toppen
    top_rect = pygame.Rect(obstacle["rect"].x, obstacle["rect"].y, obstacle["rect"].width, 6)
    pygame.draw.rect(surface, "darkred", top_rect)


def spawn_obstacle():
    """Skapa ett nytt hinder på höger sida av skärmen."""
    height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
    width = random.randint(25, 45)
    x = SCREEN_WIDTH
    y = GROUND_Y - height
    rect = pygame.Rect(x, y, width, height)
    return {"rect": rect, "color": "firebrick"}


def main():
    player_x = 300
    player_y = GROUND_Y
    vel_x = 0
    vel_y = 0
    on_ground = True
    running = True

    # Hinderlista och timer
    obstacles = []
    spawn_timer = 0
    score = 0
    score_timer = 0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vel_x = PLAYER_SPEED
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vel_x = -PLAYER_SPEED
        else:
            vel_x = 0

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and on_ground:
            vel_y = JUMP_STRENGTH
            on_ground = False

        # Fysik
        vel_y += GRAVITY
        player_x += vel_x
        player_y += vel_y

        if player_x < 50:
            player_x = 50

        # Krock vid marken
        on_ground = False
        if player_y >= GROUND_Y:
            player_y = GROUND_Y
            vel_y = 0
            on_ground = True

        # ── HINDER ──────────────────────────────────────────────

        # Spawna nya hinder
        spawn_timer += 1
        if spawn_timer >= OBSTACLE_SPAWN_TIME:
            obstacles.append(spawn_obstacle())
            spawn_timer = 0

        # Flytta och ta bort hinder som gått utanför skärmen
        obstacles = [obs for obs in obstacles if obs["rect"].right > 0]
        for obs in obstacles:
            obs["rect"].x -= OBSTACLE_SPEED

        # Kollisionskontroll: spelaren är en liten rektangel runt karaktären
        player_rect = pygame.Rect(
            player_x - player_image.get_width() // 2 + 8,   # lite marginal
            player_y - player_image.get_height() + 5,
            player_image.get_width() - 16,
            player_image.get_height() - 5
        )

        for obs in obstacles:
            if player_rect.colliderect(obs["rect"]):
                # Spelaren träffade ett hinder – avsluta spelet
                print(f"Game Over! Poäng: {score}")
                pygame.quit()
                sys.exit()

        # Öka poäng med tiden
        score_timer += 1
        if score_timer >= 30:   # varannan sekund
            score += 1
            score_timer = 0

        # ── RITA ─────────────────────────────────────────────────
        draw_background(screen)

        for obs in obstacles:
            draw_obstacle(screen, obs)

        draw_player(screen, player_x, player_y)
        draw_hud(screen, score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


main()