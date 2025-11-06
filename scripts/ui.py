import pygame
from settings import WIDTH, HEIGHT, COLOR_HUD, COLOR_ACCENT, COLOR_BG, ITEM_META, RARITY_COLOR


class StartScreen:
    def __init__(self, font):
        self.font = font
        self.title = "Remnants of Hope — MVP"
        self.sub = "Pressione ENTER para começar"

    def draw(self, surface):
        surface.fill(COLOR_BG)
        t = self.font.render(self.title, True, COLOR_HUD)
        s = self.font.render(self.sub, True, COLOR_HUD)
        surface.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 40))
        surface.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT // 2 + 4))


class HUD:
    def __init__(self, font):
        self.font = font

    def draw(self, surface, player, toast_text=None):
        # status sprint
        if player.exhausted and player.stamina < player.stamina_max * player.reactivate_ratio:
            sprint_status = "Sprint: AGUARDE 40%"
        else:
            sprint_status = "Sprint: ON" if player.sprint_active else "Sprint: OFF"

        tip = self.font.render(
            f"WASD/Setas: mover | Tab: inventário | C: crafting | Shift: alterna corrida | {sprint_status}",
            True, COLOR_HUD
        )
        surface.blit(tip, (16, 12))

        # barra de stamina
        bar_w, bar_h = 220, 16
        x, y = 16, 40
        pygame.draw.rect(surface, (80, 80, 92), (x, y, bar_w, bar_h), border_radius=6)
        fill = int(bar_w * (player.stamina / player.stamina_max))
        pygame.draw.rect(surface, COLOR_ACCENT, (x, y, fill, bar_h), border_radius=6)
        st = self.font.render("Stamina", True, COLOR_HUD)
        surface.blit(st, (x + bar_w + 8, y - 2))

        # mini-inventário (resumo)
        base_y = 70
        items = player.inv.as_list()
        if not items:
            surface.blit(self.font.render("Inventário: (vazio)", True, COLOR_HUD), (16, base_y))
        else:
            surface.blit(self.font.render("Inventário (resumo):", True, COLOR_HUD), (16, base_y))
            for i, (k, v) in enumerate(items[:4], start=1):
                name = ITEM_META.get(k, {}).get("name", k)
                line = self.font.render(f"• {name}: {v}", True, COLOR_HUD)
                surface.blit(line, (16, base_y + i * 22))

        # toast (mensagem rápida)
        if toast_text:
            box = self.font.render(toast_text, True, (255, 255, 255))
            surface.blit(box, (16, HEIGHT - 28))


class InventoryUI:
    def __init__(self, font):
        self.font = font
        self.pad = 18
        self.w = int(WIDTH * 0.7)
        self.h = int(HEIGHT * 0.7)
        self.x = (WIDTH - self.w) // 2
        self.y = (HEIGHT - self.h) // 2

    def draw(self, surface, player):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        panel = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        panel.fill((22, 24, 28, 235))
        pygame.draw.rect(panel, (255, 255, 255), (0, 0, self.w, self.h), width=2, border_radius=8)

        title = self.font.render("Inventário", True, COLOR_HUD)
        panel.blit(title, (self.pad, self.pad))

        hint = self.font.render("Tab/ESC: fechar", True, (200, 200, 200))
        panel.blit(hint, (self.pad, self.pad + 26))

        items = player.inv.as_list()
        if not items:
            panel.blit(self.font.render("(vazio)", True, (190, 190, 190)), (self.pad, self.pad + 60))
        else:
            y0 = self.pad + 60
            for (key, qty) in items:
                meta = ITEM_META.get(key, {"name": key, "rarity": "comum"})
                name = meta.get("name", key)
                rarity = meta.get("rarity", "comum")
                color = RARITY_COLOR.get(rarity, (220, 220, 220))
                line = self.font.render(f"{name}  x{qty}", True, color)
                panel.blit(line, (self.pad, y0))
                y0 += 24

        surface.blit(panel, (self.x, self.y))


class CraftingUI:
    def __init__(self, font):
        self.font = font
        self.pad = 18
        self.w = int(WIDTH * 0.72)
        self.h = int(HEIGHT * 0.74)
        self.x = (WIDTH - self.w) // 2
        self.y = (HEIGHT - self.h) // 2
        self.sel = 0  # índice selecionado na lista

    def move_sel(self, delta, total):
        if total <= 0: 
            self.sel = 0
        else:
            self.sel = (self.sel + delta) % total

    def draw(self, surface, recipes_list, player, can_craft_fn):
        # overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        # painel
        panel = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        panel.fill((22, 24, 28, 235))
        pygame.draw.rect(panel, (255, 255, 255), (0, 0, self.w, self.h), width=2, border_radius=8)

        title = self.font.render("Crafting", True, COLOR_HUD)
        panel.blit(title, (self.pad, self.pad))

        hint = self.font.render("C/ESC: fechar  |  ↑/↓: navegar  |  Enter: fabricar", True, (200, 200, 200))
        panel.blit(hint, (self.pad, self.pad + 26))

        # lista de receitas
        if not recipes_list:
            panel.blit(self.font.render("(nenhuma receita encontrada)", True, (190, 190, 190)),
                       (self.pad, self.pad + 64))
        else:
            y0 = self.pad + 64
            for i, (rid, name, rarity, inputs) in enumerate(recipes_list):
                ok, _ = can_craft_fn(player.inv, rid, 1)
                base_color = RARITY_COLOR.get(rarity, (220, 220, 220))
                color = base_color if ok else (130, 130, 130)

                prefix = "➤ " if i == self.sel else "   "
                line = self.font.render(f"{prefix}{name}", True, color)
                panel.blit(line, (self.pad, y0))

                # insumos
                y0 += 22
                need_texts = []
                for k, v in inputs.items():
                    have = player.inv.items.get(k, 0)
                    need_name = ITEM_META.get(k, {}).get("name", k)
                    need_texts.append(f"{need_name}: {have}/{v}")
                need_line = self.font.render("   " + "  |  ".join(need_texts), True, (200, 200, 200))
                panel.blit(need_line, (self.pad, y0))
                y0 += 28

        surface.blit(panel, (self.x, self.y))
