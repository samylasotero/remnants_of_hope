import pygame
from settings import TILE, RARITY_COLOR

class Resource:
    def __init__(self, x, y, key, name, rarity):
        self.key = key
        self.name = name
        self.rarity = rarity  # "comum" | "intermediario" | "raro"
        self.rect = pygame.Rect(x, y, TILE - 8, TILE - 8)
        self.collected = False

    def can_collect(self, player_rect):
        area = self.rect.inflate(24, 24)  # raio de interação
        return (not self.collected) and area.colliderect(player_rect)

    def draw(self, surface, camera):
        if self.collected:
            return
        color = RARITY_COLOR.get(self.rarity, (200, 200, 200))
        pygame.draw.rect(surface, color,
                         (self.rect.x - camera[0], self.rect.y - camera[1], self.rect.w, self.rect.h),
                         border_radius=6)
