import WeaponManager
from random import randint
from time import sleep


"""moznaby gzies dodac jeszcze ilosc atakow na runde do tego rzutu na atak"""


class AnyCharacter:
    """Class containing any playable and non-playable creatures."""

    def __init__(self, name, race="unknown", profession="unknown"):
        self.name = name
        self.race = race
        self.profession = profession


class Monster(AnyCharacter):
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

    belongings = [["food", "apple"], ["food", "carrot"]]
    equipment = {
        "Head": "",
        "Chest": "",
        "Right hand": "",
        "Left hand": "",
        "Left foot": "",
        "Right foot": "",
        "Legs": "",
    }

    ad_dmg_bonus = []  # from skills and feats, potem trzeba dodac tutaj tez z siły
    ad_atk_bonus = []

    base_speed = 10
    max_hitpoints = 10
    hp = max_hitpoints
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

    max_stamina = base_stats["CON"] / 2
    current_stamina = int(max_stamina)
    warmth = 10 + base_stats["CON"]


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

    belongings = [["food", "apple"], ["food", "carrot"]]
    equipment = {
        "Head": "",
        "Chest": "",
        "Right hand": "",
        "Left hand": "",
        "Left foot": "",
        "Right foot": "",
        "Legs": "",
    }

    ad_ac_bonus = []
    ad_dmg_bonus = []  # from skills and feats, potem trzeba dodac tutaj tez z siły
    ad_atk_bonus = []

    base_speed = 10
    max_hitpoints = 10
    hp = max_hitpoints
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

    max_stamina = base_stats["CON"] // 2
    current_stamina = max_stamina
    warmth = 10 + base_stats["CON"]

    random_encounters = []
    # attack_bonus = ["1d20", attack, feats]


def attack_roll(char, target):
    roll = randint(1, 20)
    attack_chance = roll + char.attack_bonus
    final_dmg = 0
    if attack_chance > target.armorclass:
        print(f"Obrona celu {target.name}: {target.armorclass}. Rzut 1k20: {roll}. Trafienie.")
        dmg = char.weapon.rolldice() + char.stat_bonus["STR"]
        final_dmg += dmg
        print(f"Calkowie obrazenia: {final_dmg}")
        return final_dmg
    else:
        print(f"Obrona celu: {target.armorclass}. Rzut 1k20: {roll}. Calkowite obrazenia: {final_dmg}\n")
        return final_dmg


# MAP BUILDING:
# ______________________ :
def gen_map():
    map = []
    for num in range(10):
        map.append([" "] * 30)
    for line in map:
        line[0] = "."
        line[len(line) - 1] = "."
    for n in range(30):
        map[0][n] = "."
        map[len(map) - 1][n] = "."
    map[5][15] = "X"
    return map


def prnt_map(sample):
    for line in sample:
        print("".join(line))


# player position indicator
def player_position(sample):
    for line in sample:
        for item in line:
            if "X" in item:
                x = sample.index(line)
                y = line.index(item)
                result = [x, y]
    return result


def exit_point(sample="coordinates"):
    """function called to make an exit from the maze
    if used as an argument it returns exit coordinates (but this don't really work yet, cuz
    then it still creates new exit poits in the random places whenewer called...
    besides there is that little bug here with [] which I don't understand.
    """
# if sample != "coordinates":
    randomizer = randint(1, 4)
    rand_x = randint(1, 9)
    rand_y = randint(1, 28)
    if randomizer == 1 and sample[1][rand_y] == " ":
        sample[0][rand_y] = "#"
    elif randomizer == 2 and sample[len(sample) - 2][rand_y] == " ":
        sample[len(sample) - 1][rand_y] = "#"
    elif randomizer == 3 and sample[rand_x][1] == " ":
        sample[rand_x][0] = "#"
    elif randomizer == 4 and sample[rand_x][len(sample[0]) - 2] == " ":
        sample[rand_x][len(sample[0]) - 1] = "#"
    else:
        exit_point(sample)
        print("2nd map gen")
# else:
    for line in sample:
        for item in line:
            if "#" in item:
                x = sample.index(line)
                y = line.index(item)
                exit_coordinates = [x, y]
                return exit_coordinates


def walls_first(sample):
    for num in range(1, 30):
        x = randint(2, len(sample) - 2)
        y = randint(2, len(sample[0]) - 3)
        if sample[x][y] == " " and sample[x].count("_") <= 0 and sample[x + 1].count("_") <= 0 \
                and sample[x - 1].count("_") <= 0:  # never in the same line!
            sample[x][y] = "_"


def walls_second(sample):
    walls_count = 0
    for line in sample:
        for item in line:
            if "_" in item:
                # print("indexline: ", sample.index(line))
                if sample.index(line) > 0:
                    walls_count += 1
                vx = sample.index(line)  # np linijka 2
                vy = line.index("_") + line.count("_")  # np kolumna 28
                vy1 = line.index("_")  # np kolumna 24
                # print(vx, vy, vy1)
                randomint = randint(1, 10)
                ran = randint(1, 2)
                if randomint == 1 and sample[vx][vy] == " ":
                    sample[vx][vy] = "|"
                    if ran == 1 and sample[vx - 1][vy] == " ":
                        sample[vx - 1][vy] = "|"
                    # print(line)
                elif randomint == 2 and sample[vx][vy1] == " ":
                    sample[vx][vy1] = "|"
                    if ran == 1 and sample[vx + 1][vy] == " ":
                        sample[vx + 1][vy] = "|"
                elif randomint == 3 and sample[vx + 1][vy1] == " ":
                    sample[vx + 1][vy1] = "|"
                # elif i titakj mozna dac mase kombinacji od 1-10 czy bedxie sample[vx][vy] = "|" czy "_", a potem
                # tak samo dla vx +1 i -1... moze sie uda.. ale to juz nie jest tak istotne :))
                elif randomint == 4 and sample[vx + 1][vy] == " ":
                    sample[vx + 1][vy] = "|"
                    # if sample[vx][vy + 1] == " ":
                    #     sample[vx][vy + 1] = "_"
                elif randomint >= 5 and sample[vx][vy1 - 1] == " ":
                    for iter in range(2):
                        sample[vx][vy1 - iter] = "_"
    return walls_count


def gen_walls(sample):
    for num in range(1, 30):
        x = randint(2, len(sample) - 2)
        y = randint(2, len(sample[0]) - 4)
        if sample[x][y] == " " and sample[x].count("_") <= 0 and sample[x + 1].count("_") <= 0 \
                and sample[x - 1].count("_") <= 0:  # never in the same line!
            sample[x][y] = "_"
            for m in range(1, 4):
                if sample[x][y + m] == " ":
                    sample[x][y + m] = "_"
            for n in range(1, 4):
                if sample[x][y - n] == " ":
                    sample[x][y - n] = "_"
    walls_second(sample)
    if walls_second(sample) < 20:
        walls_second(sample)
    return sample


def gen_moob(sample):
    for num in range(1, 30):
        x = randint(2, len(sample) - 2)
        y = randint(2, len(sample[0]) - 4)
        if sample[x][y] == " " and sample[x].count("m") <= 0 and sample[x + 1].count("m") <= 0 \
                and sample[x - 1].count("m") <= 0:  # never in the same line!
            sample[x][y] = "m"
    return sample


# ACTION function
# _________________ :
def action():
    # action_menu = []
    # for line in range(5):
    #     line = [" "]*5
    #
    # prnt_map(real_map)
    print("HP:", "/" * player.hp, " STAMINA:", "/" * player.current_stamina)
    prnt_map(visible_map)
    for line in visible_map:
        for item in line:
            if "m" in item:
                fight(player)

    actn = input("What do You want to do now?")
    if "wait" in actn:
        print("You decided to wait and gather your thoughts.")
        player.current_stamina += 1
    elif "search" in actn:
        print("You decided to try to look through the darkness "
              "as well as palpate with your hands to find anything useful.")
        if randint(1, 100) >= 50:
            print("You've found a torch! Now You can put some light on the scene..."
                  "\nIf You know how to light it up.")
    elif "move" in actn or "m" in actn:
        move(real_map, visible_map)
    elif "belongings" in actn or "b" in actn:
        use_items()
    else:
        print("So...?")
        action()


# MOVEMENT
# __________________ :
def movement_msg():
    move_msg = []
    for num in range(5):
        line = [" "] * 5
        move_msg.append(line)

    move_msg[0][2] = "MOVEMENT"
    # move_msg[0][0] = "_"
    move_msg[0][1] = "_"
    move_msg[0][3] = "_"
    # move_msg[0][4] = "_"
    move_msg[1][0] = "|"
    move_msg[2][0] = "|"
    move_msg[3][0] = "|"
    move_msg[4][0] = "|"
    move_msg[4][1] = "_"
    move_msg[4][2] = "_"
    move_msg[4][3] = "_"
    move_msg[4][4] = "|"
    move_msg[3][4] = "|"
    move_msg[2][4] = "|"
    move_msg[1][4] = "|"

    move_msg[1][2] = "W"
    move_msg[2][1] = "A"
    move_msg[2][3] = "D"
    move_msg[3][2] = "S"
    move_msg.insert(1, [" "] * 5)
    move_msg[1][0] = "|"
    move_msg[1][4] = "|"

    for num in range(6):
        move_msg[num].insert(0, " ")

    move_msg[0].pop(1)

    for line in move_msg:
        print("  ".join(line))


def move(sample, visible):
    movement_msg()
    direction = input("\nWhich direction?")
    x, y = player_position(sample)
    if "w" in direction or "W" in direction:
        if sample[x - 1][y] == " ":
            sample[x][y] = " "
            sample[x - 1][y] = "X"
            visible[x][y] = " "
            visible[x - 1][y] = "X"
            # prnt_map(visible)
            random_encounter()
        elif sample[x - 1][y] == "m":
            visible[x - 1][y] = "m"
            prnt_map(visible)
        else:
            visible[x - 1][y] = sample[x - 1][y]
            prnt_map(visible)
            print("Suddenly you start to feel cold on your face. "
                  "Dense forst hitted you hard. You came across the wall.")
            random_encounter("wall")
    elif "a" in direction or "A" in direction:
        if sample[x][y - 1] == " ":
            sample[x][y] = " "
            sample[x][y - 1] = "X"
            visible[x][y] = " "
            visible[x][y - 1] = "X"
            # prnt_map(visible)
            random_encounter()
        elif sample[x][y - 1] == "m":
            visible[x][y - 1] = "m"
            prnt_map(visible)
        else:
            visible[x][y - 1] = sample[x][y - 1]
            prnt_map(visible)
            print("Suddenly you start to feel cold on your face. "
                  "Dense forst hitted you hard. You came across the wall.")
            random_encounter("wall")
    elif "d" in direction or "D" in direction:
        if sample[x][y + 1] == " ":
            sample[x][y] = " "
            sample[x][y + 1] = "X"
            visible[x][y] = " "
            visible[x][y + 1] = "X"
            # prnt_map(visible)
            random_encounter()
        elif sample[x][y + 1] == "m":
            visible[x][y + 1] = "m"
            prnt_map(visible)
        else:
            visible[x][y + 1] = sample[x][y + 1]
            prnt_map(visible)
            print("Suddenly you start to feel cold on your face. "
                  "Dense forst hitted you hard. You came across the wall.")
            random_encounter("wall")
    elif "s" in direction or "S" in direction:
        if sample[x + 1][y] == " ":
            sample[x][y] = " "
            sample[x + 1][y] = "X"
            visible[x][y] = " "
            visible[x + 1][y] = "X"
            # prnt_map(visible)
            random_encounter()
        elif sample[x + 1][y] == "m":
            visible[x + 1][y] = "m"
            prnt_map(visible)
        else:
            visible[x + 1][y] = sample[x + 1][y]
            prnt_map(visible)
            print("Suddenly you start to feel cold on your face. "
                  "Dense forst hitted you hard. You came across the wall.")
            random_encounter("wall")
    else:
        restin = input("You decided to rest a bit?")
        if "y" in restin:
            return sample
        if "n" in restin:
            print("So make your mind!")
            move(sample, visible)


# GAMEPLAY functions (special actions after game starts)
# __________________ :

# function which adds objects onto the map during the game
# # needs created instances of real and visible_map

def change_map_LR(object="unknown"):
    """function that puts objects onto the random position 3 steps from the
      player current position on the left or right"""
    letter, *rest = object.lower()  # needed for the real map to know how to react when player steps on it (item/moob)
    x1, y1 = player_position(real_map)
    x2, y2 = player_position(visible_map)
    y_left = -1
    y_right = 1
    if "torch" in object:
        for n in range(1, 5):
            if real_map[x1][y1 + n] != " ":
                break
            elif real_map[x1][y1 + n] == " ":
                y_right += 1
            # print("right: ", y_right)
        for m in range(1, 5):
            if real_map[x1][y1 - m] != " ":
                break
            elif real_map[x1][y1 - m] == " ":
                y_left -= 1
        #     print("left: ", y_left)
        # print(":", y_right, y_left)
        if abs(y_left) > abs(y_right) and abs(y_left) >= 3:
            real_map[x1][y1 + y_left] = letter
            visible_map[x2][y2 + y_left] = "?"
            print("*Suddenly you realized that rocks, created in your imagination along with their humble\n"
                  "mountain, rolled straight to your left.*")
        elif abs(y_right) > abs(y_left) and abs(y_right) >= 3:
            real_map[x1][y1 + y_right] = letter
            visible_map[x2][y2 + y_right] = "?"
            print("*Suddenly you realized that rocks, created in your imagination along with their humble\n"
                  "mountain, rolled straight to your right.*")
        elif abs(y_right) == abs(y_left) >= 3:
            ran = randint(1, 2)
            if ran == 1:
                real_map[x1][y1 + y_left] = letter
                visible_map[x2][y2 + y_left] = "?"
                print("*Suddenly you realized that rocks, created in your imagination along with their humble\n"
                      "mountain, rolled straight to your left.*")
            elif ran == 2:
                real_map[x1][y1 + y_right] = letter
                visible_map[x2][y2 + y_right] = "?"
                print("*Suddenly you realized that rocks, created in your imagination along with their humble\n"
                      "mountain, rolled straight to your right.*")
    elif object == "unknown":
        pass
        # for n in range(1, 5):
        #     if real_map[x1][y1 + n] != " ":
        #         break
        #     elif real_map[x1][y1 + n] == " ":
        #         y_right += 1
        #     # print("right: ", y_right)
        # for m in range(1, 5):
        #     if real_map[x1][y1 - m] != " ":
        #         break
        #     elif real_map[x1][y1 - m] == " ":
        #         y_left -= 1
        # moob = MonsterGenerator.Monster("Flesh Golem")
        # real_map[x1][y1 + y_right] = "m"
        # visible_map[x2][y2 + y_right] = "?"
    else:
        pass


# needs from time import sleep to work
# to the Actions file and into the action() funct
def random_encounter(kind='randomized'):  # player.luck as second input later
    plr_msg = "*What do you do?*"
    # end_pointless = "end"
    randomizer = randint(0, 10)
    if kind == "wall" and randomizer >= 7 and player.random_encounters.count("wall") == 0:
        print("\n - Watch your steps! - stony-cold voice came from nowhere.\n")
        player.random_encounters.append("wall")
        answer1 = input("*What do you do?*")
        if not answer1:
            print(" - Yup... It was nice to meet you... Moron. - Came form the void like another solid piece of\n"
                  "hard ice aimed right in your head leaving known already silence of that lands.\n")
        elif "sorry" not in answer1.lower() and "apologize" not in answer1.lower():
            print("\n - Hey you! I'm talking to you. If not in the mood for a chat it would be just polite\n"
                  "to at least say 'sorry'. - Words sounding like falling rocks brayed your brain.\n")
            answer1_1 = input(f'{plr_msg}')
            if not answer1_1:
                print(" - Yup... It was nice to meet you... Moron. - Came form the void like another solid piece of\n"
                      "hard ice aimed right in your head leaving known already silence of that lands.\n")
            elif "sorry" not in answer1_1.lower and "apologize" not in answer1_1.lower():
                print("\n - Phff! Uncivilized pricks... - Came form the void like another solid piece of\n"
                      "hard ice aimed right in your head leaving known already silence of that lands.\n")
            else:
                print("\n - It's okay. It happens all the time. It's probably of that shitass darkness all around"
                      "...\nIf they'd give us some lanterns all would be much easier... - Words sounding like\n"
                      "rocks rolling from the steep hummock fell into your head.\n")
                answer1_2 = input("*What do You do?*")
                if not answer1_2:
                    print(" - Yup... It was nice to meet you... Moron. - Came form the void like another solid piece\n"
                          "of hard ice aimed right in your head leaving already known silence of that lands.\n")
                elif "light" in answer1_2 or "torch" in answer1_2.lower() or "lantern" in answer1_2.lower() \
                        or "fire" in answer1_2 or "bright" in answer1_2:
                    print("\n - I'm almost certain that one of the previous... visitors\n"
                          "came here with an irritating warmstick...\n")
                    answer1_2_1 = input(f'{plr_msg}')
                    if not answer1_2_1:
                        print("Void answers your muteness leaving you with already known silence of that lands.\n")
                    elif "where" in answer1_2_1.lower() or "go" in answer1_2_1 or "went" in answer1_2_1:
                        print("\n - Well... I think he's last sounds came from this direction... - Words sounding\n"
                              "like rocks falling from a steep hummock rolled through your head and the voice\n"
                              "fallen silent leaving you with arguably useful advice.\n")
                elif "where" in answer1_2.lower() and "you" in answer1_2.lower():
                    print("\n - Here. - Answered curtly as an uncuted stone. - You almost "
                          "stepped on me... You probably\nwould If You could...\n")
                    print("*Suddenly it came to you with another blow of the cold, moisty\nunderground"
                          "air... You are just talking to the wall. It seems pretty loony.\n"
                          "- Maybe I'll simply go now... - You've recognized your own polite voice peculiar\n"
                          "and immidiately added with even more frantic tone - Just thinking aloud...")
                elif "who" in answer1_2:
                    print("\n - Well... I'm Wall. Without superfluous coyness pretty solid one.\n")
                    answer1_2_2 = input(f'{plr_msg}')
                    if not answer1_2_2:
                        print("Void answers your muteness leaving you with already known silence of that lands.\n")
                    elif "nice" in answer1_2_2:
                        print("*Suddenly it came to you with another blow of the cold, moisty\nunderground"
                              "air... You are just talking to the wall. It seems pretty loony.\n"
                              "- Maybe I'll simply go now... - You've recognized your own polite voice peculiar\n"
                              "and immidiately added with even more frantic tone - Just thinking aloud...*")
        else:  # elif "sorry" in answer1.lower() or "apologize" in answer1.lower():
            print("\n - It's okay. It happens all the time. It's probably of that shitass darkness all around"
                  "...\nIf they'd give us some lanterns all would be much easier... - Words sounding like\n"
                  "rocks rolling from the steep hummock fell into your head.\n")
            answer2_2 = input("*What do You do?*")
            if not answer2_2:
                print("Void answers your muteness leaving you with already known silence of that lands.\n")
            elif "light" in answer2_2.lower() or "torch" in answer2_2.lower() or "lantern" in answer2_2.lower() \
                    or "fire" in answer2_2.lower():
                print("\n - Hmmm... Maybe I can help you... I'm almost certain that one of the previous... visitors\n"
                      "came here with that irritating warmstick...\n")
                # playerluck += 1
                answer2_3 = input(f'{plr_msg}')
                if not answer2_3:
                    print("Void answers your muteness leaving you with already known silence of that lands.\n")
                elif "where" in answer2_3.lower() or "more" in answer2_3:
                    print("\n - Sounds he made were even funnier than yours... - Opinion cold as a stone "
                          "echoed in your\n"
                          "head. - I think he were already lurking around for a while before he crossed me...\n"
                          "And I don't think he went too far from here...\n")
                    answer2_4 = input(f'{plr_msg}')
                    if not answer2_4:
                        print("Void answers your muteness leaving you with already known silence of that lands.\n")
                    elif "help" in answer2_4.lower() or "anything" in answer2_4.lower() or "more" in answer2_4.lower():
                        print("\n - Well... I think he's last sounds came from this direction... - Words sounding\n"
                              "like rocks falling from a steep hummock rolled through your head and the voice\n"
                              "fallen silent leaving you with arguably useful advice.\n")
                        change_map_LR("torch")
            elif "where" in answer2_2.lower() and "you" in answer2_2.lower():
                print("\n - Here. - Answered curtly as an uncuted stone. - You almost stepped on me... You probably\n"
                      "would If You could...\n")
                print("*Suddenly it came to you with another blow of the cold, moisty\nunderground"
                      "air... You are just talking to the wall. It seems pretty loony.\n"
                      "- Maybe I'll simply go now... - You've recognized your own polite voice peculiar\n"
                      "and immidiately added with even more frantic tone - Just thinking aloud...")
            elif "who" in answer2_2.lower() and "you" in answer2_2.lower():
                print("\n - Well... I'm Wall. Without superfluous coyness pretty solid one.\n")
                answer2_2_1 = input(f'{plr_msg}')
                if not answer2_2_1:
                    print("Void answers your muteness leaving you with already known silence of that lands.\n")
                elif "help" in answer2_2_1.lower() or "pretty" in answer2_2_1.lower() or "nice" in answer2_2_1.lower():
                    print("\n - Hmmm... Maybe I can help you... I'm almost certain that one of the previous... "
                          "visitors\ncame here with that irritating warmstick... I think his last sounds came from\n"
                          "this direction... - Words sounding like rocks falling from a steep hummock rolled\n"
                          "through your head and the voice fallen silent leaving you with arguably useful advice.\n")
                    change_map_LR("torch")
    elif kind == "wall1" and randomizer >= 7 and player.random_encounters.count("wall1") == 0:
        player.random_encounters.append("wall1")
    else:
        """function may be called without args at any moment in the game (every step?) 
        then it gives a player random chance to found something"""
        randomitem = randint(0, 10)
        if randomitem == 6:
            typ = "food"
            itm = "dried meat"
        elif randomitem == 7:
            typ = "armor"
            itm = "fur cap"
        elif randomitem == 8:
            typ = "armor"
            itm = "leather glove"
        elif randomitem == 9:
            typ = "weapon"
            itm = "dagger"
        elif randomitem == 10:
            typ = "food"
            itm = "bottle of water"
        else:
            itm = "only growing feeling of hopelessness"
            pass
        if kind == "randomized" and randomizer > 8:
            if not player.equipment.get("torch"):
                print("Groping among the darkness You almost triped over something on the ground...\n"
                      "You squat and search carefully through the rubble yet still hurting your palms\n"
                      "on the edges of few nasty stones.")
                player.hp -= 1
                for i in range(3):
                    sleep(1)
                    print(".")
                print(f"Finally you found: {itm}.")
                # if player.equipment.
                if randomitem >= 6:
                    player.belongings.append([typ, itm])
                    print(player.belongings)
            else:
                print("In the weak light of your torch you see a shape on the ground...\n"
                      "You squat and search carefully through the rubble yet still hurting your palms\n"
                      "on the edges of few nasty stones.")


def fight(player):
    moob = Monster("monster")
    print("Lurking through the darkness you almost stepped on... Someone else? Human shape appeared\n"
          "right before your eyes and it was to late for making decisions...")
    moob_dmg = attack_roll(moob, player)
    if moob_dmg > 0:
        player.hp -= moob_dmg
        print("Now you had a brief chance to see... Unnaturally slender arm ending with impressive talons\n"
              "sliced the air right before you... right before you had an another lucky chance to feel\n"
              "cold pain of your skin opening like germinating grain under soft touch of the water drop.")

    while moob.max_hitpoints > 0:
        plr_atk = input("You step back under the impact when involuntary hiss came from your mouth but the creature\n"
                        "also lost it's balance in the fierce attack. Now you've got a chance to strike back.\n")
        player_dmg = attack_roll(player, moob)
        moob.max_hitpoints -= player_dmg
        sleep(1)
        moob_dmg = attack_roll(moob, player)
        player.hp -= moob_dmg
        sleep(1)
        if player.hp <= 0:
            player_turn(player)
    print("Hideous shape barely seen in the dark fell before Your feet. You're alive.")
    player_turn(player)


def use_items():
    for itm in player.belongings:
        print(": ".join(itm))
    item = input("You can't always get what you want, but... What do you want from what you have?")
    for itm in player.belongings:
        if itm[1].count(item):
            print("Using chosen item.")
            sleep(1)


# not needed anymore; condition added to move function
# edit: nope, still needed. but i dont now how to put it into
# the playerturn while loop to work correctly
#
# this part from move() may be useful:
#         elif sample[x - 1][y] == "#":
#             visible[x - 1][y] = sample[x - 1][y]
#             prnt_map(visible)
#             print("WINNER!\nJust joking... You just found the exit from the little frigging deadly\n"
#                   "maze. Now it's time for the real shit*coughs*life.")


def win_check(visible):
    for line in visible:
        for item in line:
            if "#" in item:
                print("WINNER!\nJust joking... You just got out of the frigging deadly maze, now it's time\n"
                      "for the real shit*coughs*life.")
                return True


# it should be in Gameplay or Actions file so:
# from DungeonGame.Structure.Mobiles import *
def player_turn(player):
    """First function for the game?
    it needs defined Player class instance
    because it uses its inner variables."""

    if player.hp <= 0:
        print(f'{real_map} \nYou had to just get out of the place...\n '
              f'But you\'re dead now. Every living and non-living creatures - including\n'
              f'mostly the walls - will remember you and think about you fondly and...\n'
              f'or... maybe rather coolly... But thanks for the play anyways :)'
              f'\nExit form the maze was at #.')
    else:  # player not dead
        # pytaj, reaguj odpow, znow pytaj; trzeba wrzucic while do action()
        while player.current_stamina > 0:
            action()
            player.current_stamina -= 1
            if player.current_stamina != 0:
                continue
            print("You need to rest.")
            while player.current_stamina < player.max_stamina:
                sleep(1)
                player.current_stamina += 2
                print(".")


# GAME functions instances and making the game finally run
# _____________ :
#
player = PlayerCharacter("Joe")
real_map = gen_walls(gen_map())
visible_map = gen_map()
gen_moob(real_map)
exit_point(real_map)
prnt_map(real_map)
#
player_turn(player)
#
# win_check()