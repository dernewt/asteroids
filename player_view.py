import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullet import Bullet
from terry import Terry

def draw_player_view(screen, player, asteroids, bullets):
    offset = 100
    screen_center = pygame.Vector2(
        screen.get_width() // 2,
        screen.get_height() // 2 + offset)
    player_angle = player.rotation  # Make sure this is in degrees

    # --- Draw Player ---
    triangle_points = player.triangle()  # Returns 3 world-space points
    rotated = [pt - player.position for pt in triangle_points]  # make relative to player
    rotated = [pt.rotate(-player_angle) for pt in rotated]      # rotate so player faces up
    final = [screen_center + pt for pt in rotated]              # move to screen center
    #pygame.draw.polygon(screen, (135, 135, 135), final, width=2)
    pygame.draw.polygon(screen, (135, 135, 135), final, width=0)

    # --- Draw Asteroids ---
    for asteroid in asteroids:
        rel = asteroid.position - player.position
        rel = rel.rotate(-player_angle)
        pos = screen_center + rel
        pygame.draw.circle(screen, (200, 200, 200), pos, asteroid.radius, width=2)

    # --- Draw Bullets ---
    for bullet in bullets:
        rel = bullet.position - player.position
        rel = rel.rotate(-player_angle)
        pos = screen_center + rel
        pygame.draw.circle(screen, (255, 30, 77), pos, BULLET_RADIUS)
