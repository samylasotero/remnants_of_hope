import pygame
from settings import TILE, COLOR_PLAYER
from scripts.inventory import Inventory

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE - 6, TILE - 6)
        self.base_speed = 140
        self.sprint_speed = 240

        # Stamina
        self.stamina_max = 100.0
        self.stamina = self.stamina_max
        self.stamina_drain = 25.0
        self.stamina_regen = 15.0

        # Sprint (toggle) + trava de reativação
        self.sprint_active = False
        self.exhausted = False
        self.reactivate_ratio = 0.40

        # Inventário real
        self.inv = Inventory()

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and (e.key in (pygame.K_LSHIFT, pygame.K_RSHIFT)):
                if not self.exhausted:
                    self.sprint_active = not self.sprint_active

    def _input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy += 1
        if dx and dy:
            inv = 0.70710678
            dx *= inv; dy *= inv
        return dx, dy

    def update(self, dt, walls, events=None):
        if events: self.handle_events(events)
        dx, dy = self._input()
        sprint_ok = self.sprint_active and (not self.exhausted) and self.stamina > 0.0
        speed = self.sprint_speed if sprint_ok else self.base_speed

        old_x, old_y = self.rect.x, self.rect.y
        # X
        self.rect.x += int(dx * speed * dt)
        for w in walls:
            if self.rect.colliderect(w):
                if dx > 0: self.rect.right = w.left
                elif dx < 0: self.rect.left = w.right
        # Y
        self.rect.y += int(dy * speed * dt)
        for w in walls:
            if self.rect.colliderect(w):
                if dy > 0: self.rect.bottom = w.top
                elif dy < 0: self.rect.top = w.bottom

        moved = (self.rect.x != old_x) or (self.rect.y != old_y)

        # Stamina
        if sprint_ok and moved:
            self.stamina -= self.stamina_drain * dt
            if self.stamina <= 0.0:
                self.stamina = 0.0
                self.exhausted = True
                self.sprint_active = False
        else:
            self.stamina = min(self.stamina_max, self.stamina + self.stamina_regen * dt)

        if self.exhausted and self.stamina >= self.stamina_max * self.reactivate_ratio:
            self.exhausted = False

    def draw(self, surface, camera):
        pygame.draw.rect(surface, COLOR_PLAYER,
                         (self.rect.x - camera[0], self.rect.y - camera[1], self.rect.w, self.rect.h),
                         border_radius=6)
