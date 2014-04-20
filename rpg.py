# DECORATOR, INHERITANCE, COMPOSITION

import random
from time import sleep

# Character is the base class, or parent
class Character(object):
    NAME = 'Anonymous'
    HEALTH = 100
    MIN_DAMAGE_POINTS = 0
    MAX_DAMAGE_POINTS = 0

    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.NAME = kwargs['name']
        if 'health' in kwargs:
            self.HEALTH = kwargs['health']
        if 'max_damage_points' in kwargs:
            self.MIN_DAMAGE_POINTS = kwargs['min_damage_points']
        if 'min_damage_points' in kwargs:
            self.MAX_DAMAGE_POINTS = kwargs['max_damage_points']

    def __str__(self):
        return self.NAME + " hp: " + str(self.HEALTH) + " dp: " + str(self.MAX_DAMAGE_POINTS)

    def attack(self, character):
        if character.HEALTH > 0:
            damage = random.randint(self.MIN_DAMAGE_POINTS, self.MAX_DAMAGE_POINTS)
            character.HEALTH -= damage
            print self.NAME + " hit " + character.NAME + " by " + str(damage) + " damage points!"
            if character.HEALTH <= 0:
                print character.NAME + " PWNED!"

# The Barbarian is focused more on damage
class Barbarian(Character):
    MIN_DAMAGE_POINTS = 85
    MAX_DAMAGE_POINTS = 100

# The Archer is keen and quick
class Archer(Character):
    HEALTH = 90
    MIN_DAMAGE_POINTS = 50
    MAX_DAMAGE_POINTS = 100

# The Warlord is vulnerable
class Warlord(Character):
    HEALTH = 100
    MAX_DAMAGE_POINTS = 100
    MIN_DAMAGE_POINTS = MAX_DAMAGE_POINTS

# The Paladin is lighthearted
class Paladin(Character):
    MIN_DAMAGE_POINTS = 50
    MAX_DAMAGE_POINTS = 75

    def attack(self, character):
        if random.randint(0, 10) % 2 is 0:
            super(Paladin, self).attack(character)
            if random.randint(0, 10) % 2 is 0:
                print self.NAME + " heals self."
                self.__heal__(self)
        else:
            print self.NAME + " shows mercy to " + character.NAME
            if random.randint(0, 10) % 2 is 0:
                print self.NAME + " heals " + character.NAME
                self.__heal__(character)

    def __heal__(self, character):
        character.HEALTH += random.randint(0, 100)

    def healSelf(self):
        self.__heal__(self)

    def healEnemy(self, character):
        self.__heal__(character)

# The Samurai has high speed, mobility and strength
class Samurai(Character):
    def __init__(self, **kwargs):
        self.MIN_DAMAGE_POINTS = 80
        self.MAX_DAMAGE_POINTS = 99
        Character.__init__(self, **kwargs)

    def attack(self, character):
        if random.randint(0, 10) % 2 != 0:
            super(Samurai, self).attack(character)
        else:
            print self.NAME + " is confused. Commits harakiri!"
            super(Samurai, self).attack(self)

#The Game Handler
class Game(object):
    # Game Modes
    # 0 - Spectator Mode  1 - Turn Based (User)
    # 2 - Showdown
    GAME_MODE = 0
    ROSTERS = ['Katniss', 'Rues', 'Phil', 'Peta', 'Shem',
               'Lass', 'Cloud', 'Linus', 'Steve', 'Bill']

    def __init__(self, **kwargs):
        if 'game_mode' in kwargs:
            self.GAME_MODE = kwargs['game_mode']

    def start(self):
        if self.GAME_MODE is 0:
            self.mode_spectator()
        return

    def mode_spectator(self):
        team_a = []
        team_b = []
        fallen = []

        #random team selection
        job = 0
        while len(team_a) < 5:
            roster = random.choice(self.ROSTERS)
            team_a.append(self.create_character(job, roster))
            self.ROSTERS.remove(roster)
            job += 1
        job = 0
        while len(team_b) < 5:
            roster = random.choice(self.ROSTERS)
            team_b.append(self.create_character(job, roster))
            self.ROSTERS.remove(roster)
            job += 1

        print team_a, ' vs ',
        print team_b
        print

        #attack
        turn = 0
        while len(fallen) < 9:
            if not team_a:
                break
            if not team_b:
                break
            player_a = random.choice(team_a)
            player_b = random.choice(team_b)
            if turn == 0:
                player_a.attack(player_b)
                print player_b
                if (player_b.HEALTH <= 0):
                    team_b.remove(player_b)
                    fallen.append(player_b)
                turn = 1
            elif turn == 1:
                player_b.attack(player_a)
                print player_a
                if (player_a.HEALTH <= 0):
                    team_a.remove(player_a)
                    fallen.append(player_a)
                turn = 0
            print
            sleep(0.5)
        
        print "Our victor,",
        if turn == 1:
            print str(team_a[0].NAME) + "!"
            print "Team A Wins!"
        else:
            print str(team_b[0].NAME) + "!"
            print "Team B Wins!"
        return

    def create_character(self, job, _name):
        if job == 0:
            return Barbarian(name=_name)
        elif job == 1:
            return Archer(name=_name)
        elif job == 2:
            return Samurai(name=_name)
        elif job == 3:
            return Paladin(name=_name)
        elif job == 4:
            return Warlord(name=_name)