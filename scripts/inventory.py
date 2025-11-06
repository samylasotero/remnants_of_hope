class Inventory:
    def __init__(self):
        self.items = {}  # { "madeira": 3, "ferro": 1 }

    def add(self, key, qty=1):
        self.items[key] = self.items.get(key, 0) + qty

    def as_list(self):
        # retorna lista ordenada por nome da key
        return sorted(self.items.items(), key=lambda kv: kv[0])
