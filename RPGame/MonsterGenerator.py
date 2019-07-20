class Monster():

    def __init__(self, kind):
        self.kind = kind

    base_stats = {
        "STR": 10,
        "DEX": 10,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10
    }
    stat_bonus = {
        "STR": 0,
        "DEX": 0,
        "CON": 0,
        "INT": 0,
        "WIS": 0,
        "CHA": 0
    }
    skills = {}
    feats = []

    base_speed = 10
    hitpoints = 10
    armorclass = 10

    base_attack_bonus = 1

    spells = {
        1: ["Bless", "Cure wounds", "Sanctuary"],
    }

    if "Weapon Finesse" not in feats:
        attack = base_attack_bonus + stat_bonus["STR"]
    else:
        attack = base_attack_bonus + stat_bonus["DEX"]
