import MonsterGenerator
import WeaponManager
from random import randint

"""moznaby gzies dodac jeszcze ilosc atakow na runde do tego rzutu na atak"""

class AnyCharacter:
    """Class containing any playable and non-playable creatures."""

    def __init__(self, name, race="unknown", profession="unknown"):
        self.name = name
        self.race = race
        self.profession = profession



class NPCharacter(AnyCharacter):
    """Class containing non-playable characters."""

    def __repr__(self):
        return "NPC"


class PlayerCharacter(AnyCharacter):

    def __init__(self, name):
        super().__init__(name)  # , race, class

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

    ad_dmg_bonus = []  # from skills and feats, potem trzeba dodac tutaj tez z siły
    ad_atk_bonus = []

    base_speed = 10
    hitpoints = 10
    armorclass = 10

    base_attack_bonus = 1
    weapon = WeaponManager.SimpleWeapon.create("club")

    spells = {
        1: ["Bless", "Cure wounds", "Sanctuary"],
    }

    if "Weapon Finesse" not in feats:
        attack_bonus = base_attack_bonus + stat_bonus["STR"]
    else:
        attack_bonus = base_attack_bonus + stat_bonus["DEX"]

    # attack_bonus = ["1d20", attack, feats]


"""najpierw rzucasz k20 na atak, jak rzut + BAB+ str > AC to trafienie,
 jesli sam rzut jest powyzej crit range to kolejny rzut k20 i jesli trafienie to rzut na dmg 2x
 rzut na dmg z broni + stat_bonus["STR] """

Joe = PlayerCharacter("Joe")
orc = MonsterGenerator.Monster("orc")


def attack_roll(char, target):
    roll = randint(1, 20)
    attack_chance = roll + char.attack_bonus
    final_dmg = 0
    if roll >= char.weapon.crit_range and attack_chance > target.armorclass:
        print(f"Obrona celu: {target.armorclass}. Rzut 1d20: {roll}. Cios krytyczny!")
        confirm_roll = randint(1, 20)
        crit_confirm = confirm_roll + char.attack_bonus  # +char.crit_multiplier_bonus
        if crit_confirm >= target.armorclass:
            #  for hit in range(char.crit_multiplier_bonus):
                #  dmg_roll = char.weapon.rolldice() + char.stat_bonus["STR"]
                #  final_dmg += dmg_roll
            dmg1 = char.weapon.rolldice() + char.stat_bonus["STR"]
            dmg2 = char.weapon.rolldice() + char.stat_bonus["STR"]
            final_dmg += dmg1 + dmg2
            print(f"Potwierdzenie 1d20: {confirm_roll} Trafienie krytyczne! Calkowie obrazenia: {final_dmg}\n")
            return final_dmg
        else:
            print(f"Potwierdzenie trafienia krytycznego: {crit_confirm}. Krytyczne obrazenia nie siegnely celu.\n")
    if attack_chance > target.armorclass:
        print(f"Obrona celu: {target.armorclass}. Rzut 1k20: {roll}. Trafienie.")
        dmg = char.weapon.rolldice() + char.stat_bonus["STR"]
        final_dmg += dmg
        print(f"Calkowie obrazenia: {final_dmg}")
        return final_dmg
    else:
        print(f"Obrona celu: {target.armorclass}. Rzut 1k20: {roll}. Calkowite obrazenia: {final_dmg}\n")
        return final_dmg


attack_roll(Joe, orc)
