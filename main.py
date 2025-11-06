import pygame, sys
from settings import WIDTH, HEIGHT, FPS, COLOR_BG
from scripts.world import World
from scripts.ui import StartScreen, HUD, InventoryUI, CraftingUI
from scripts.crafting import load_recipes, list_recipes, can_craft, craft


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Remnants of Hope — MVP")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)

        self.state = "menu"
        self.menu = StartScreen(self.font)
        self.world = World()
        self.hud = HUD(self.font)
        self.inv_ui = InventoryUI(self.font)
        self.craft_ui = CraftingUI(self.font)

        self.cam_x = 0
        self.cam_y = 0

        # estados de UI
        self.inventory_open = False
        self.crafting_open = False

        # receitas
        self.recipes = load_recipes()
        self.recipes_list = list_recipes(self.recipes)

        # toast
        self.toast_text = None
        self.toast_timer = 0.0

    def show_toast(self, text, seconds=2.0):
        self.toast_text = text
        self.toast_timer = seconds

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            if self.toast_timer > 0:
                self.toast_timer -= dt
                if self.toast_timer <= 0:
                    self.toast_text = None

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit(0)
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    if self.inventory_open:
                        self.inventory_open = False
                    elif self.crafting_open:
                        self.crafting_open = False
                    else:
                        pygame.quit(); sys.exit(0)
                if self.state == "menu" and e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    self.state = "game"
                if self.state == "game" and e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_TAB:
                        # abre/fecha inventário (fecha crafting se aberto)
                        if self.crafting_open:
                            self.crafting_open = False
                        self.inventory_open = not self.inventory_open
                    if e.key == pygame.K_c:
                        # abre/fecha crafting (fecha inventário se aberto)
                        if self.inventory_open:
                            self.inventory_open = False
                        self.crafting_open = not self.crafting_open

                    # navegação crafting
                    if self.crafting_open and self.recipes_list:
                        if e.key in (pygame.K_UP, pygame.K_w):
                            self.craft_ui.move_sel(-1, len(self.recipes_list))
                        if e.key in (pygame.K_DOWN, pygame.K_s):
                            self.craft_ui.move_sel(+1, len(self.recipes_list))
                        if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            rid, name, rarity, inputs = self.recipes_list[self.craft_ui.sel]
                            ok, _ = can_craft(self.world.player.inv, self.recipes, rid, qty=1)
                            if ok:
                                ok2, msg = craft(self.world.player.inv, self.recipes, rid, qty=1)
                                self.show_toast(msg)
                                # recarrega lista (quantidades mudaram, mas receitas em si não)
                            else:
                                self.show_toast("Faltam recursos para craftar.")

            if self.state == "menu":
                self.menu.draw(self.screen)
                pygame.display.flip()
                continue

            # pausa se inventário OU crafting estiverem abertos
            paused = self.inventory_open or self.crafting_open
            self.world.update(dt, events, paused=paused)

            # CÂMERA
            target_x = self.world.player.rect.centerx - WIDTH // 2
            target_y = self.world.player.rect.centery - HEIGHT // 2
            target_x = max(0, min(target_x, self.world.width - WIDTH))
            target_y = max(0, min(target_y, self.world.height - HEIGHT))
            self.cam_x += (target_x - self.cam_x) * 0.15
            self.cam_y += (target_y - self.cam_y) * 0.15
            camera = (self.cam_x, self.cam_y)

            # DRAW
            self.screen.fill(COLOR_BG)
            self.world.draw(self.screen, camera)
            self.hud.draw(self.screen, self.world.player, toast_text=self.toast_text)

            if self.inventory_open:
                self.inv_ui.draw(self.screen, self.world.player)
            if self.crafting_open:
                # passa uma função que verifica se dá para craftar (inv + recipe)
                def _can(inv, rid, q=1):
                    return can_craft(inv, self.recipes, rid, q)
                self.craft_ui.draw(self.screen, self.recipes_list, self.world.player, _can)

            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
