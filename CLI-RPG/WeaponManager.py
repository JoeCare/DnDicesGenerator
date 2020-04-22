from random import randint


class Weapon():
    """Main class for the all kind of weaponry in D&D"""

    # roboczo, bo trzeba bedzie dodac do kazdej:
    crit_range = 19

    def __init__(self, kind, price, damage, dmgtype, weight, weapontype, *otherfeats):
        self.kind = kind  # 1
        self.price = price  # 2
        self.damage = damage  # 3
        self.dmgtype = dmgtype  # 4
        self.weight = weight  # 5
        self.weapontype = weapontype  # 6
        self.otherfeats = otherfeats  # 7

    def __repr__(self):
        return f"{self.kind}-style {self.dmgtype} weapon, probably " \
            f"{self.price} worth, and weighing about {self.weight}. " \
            f"Other info: {self.weapontype}, damage: {self.damage}, " \
            f"critical range: {self.crit_range}/20, {self.otherfeats}"

    def __str__(self):
        return f"This weapon looks just like any other {self.kind}."



    def rolldice(self):
        z = self.kind
        total = 0
        dam = list(self.damage)
        if len(dam) <= 1:
            return 1
        x = int(dam[0])
        y = int(dam[2])
        if len(dam) >= 4:
            y = int(str(y) + dam[3])
        for n in range(x):
            roll = (randint(1, y))
            total += roll
        print(f'Obrażenia dla broni {z}: {x}k{y}. Rzut: {total}.')
        return total

    @classmethod
    def from_string(cls, weap_str):
        kind, price, damage, dmgtype, weight, weapontype, *otherfeats = weap_str.split(",")
        return cls(kind, price, damage, dmgtype, weight, weapontype, *otherfeats)


class SimpleWeapon(Weapon):

    @staticmethod
    def create(kind):
        new_weapon = ""
        with open("SimpleWeapon.txt", "r") as f:
            for line in f.readlines():
                k, *x = line.split(",")
                if k == kind:
                    new_weapon = Weapon.from_string(line)
                    return new_weapon
                else:
                    continue
            if new_weapon == "":
                raise ValueError(f'No "{kind}" weapon in database.')



class SimpleRangedWeapon(Weapon):

    @staticmethod
    def create(kind):
        new_weapon = ""
        with open("SimpleRangedWeapon.txt", "r") as f:
            for line in f.readlines():
                k, *x = line.split(",")
                if k == kind:
                    new_weapon = Weapon.from_string(line)
                    return new_weapon
                else:
                    continue
            if new_weapon == "":
                raise ValueError(f'No "{kind}" weapon in database.')


class MartialWeapon(Weapon):

    @staticmethod
    def create(kind):
        new_weapon = ""
        with open("MartialWeapon.txt", "r") as f:
            for line in f.readlines():
                k, *x = line.split(",")
                if k == kind:
                    new_weapon = Weapon.from_string(line)
                    return new_weapon
                else:
                    continue
            if new_weapon == "":
                raise ValueError(f'No "{kind}" weapon in database.')

class MartialRangedWeapon(Weapon):

    @staticmethod
    def create(kind):
        new_weapon = ""
        with open("MartialRangedWeapon.txt", "r") as f:
            for line in f.readlines():
                k, *x = line.split(",")
                if k == kind:
                    new_weapon = Weapon.from_string(line)
                    return new_weapon
                else:
                    continue
            if new_weapon == "":
                raise ValueError(f'No "{kind}" weapon in database.')


# #
# crossbow = MartialRangedWeapon.create("heavy crossbow")
# crossbow.rolldice()
