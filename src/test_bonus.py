import unittest

from king import King
import village
import random
import points as pt

# import sys
# original_stdout = sys.stdout # Save a reference to the original standard output

# with open('output_bonus.txt', 'w') as f:
    # sys.stdout = f # Change the standard output to the file we created.

level = 1
V1 = village.createVillage(level)
spawn_locations = []
spec_locs = []

vmap1 = V1.map
for i in range(len(vmap1)):
    for j in range(len(vmap1[i])):
        if vmap1[i][j] != pt.BLANK:
            spawn_locations.append((i,j))   
        if vmap1[i][j] == pt.SPAWN:
            spec_locs.append((i,j)) 

# print(spawn_locations)  
        
class TestKingAttack(unittest.TestCase):

    def test_aggregate(self):

        # testing if target is inflicted damage when king is dead.

        target = V1.get_target(12,13)
        temp = target.health
        position = target.position
        dimensions = target.dimensions
        destroyed = target.destroyed
        max_health = target.max_health
        testKingd = King([2,2])
        testKingd.alive = False
        testKingd.attack_target(target,testKingd.attack)
        self.assertEqual(target.health, temp)
        self.assertEqual(target.position, position)
        self.assertEqual(target.dimensions, dimensions)
        self.assertEqual(target.destroyed, destroyed)
        self.assertEqual(target.max_health, max_health)

        # testing against a cannon now

        testKing = King([2,2])
        target = V1.get_target(10,22) 
        temp = target.health
        cannon_pos = target.position
        cannon_maxhealth = target.max_health
        cannon_attack = target.attack
        cannon_attack_radius = target.attack_radius
        cannon_dimensions = target.dimensions
        cannon_isShooting = target.isShooting
        cannon_type = target.type
        cannon_destroyed = target.destroyed
        testKing.attack_target(target, testKing.attack)
        self.assertEqual(target.health, temp - testKing.attack)
        self.assertEqual(target.position, cannon_pos)
        self.assertEqual(target.max_health, cannon_maxhealth)
        self.assertEqual(target.attack, cannon_attack)
        self.assertEqual(target.attack_radius, cannon_attack_radius)
        self.assertEqual(target.dimensions, cannon_dimensions)
        self.assertEqual(target.isShooting, cannon_isShooting)
        self.assertEqual(target.type, cannon_type) 
        self.assertEqual(target.destroyed, cannon_destroyed)

        # testing against a wall now

        testKing2 = King([2,2])
        target2 = V1.get_target(3,12)
        wall_maxhealth = target2.max_health
        wall_position = target2.position
        wall_dimensions = target2.dimensions
        wall_type = target2.type
        testKing2.attack_target(target2, testKing2.attack)
        self.assertEqual(target2.health, 0)
        self.assertEqual(target2.destroyed, True)
        self.assertEqual(target2.max_health, wall_maxhealth)
        self.assertEqual(target2.position, wall_position)
        self.assertEqual(target2.dimensions, wall_dimensions)
        self.assertEqual(target2.type, wall_type)

        # testing against a hut now

        testKing3 = King([2,2])
        target3 = V1.get_target(10,4)
        hut_maxhealth = target3.max_health
        hut_position = target3.position
        hut_dimensions = target3.dimensions
        hut_type = target3.type
        hut_health = target3.health
        hut_destroyed = target3.destroyed
        testKing3.attack_target(target3, testKing3.attack)
        self.assertEqual(target3.health, hut_health - testKing3.attack)
        self.assertEqual(target3.max_health, hut_maxhealth)
        self.assertEqual(target3.position, hut_position)
        self.assertEqual(target3.dimensions, hut_dimensions)
        self.assertEqual(target3.type, hut_type)
        self.assertEqual(target3.destroyed, hut_destroyed)

        # testing against a wizard_tower now

        testKing4 = King([2,2])
        target4 = V1.get_target(7,27)
        wizard_tower_maxhealth = target4.max_health
        wizard_tower_position = target4.position
        wizard_tower_dimensions = target4.dimensions
        wizard_tower_type = target4.type
        wizard_tower_health = target4.health
        wizard_tower_attack = target4.attack
        wizard_tower_attack_radius = target4.attack_radius
        wizard_tower_isShooting = target4.isShooting
        wizard_tower_destroyed = target4.destroyed
        testKing4.attack_target(target4, testKing4.attack)
        self.assertEqual(target4.health, wizard_tower_health - testKing4.attack)
        self.assertEqual(target4.max_health, wizard_tower_maxhealth)
        self.assertEqual(target4.position, wizard_tower_position)
        self.assertEqual(target4.dimensions, wizard_tower_dimensions)
        self.assertEqual(target4.type, wizard_tower_type)
        self.assertEqual(target4.attack, wizard_tower_attack)
        self.assertEqual(target4.attack_radius, wizard_tower_attack_radius)
        self.assertEqual(target4.isShooting, wizard_tower_isShooting)
        self.assertEqual(target4.destroyed, wizard_tower_destroyed)

        # testing against a townhall now

        testKing5 = King([2,2])
        target5 = V1.get_target(6,16)
        townhall_maxhealth = target5.max_health
        townhall_position = target5.position
        townhall_dimensions = target5.dimensions
        townhall_type = target5.type
        townhall_health = target5.health
        townhall_destroyed = target5.destroyed
        testKing5.attack_target(target5, testKing5.attack)
        self.assertEqual(target5.health, townhall_health - testKing5.attack)
        self.assertEqual(target5.max_health, townhall_maxhealth)
        self.assertEqual(target5.position, townhall_position)
        self.assertEqual(target5.dimensions, townhall_dimensions)
        self.assertEqual(target5.type, townhall_type)
        self.assertEqual(target5.destroyed, townhall_destroyed)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKingAttack)
    result = unittest.TextTestRunner().run(suite)
    if result.wasSuccessful():
        with open('output_bonus.txt', 'w') as f:
            f.write('True')
    else:
        with open('output_bonus.txt', 'w') as f:
            f.write('False')
