import json
from pathlib import Path

# Este módulo NÃO tem dependências de pygame.
# Ele opera apenas sobre o inventário (player.inv), que deve ter:
#   - atributo dict: inv.items  (ex.: {"madeira": 3, "sucata_metal": 1})
#   - método: inv.add(key, qty=1)

# ----------------------------
# Carregamento de receitas
# ----------------------------

def load_recipes(path="data/recipes.json"):
    """
    Lê o arquivo JSON e retorna um dicionário de receitas:
    {
      "faca": {
        "name": "Faca",
        "rarity": "intermediario",
        "inputs": {"madeira": 1, "sucata_metal": 1}
      },
      ...
    }
    """
    p = Path(path)
    if not p.exists():
        # retorna vazio para o jogo não quebrar se o arquivo não existir
        return {}
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # normaliza chaves para string simples
    norm = {}
    for rid, rec in data.items():
        rid = str(rid).strip()
        rec = {
            "name": rec.get("name", rid),
            "rarity": rec.get("rarity", "comum"),
            "inputs": {str(k).strip(): int(v) for k, v in rec.get("inputs", {}).items()},
        }
        norm[rid] = rec
    return norm


# ----------------------------
# Utilidades de inventário
# ----------------------------

def inv_get(inv, key):
    """Quantidade atual do item no inventário."""
    return int(inv.items.get(key, 0))

def inv_consume(inv, key, qty):
    """Consome 'qty' do item. Não valida disponibilidade (veja can_craft)."""
    cur = inv.items.get(key, 0)
    cur -= qty
    if cur <= 0:
        inv.items.pop(key, None)
    else:
        inv.items[key] = cur


# ----------------------------
# Lógica de crafting
# ----------------------------

def can_craft(inv, recipes, recipe_id, qty=1):
    """
    Verifica se é possível craftar 'qty' unidades da receita 'recipe_id'.
    Retorna (ok: bool, faltantes: dict)
    - faltantes: {"madeira": 1, ...} com quantias que faltam (se ok=False)
    """
    rec = recipes.get(recipe_id)
    if not rec:
        return False, {"_erro": "receita_inexistente"}

    faltantes = {}
    for item_key, need in rec["inputs"].items():
        want = int(need) * int(qty)
        have = inv_get(inv, item_key)
        if have < want:
            faltantes[item_key] = want - have

    ok = (len(faltantes) == 0)
    return ok, faltantes

def craft(inv, recipes, recipe_id, qty=1):
    """
    Tenta craftar. Se possível:
      - consome insumos
      - adiciona o produto (mesma key da receita)
    Retorna (ok: bool, msg: str)
    """
    qty = int(qty)
    if qty <= 0:
        return False, "Quantidade inválida."

    rec = recipes.get(recipe_id)
    if not rec:
        return False, "Receita não encontrada."

    ok, faltantes = can_craft(inv, recipes, recipe_id, qty)
    if not ok:
        faltos = ", ".join(f"{k} x{v}" for k, v in faltantes.items())
        return False, f"Faltam recursos: {faltos}"

    # Consome insumos
    for item_key, need in rec["inputs"].items():
        inv_consume(inv, item_key, int(need) * qty)

    # Adiciona produto
    inv.add(recipe_id, qty)

    name = rec.get("name", recipe_id)
    return True, f"✅ Item criado: {name} x{qty}"

def list_recipes(recipes):
    """
    Retorna uma lista estável para UI:
      [(recipe_id, name, rarity, inputs_dict), ...]
    """
    out = []
    for rid, rec in recipes.items():
        out.append((rid, rec.get("name", rid), rec.get("rarity", "comum"), dict(rec.get("inputs", {}))))
    # ordena por nome
    out.sort(key=lambda t: t[1].lower())
    return out
