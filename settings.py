# =============================
# FILE: settings.py
# =============================

WIDTH, HEIGHT = 960, 540
FPS = 60
TILE = 32

# Cores
COLOR_BG = (18, 18, 22)
COLOR_FLOOR = (40, 44, 52)
COLOR_WALL = (85, 90, 105)
COLOR_PLAYER = (64, 185, 255)
COLOR_HUD = (235, 235, 235)
COLOR_ACCENT = (120, 220, 120)

# Mapa básico (grid)
MAP_LAYOUT = [
    "############################",
    "#..........#...............#",
    "#..######..#..######..###..#",
    "#..#....#..#..#....#..#....#",
    "#..#....#..#..#....#..#....#",
    "#..#....#..#..#....#..#....#",
    "#..##..##..#..######..#....#",
    "#...........P..............#",
    "#..######..#..######..###..#",
    "#..#....#..#..#....#..#....#",
    "#..#....#..#..#....#..#....#",
    "#..######..#..######..#....#",
    "#..........................#",
    "############################",
]

# ... (suas constantes atuais permanecem)

# Paleta de raridade (para UI e recursos)
RARITY_COLOR = {
    "comum": (180, 180, 180),
    "intermediario": (120, 180, 255),
    "raro": (255, 215, 120),
}

# (Opcional) metadados simples de itens para UI (nome + raridade)
ITEM_META = {
    "madeira":           {"name": "Madeira",            "rarity": "comum"},
    "sucata_metal":      {"name": "Sucata de metal",    "rarity": "comum"},
    "parafusos_pregos":  {"name": "Parafusos e pregos", "rarity": "comum"},
    "fios_eletricos":    {"name": "Fios elétricos",     "rarity": "comum"},
    "placas_metalicas":  {"name": "Placas metálicas",   "rarity": "intermediario"},
    "placa_circuito":    {"name": "Placa de circuito",  "rarity": "intermediario"},
    "pilhas":            {"name": "Pilhas/baterias",    "rarity": "intermediario"},
    "antibioticos":      {"name": "Antibióticos",       "rarity": "raro"},
    "kit_medico":        {"name": "Kit médico",         "rarity": "raro"},
}
