import pygame
from constants import *
from bullet import Bullet
from circleshape import CircleShape

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0
        self.previous_keys = pygame.key.get_pressed()
        self.slowing = False
        self.slow_speed = 0
        

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, (135, 135, 135), self.triangle())

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # checks to see if a key was pressed and how the player reacts
        if keys[pygame.K_SPACE]:                        # If they press the spacebar,
            self.shoot()                                # they shoot a bullet.

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:     # If they press the LEFT arrow (or A key),
            self.rotate(-abs(dt))                       # they rotate counter-clockwise.

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:    # If they press the RIGHT arrow (or D key),
            self.rotate(dt)                             # they rotate clockwise.

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:     # If they press the DOWN arrow (or S key),
            self.move(-abs(dt))                         # they move backwards.

        if keys[pygame.K_w] or keys[pygame.K_UP]:       # If they press the UP arrow (or W key),
            self.move(dt)                               # they move forwards.

        if self.previous_keys[pygame.K_UP] and not keys[pygame.K_UP]:   # Check if the UP key was released.
            self.slow_speed = dt                                        # If so, we are going to slow down instead of stop.
            self.slowing = True
        elif self.previous_keys[pygame.K_w] and not keys[pygame.K_w]:   # Check if the W key was released.
            self.slow_speed = dt                                        # If so, we are going to slow down instead of stop.
            self.slowing = True

        self.previous_keys = keys   # Update the current state of keys (pressed or not) into the previous state.
                                    # This will detect future key releases.

        if self.slowing == True:                                    # If the player is slowing down,
            self.slow_speed = self.slow_speed * SLOW_DOWN_FACTOR    # then we need to reduce its speed.
            self.move(self.slow_speed)
            if abs(self.slow_speed) < dt * 0.01:    # Once we are sufficiently slow enough, we stop slowing down and just stop.
                self.slowing = False
        
        self.cooldown_timer -= dt

    def move(self, dt):
        # Check if, when moving, the player crosses any screen borders. If they do, loop them around to the opposite side
        if self.position.x - self.radius < 0:
            self.position = pygame.Vector2(SCREEN_WIDTH - self.radius, self.position.y)

        if self.position.x + self.radius > SCREEN_WIDTH:
            self.position = pygame.Vector2(0 + self.radius, self.position.y)

        if self.position.y - self.radius < 0:
            self.position = pygame.Vector2(self.position.x, SCREEN_HEIGHT - self.radius)

        if self.position.y + self.radius > SCREEN_HEIGHT:
            self.position = pygame.Vector2(self.position.x, 0 + self.radius)

        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        

    def shoot(self):
        if self.cooldown_timer > 0:
            return
        velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        bullet = Bullet(self.position.x, self.position.y, velocity)
        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN
