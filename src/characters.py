import points as pt
import collections
from graph import moveWithoutBreakingWalls
import time

barbarians = []
dragons = []
balloons = []
archers = []
stealth_archers = []
healers = []

troops_spawned = {
    'barbarian': 0,
    'archer': 0,
    'dragon': 0,
    'balloon': 0,
    # added below
    'stealth_archer' : 0,
    'healer' : 0,
}


def clearTroops():
    barbarians.clear()
    dragons.clear()
    balloons.clear()
    archers.clear()
    healers.clear()
    # added below
    stealth_archers.clear()
    troops_spawned['barbarian'] = 0
    troops_spawned['dragon'] = 0
    troops_spawned['balloon'] = 0
    troops_spawned['archer'] = 0
    troops_spawned['healer'] = 0
    # added below
    troops_spawned['stealth_archer'] = 0


class Barbarian:
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 1
        self.position = position
        self.alive = True
        self.target = None

    # change add here
    def check_new(self):
        return 0

    def move(self, pos, V, type):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r + c == 1):
            info = vmap[pos[0]][pos[1]]
            if(info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif type == 1:
            flag = 0
            for i in range(self.speed):
                coords = findPathWithoutWall(V.map, self.position, pos)
                if(coords == None):
                    flag = 1
                    break
                info = vmap[pos[0]][pos[1]]
                x = 0
                y = 0
                if(info != pt.TOWNHALL):
                    x = int(info.split(':')[1])
                    y = int(info.split(':')[2])
                else:
                    x = pos[0]
                    y = pos[1]
                if(x == coords[0] and y == coords[1]):
                    flag = 1
                    break
                self.position = coords
            if(flag == 0):
                return
        if(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] += 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] -= 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] += 1
                    if(self.position[0] == pos[0]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] -= 1
                    if(self.position[0] == pos[0]):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] += 1
                    if(self.position[1] == pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] -= 1
                    if(self.position[1] == pos[1]):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] += 1
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] -= 1

    def check_for_walls(self, x, y, vmap):
        if(vmap[x][y] == pt.WALL):
            return True
        return False

    def break_wall(self, x, y, V):
        target = V.wall_objs[(x, y)]
        self.attack_target(target)

    def break_building(self, x, y, V):
        target = None
        if(V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if(self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy()

    def kill(self):
        self.alive = False
        barbarians.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health


class Archer:
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 1
        self.attack_radius = 3
        self.position = position
        self.alive = True
        self.target = None

    # change add here
    def check_new(self):
        return 0

    def isInAttackradius(self,pos):
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r**2 + c**2 <= self.attack_radius**2):
            return True
        return False

    def move(self, pos, V, type):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(self.isInAttackradius(pos)):
            info = vmap[pos[0]][pos[1]]
            if(info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif type == 1:
            flag = 0
            for i in range(self.speed):
                coords = findPathWithoutWall(V.map, self.position, pos)
                if(coords == None):
                    flag = 1
                    break
                self.position = coords
            if(flag == 0):
                return
        if(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] += 1
                    if(self.isInAttackradius(pos)):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] -= 1
                    if(self.isInAttackradius(pos)):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] += 1
                    if(self.position[0] == pos[0] or self.isInAttackradius(pos)):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] -= 1
                    if(self.position[0] == pos[0] or self.isInAttackradius(pos)):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] += 1
                    if(self.position[1] == pos[1] or self.isInAttackradius(pos)):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] -= 1
                    if(self.position[1] == pos[1] or self.isInAttackradius(pos)):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] += 1
                    if(self.isInAttackradius(pos)):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] -= 1
                    if(self.isInAttackradius(pos)):
                        break

    def check_for_walls(self, x, y, vmap):
        if(vmap[x][y] == pt.WALL):
            return True
        return False

    def break_wall(self, x, y, V):
        target = V.wall_objs[(x, y)]
        self.attack_target(target)

    def break_building(self, x, y, V):
        target = None
        if(V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if(self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy()

    def kill(self):
        self.alive = False
        archers.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health

# Added stealth archer class below

class Stealth_Archer:
    def __init__(self, position):
        # change add here
        self.init_time = time.time()
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 1
        # change add attack_radius here
        self.attack_radius = 3
        self.position = position
        self.alive = True
        self.target = None
    
    # change add here
    def check_new(self):
        return 1

    def isInAttackradius(self,pos):
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r**2 + c**2 <= self.attack_radius**2):
            return True
        return False

    def move(self, pos, V, type):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(self.isInAttackradius(pos)):
            info = vmap[pos[0]][pos[1]]
            if(info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif type == 1:
            flag = 0
            for i in range(self.speed):
                coords = findPathWithoutWall(V.map, self.position, pos)
                if(coords == None):
                    flag = 1
                    break
                self.position = coords
            if(flag == 0):
                return
        if(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] += 1
                    if(self.isInAttackradius(pos)):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] -= 1
                    if(self.isInAttackradius(pos)):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] += 1
                    if(self.position[0] == pos[0] or self.isInAttackradius(pos)):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] -= 1
                    if(self.position[0] == pos[0] or self.isInAttackradius(pos)):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] += 1
                    if(self.position[1] == pos[1] or self.isInAttackradius(pos)):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[1] -= 1
                    if(self.position[1] == pos[1] or self.isInAttackradius(pos)):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] += 1
                    if(self.isInAttackradius(pos)):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    if(self.check_for_walls(r, c, vmap)):
                        self.break_wall(r, c, V)
                        return
                    self.position[0] -= 1
                    if(self.isInAttackradius(pos)):
                        break

    def check_for_walls(self, x, y, vmap):
        if(vmap[x][y] == pt.WALL):
            return True
        return False

    def break_wall(self, x, y, V):
        target = V.wall_objs[(x, y)]
        self.attack_target(target)

    def break_building(self, x, y, V):
        target = None
        if(V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if(self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy()

    def kill(self):
        self.alive = False
        # change add here
        stealth_archers.remove(self)

    # change add here
    def aoe_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def elapsed_time(self):
        if time.time() - self.init_time > 10:
            return 1
        else:
            return 0

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        # change add here
        curr_time = time.time()
        if curr_time - self.init_time > 10:
            self.health -= hit
            if self.health <= 0:
                self.health = 0
                self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health

# End stealth archer class ################################


class Dragon:
    def __init__(self, position):
        self.speed = 1
        self.health = 100
        self.max_health = 100
        self.attack = 5
        self.position = position
        self.alive = True

    # change add here
    def check_new(self):
        return 0
        

    def move(self, pos, V):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r + c == 1):
            info = vmap[pos[0]][pos[1]]
            if(info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
                    if(self.position[0] == pos[0]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1
                    if(self.position[0] == pos[0]):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if(self.position[1] == pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if(self.position[1] == pos[1]):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1

    def break_building(self, x, y, V):
        target = None
        if(V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if(self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy()

    def kill(self):
        self.alive = False
        dragons.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health


class Balloon:
    def __init__(self, position):
        self.speed = 2
        self.health = 100
        self.max_health = 100
        self.attack = 2
        self.position = position
        self.alive = True

    # change add here
    def check_new(self):
        return 0
        

    def move(self, pos, V):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r + c == 1):
            info = vmap[pos[0]][pos[1]]
            if(info == pt.TOWNHALL):
                self.break_building(pos[0], pos[1], V)
                return
            x = int(info.split(':')[1])
            y = int(info.split(':')[2])
            self.break_building(x, y, V)
            return
        elif(r == 0):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if(abs(pos[1] - self.position[1]) == 1):
                        break
        elif(r > 1):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    r = self.position[0] + 1
                    c = self.position[1]
                    self.position[0] += 1
                    if(self.position[0] == pos[0]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0] - 1
                    c = self.position[1]
                    self.position[0] -= 1
                    if(self.position[0] == pos[0]):
                        return
        elif(c > 1):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] + 1
                    self.position[1] += 1
                    if(self.position[1] == pos[1]):
                        return
            else:
                for i in range(self.speed):
                    r = self.position[0]
                    c = self.position[1] - 1
                    self.position[1] -= 1
                    if(self.position[1] == pos[1]):
                        return
        elif(r+c == 2):
            if(pos[0] > self.position[0]):
                    self.position[0] += 1
            else:
                    self.position[0] -= 1

    def break_building(self, x, y, V):
        target = None
        if(V.map[x][y] == pt.TOWNHALL):
            target = V.town_hall_obj
        else:
            all_buildings = collections.ChainMap(
                V.hut_objs, V.cannon_objs, V.wizard_tower_objs)
            target = all_buildings[(x, y)]
        self.attack_target(target)

    def attack_target(self, target):
        if(self.alive == False):
            return
        target.health -= self.attack
        if target.health <= 0:
            target.health = 0
            target.destroy()

    def kill(self):
        self.alive = False
        balloons.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health

# change add here

class Healer:
    def __init__(self, position):
        self.speed = 2
        self.health = 250
        self.max_health = 250
        self.attack = 2
        self.range = 7
        self.heal_radius = 2
        self.heal_strength = 20
        self.position = position
        self.alive = True

    # change add here
    def check_new(self):
        return 0

    def isInHealrange(self,pos):
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(r**2 + c**2 <= self.range**2):
            return True
        return False

    def move(self, pos, V, flag,King):
        if(self.alive == False):
            return
        vmap = V.map
        r = abs(pos[0] - self.position[0])
        c = abs(pos[1] - self.position[1])
        if(self.isInHealrange(pos)):
            self.heal_troop(pos[0], pos[1], flag, King)
            return
        elif(r > c):
            if(pos[0] > self.position[0]):
                for i in range(self.speed):
                    self.position[0] += 1
            else:
                for i in range(self.speed):
                    self.position[0] -= 1
        elif (r <= c):
            if(pos[1] > self.position[1]):
                for i in range(self.speed):
                    self.position[1] += 1
            else:
                for i in range(self.speed):
                    self.position[1] -= 1

    def heal_troop(self,x,y,flag,King):
        if self.alive == False:
            return
        # if flag == 0:
        kinglist = [King]
        troops = barbarians + archers + dragons + balloons + stealth_archers + kinglist
        for troop in troops:
            if troop.position[0] == x and troop.position[1] == y:
                if(troop.health < troop.max_health - self.heal_strength):
                    troop.health += self.heal_strength
                elif(troop.health < troop.max_health and troop.health > troop.max_health - self.heal_strength):
                    troop.health = troop.max_health
                else:
                    continue
            elif troop.position[0] == x - 1 and troop.position[1] == y:
                if(troop.health < troop.max_health - self.heal_strength):
                    troop.health += self.heal_strength
                elif(troop.health < troop.max_health and troop.health > troop.max_health - self.heal_strength):
                    troop.health = troop.max_health
                else:
                    continue
            elif troop.position[0] == x and troop.position[1] == y - 1:
                if(troop.health < troop.max_health - self.heal_strength):
                    troop.health += self.heal_strength
                elif(troop.health < troop.max_health and troop.health > troop.max_health - self.heal_strength):
                    troop.health = troop.max_health
                else:
                    continue
            elif troop.position[0] == x + 1 and troop.position[1] == y:
                if(troop.health < troop.max_health - self.heal_strength):
                    troop.health += self.heal_strength
                elif(troop.health < troop.max_health and troop.health > troop.max_health - self.heal_strength):
                    troop.health = troop.max_health
                else:
                    continue
            elif troop.position[0] == x and troop.position[1] == y + 1:
                if(troop.health < troop.max_health - self.heal_strength):
                    troop.health += self.heal_strength
                elif(troop.health < troop.max_health and troop.health > troop.max_health - self.heal_strength):
                    troop.health = troop.max_health
                else:
                    continue
            else:
                continue
        # else:
        #     if(King.health < King.max_health - self.heal_strength):
        #         King.health += self.heal_strength
        #     elif(King.health < King.max_health and King.health > King.max_health - self.heal_strength):
        #         King.health = King.max_health
        #     else:
        #         King.health = King.health

    def kill(self):
        self.alive = False
        healers.remove(self)

    def deal_damage(self, hit):
        if(self.alive == False):
            return
        self.health -= hit
        if self.health <= 0:
            self.health = 0
            self.kill()

    def rage_effect(self):
        self.speed = self.speed*2
        self.attack = self.attack*2

    def heal_effect(self):
        self.health = self.health*1.5
        if self.health > self.max_health:
            self.health = self.max_health

# end of healer class


def spawnBarbarian(pos):
    if(pt.troop_limit['barbarian'] <= troops_spawned['barbarian']):
        return

    # convert tuple to list
    pos = list(pos)
    barb = Barbarian(pos)
    troops_spawned['barbarian'] += 1
    barbarians.append(barb)

def spawnArcher(pos):
    if(pt.troop_limit['archer'] <= troops_spawned['archer']):
        return

    # convert tuple to list
    pos = list(pos)
    archer = Archer(pos)
    troops_spawned['archer'] += 1
    archers.append(archer)

## Change add here

def spawnStealthArcher(pos):
    if(pt.troop_limit['stealth_archer'] <= troops_spawned['stealth_archer']):
        return

    # convert tuple to list
    pos = list(pos)
    stealth_archer = Stealth_Archer(pos)
    troops_spawned['stealth_archer'] += 1
    stealth_archers.append(stealth_archer)

def spawnDragon(pos):
    if(pt.troop_limit['dragon'] <= troops_spawned['dragon']):
        return

    # convert tuple to list
    pos = list(pos)
    dr = Dragon(pos)
    troops_spawned['dragon'] += 1
    dragons.append(dr)

def spawnBalloon(pos):
    if(pt.troop_limit['balloon'] <= troops_spawned['balloon']):
        return

    # convert tuple to list
    pos = list(pos)
    bal = Balloon(pos)
    troops_spawned['balloon'] += 1
    balloons.append(bal)

def spawnHealer(pos):
    if(pt.troop_limit['healer'] <= troops_spawned['healer']):
        return

    # convert tuple to list
    pos = list(pos)
    bal = Healer(pos)
    troops_spawned['healer'] += 1
    healers.append(bal)

def move_barbarians(V,type):
    if(type == 1):
        for barb in barbarians:
            if(barb.alive == False):
                continue
            if barb.target != None:    
                if(V.map[barb.target[0]][barb.target[1]] == pt.BLANK):
                    barb.target = None

            if(barb.target == None):
                barb.target = search_for_closest_building(barb.position, V.map, 0)
            if(barb.target == None):
                continue
            barb.move(barb.target, V, type)
    elif(type == 2):
        for barb in barbarians:
            if(barb.alive == False):
                continue
            closest_building = search_for_closest_building(barb.position, V.map, 0)
            if(closest_building == None):
                continue
            barb.move(closest_building, V, type)

def move_archers(V,type):
    if(type == 1):
        for archer in archers:
            if(archer.alive == False):
                continue
            if archer.target != None:
                if(V.map[archer.target[0]][archer.target[1]] == pt.BLANK):
                    archer.target = None
            if(archer.target == None):
                archer.target = search_for_closest_building(archer.position, V.map, 0)
            if(archer.target == None):
                continue
            archer.move(archer.target, V,type)
    elif(type == 2):
        for archer in archers:
            if(archer.alive == False):
                continue
            closest_building = search_for_closest_building(archer.position, V.map, 0)
            if(closest_building == None):
                continue
            archer.move(closest_building, V, type)

# change add here

def move_stealth_archers(V,type):
    if(type == 1):
        for archer in stealth_archers:
            if(archer.alive == False):
                continue
            if archer.target != None:
                if(V.map[archer.target[0]][archer.target[1]] == pt.BLANK):
                    archer.target = None
            if(archer.target == None):
                archer.target = search_for_closest_building(archer.position, V.map, 0)
            if(archer.target == None):
                continue
            archer.move(archer.target, V,type)
    elif(type == 2):
        for archer in stealth_archers:
            if(archer.alive == False):
                continue
            closest_building = search_for_closest_building(archer.position, V.map, 0)
            if(closest_building == None):
                continue
            archer.move(closest_building, V, type)

def move_dragons(V):
    for dr in dragons:
        if(dr.alive == False):
            continue
        closest_building = search_for_closest_building(dr.position, V.map, 0)
        if(closest_building == None):
            continue
        dr.move(closest_building, V)

def move_balloons(V):
    for bal in balloons:
        if(bal.alive == False):
            continue
        closest_building = search_for_closest_building(bal.position, V.map, 1)
        if(closest_building == None):
            continue
        bal.move(closest_building, V)

def move_healers(V, troops, King):
    spec_coords = King.position
    for bal in healers:
        if(bal.alive == False):
            continue
        closest_troop = search_for_closest_troop(bal.position, V.map ,troops, spec_coords)
        flag2 = 0
        # print(closest_troop)
        if(closest_troop == None):
            continue
        if closest_troop[0] == spec_coords[0] and closest_troop[1] == spec_coords[1]:
            flag2 = 1
        # print(flag2)
        bal.move(closest_troop, V, flag2, King)

def search_for_closest_building(pos, vmap, prioritized):
    closest_building = None
    closest_dist = 10000
    flag = 0
    for i in range(len(vmap)):
        for j in range(len(vmap[i])):
            item = vmap[i][j].split(':')[0]
            if(prioritized == 0):
                if (item == pt.HUT or item == pt.CANNON or item == pt.TOWNHALL or item == pt.WIZARD_TOWER):
                    dist = abs(i - pos[0]) + abs(j - pos[1])
                    if(dist < closest_dist):
                        flag = 1
                        closest_dist = dist
                        closest_building = (i, j)
            else:
                if (item == pt.CANNON or item == pt.WIZARD_TOWER):
                    dist = abs(i - pos[0]) + abs(j - pos[1])
                    if(dist < closest_dist):
                        flag = 1
                        closest_dist = dist
                        closest_building = (i, j)
    if(flag == 0 and prioritized == 0):
        return None
    elif(flag == 0 and prioritized == 1):
        return search_for_closest_building(pos, vmap, 0)
    else:
        return closest_building

# change add here search for nearest sprite

def search_for_closest_troop(pos, vmap, troops, spec_coords):
    closest_troop = None
    closest_dist = 10000
    flag = 0
    flag_ = 0

    for troop in troops:
        if troop.health == troop.max_health:
            continue
        xcoord = troop.position[0]
        ycoord = troop.position[1]
        dist = abs(xcoord-pos[0]) + abs(ycoord-pos[1])
        if dist < closest_dist:
            flag = 1
            closest_dist = dist
            closest_troop = (xcoord,ycoord)
    if abs(spec_coords[0]-pos[0]) + abs(spec_coords[1]-pos[1]) < closest_dist and flag == 1:
        closest_dist = abs(spec_coords[0]-pos[0]) + abs(spec_coords[1]-pos[1])
        closest_troop = (spec_coords[0],spec_coords[1])
        flag_ = 1
    if(flag == 0):
        return None
    else:
        return closest_troop

def findPathWithoutWall(grid,start,end):
    graph = []
    for row in grid:
        row2 = []
        for col in row:
            if(col == pt.BLANK):
                row2.append(0) # 0 means walkable
            else:
                row2.append(1) # 1 means not walkable
        graph.append(row2)
    graph[start[0]] [start[1]] = 2 # mark start as 2
    graph[end[0]] [end[1]] = 3 # mark end as 3

    coords = moveWithoutBreakingWalls(graph,start)
    if coords == None:
        return None
    else:
        return list(coords)
   