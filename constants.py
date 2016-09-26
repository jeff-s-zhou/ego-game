from enum import Enum
from typing import List


class Targets(Enum):
    self = 'self'
    single_enemy = 'single_enemy'
    enemy_frontline = 'enemy_frontline'
    enemy_backline = 'enemy_backline'
    all_enemies = 'all_enemies'
    single_ally = 'single_ally'
    ally_frontline = 'ally_frontline'
    ally_backline = 'ally_backline'
    all_allies = 'all_allies'
    all = 'all'


'''
SKILLS
'''

class SKILL_CONSTANT:
    id = ""
    name = ""
    valid_targets = []
    verb = ""
    tooltip = ""


class SLASH(SKILL_CONSTANT):
    id = 1
    name = 'Slash'
    valid_targets = [Targets.single_enemy]
    verb = 'attacks'
    tooltip = 'A basic cutting attack.'
    damage_multiplier = 50
    cooldown = 1
    balance_cost = 10


class PROTECT(SKILL_CONSTANT):
    id = 2
    name = 'Protect'
    valid_targets = [Targets.single_ally]
    verb = 'supports'
    tooltip = 'Cast Protected on target.'
    cooldown = 4
    balance_cost = 20


class HEAL(SKILL_CONSTANT):
    id = 3
    name = 'Heal'
    verb = 'heals'
    valid_targets = [Targets.single_ally]
    tooltip = 'Heal the target.'
    heal_amount = 100
    cooldown = 5
    balance_cost = 30


class ELECTRIC_THORN_BIND(SKILL_CONSTANT):
    id = 4
    name = 'Electric Thorn Bind'
    verb = 'curses'
    valid_targets = [Targets.single_enemy]
    tooltip = 'Casts Thorn Bound on target.'
    cooldown = 5
    balance_cost = 40
