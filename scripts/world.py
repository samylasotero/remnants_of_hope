import pygame
from settings import TILE, MAP_LAYOUT, COLOR_FLOOR, COLOR_WALL
from scripts.player import Player
from scripts.resource import Resource

class World:
    def __init__(self):
        self.walls = []
        self.wall_tiles = set()
        self.player = None
        self.resources = []
        self.width = len(MAP_LAYOUT[0]) * TILE
        self.height = len(MAP_LAYOUT) * TILE
        self._parse()
        self._spawn_resources_demo()

    def in_bounds(self, ti, tj):
        return 0 <= tj < len(MAP_LAYOUT) and 0 <= ti < len(MAP_LAYOUT[0])

    def is_wall_tile(self, ti, tj):
        return (ti, tj) in self.wall_tiles

    def tile_to_xy(self, ti, tj):
        return ti * TILE, tj * TILE

    def place_on_free(self, ti, tj, key, name, rarity, max_radius=8):
        if self.in_bounds(ti, tj) and not self.is_wall_tile(ti, tj):
            x, y = self.tile_to_xy(ti, tj)
            self.resources.append(Resource(x + 4, y + 4, key, name, rarity))
            return
        for r in range(1, max_radius + 1):
            for dx in range(-r, r + 1):
                for dy in (-r, r):
                    ti2, tj2 = ti + dx, tj + dy
                    if self.in_bounds(ti2, tj2) and not self.is_wall_tile(ti2, tj2):
                        x, y = self.tile_to_xy(ti2, tj2)
                        self.resources.append(Resource(x + 4, y + 4, key, name, rarity))
                        return
            for dy in range(-r + 1, r):
                for dx in (-r, r):
                    ti2, tj2 = ti + dx, tj + dy
                    if self.in_bounds(ti2, tj2) and not self.is_wall_tile(ti2, tj2):
                        x, y = self.tile_to_xy(ti2, tj2)
                        self.resources.append(Resource(x + 4, y + 4, key, name, rarity))
                        return

    def _parse(self):
        for j, row in enumerate(MAP_LAYOUT):
            for i, ch in enumerate(row):
                x, y = i * TILE, j * TILE
                if ch == "#":
                    self.walls.append(pygame.Rect(x, y, TILE, TILE))
                    self.wall_tiles.add((i, j))
                elif ch == "P":
                    self.player = Player(x + 3, y + 3)
        if self.player is None:
            self.player = Player(TILE * 2, TILE * 2)

    def _spawn_resources_demo(self):
        self.place_on_free(5, 2,  "madeira",          "Madeira",             "comum")
        self.place_on_free(7, 8,  "sucata_metal",     "Sucata de metal",     "comum")
        self.place_on_free(9, 4,  "parafusos_pregos", "Parafusos e pregos",  "comum")
        self.place_on_free(18, 3, "fios_eletricos",   "Fios elétricos",      "comum")
        self.place_on_free(15, 6, "placas_metalicas", "Placas metálicas",    "intermediario")
        self.place_on_free(20, 9, "placa_circuito",   "Placa de circuito",   "intermediario")
        self.place_on_free(22, 5, "pilhas",           "Pilhas/baterias",     "intermediario")
        self.place_on_free(12,10, "antibioticos",     "Antibióticos",        "raro")
        self.place_on_free(23, 7, "kit_medico",       "Kit médico",          "raro")

    def update(self, dt, events, paused=False):
        # Se o inventário estiver aberto, "pausa" o mundo (sem mover/coletar)
        if paused:
            # ainda assim processamos o toggle de sprint caso você queira permitir mudar estado parado
            # mas sem mover/colecionar
            self.player.handle_events(events)
            return

        # movimento normal
        self.player.update(dt, self.walls, events)

        # Coleta com E quando próximo
        pressed_e = any(e.type == pygame.KEYDOWN and e.key == pygame.K_e for e in events)
        if pressed_e:
            for res in self.resources:
                if not res.collected and res.can_collect(self.player.rect):
                    res.collected = True
                    self.player.inv.add(res.key, 1)
                    # break  # opcional limitar a 1 por tecla

    def draw(self, surface, camera):
        cols = (self.width // TILE) + 1
        rows = (self.height // TILE) + 1
        start_x = int(camera[0] // TILE)
        start_y = int(camera[1] // TILE)
        for y in range(start_y - 1, start_y + rows + 1):
            for x in range(start_x - 1, start_x + cols + 1):
                rx = x * TILE - camera[0]
                ry = y * TILE - camera[1]
                pygame.draw.rect(surface, COLOR_FLOOR, (rx, ry, TILE, TILE))

        for w in self.walls:
            pygame.draw.rect(surface, COLOR_WALL, (w.x - camera[0], w.y - camera[1], w.w, w.h))

        for r in self.resources:
            r.draw(surface, camera)

        self.player.draw(surface, camera)
