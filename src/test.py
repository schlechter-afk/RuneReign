import unittest

from king import King
import village
import random
import points as pt

# import sys
# original_stdout = sys.stdout # Save a reference to the original standard output

# with open('output.txt', 'w') as f:
#     sys.stdout = f # Change the standard output to the file we created.
#     # sys.stdout = original_stdout # Reset the standard output to its original value

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
# print(spec_locs)
# [0,0] to [17,35] (len-1,len-1) both inclusive are valid points
        
class TestKingMove(unittest.TestCase):

    def test_aggregate(self):
        testKing = King([2,2])
        temp = pt.HERO_POS
        testKing.move('gibberish', V1)
        self.assertEqual(pt.HERO_POS, testKing.position, "pt.HERO_POS changed when given invalid input")
        testKing.move('up', V1)
        self.assertEqual(pt.HERO_POS, [1,2], "pt.HERO_POS not set correctly")
        testKing.move('down', V1)
        self.assertEqual(pt.HERO_POS, [2,2], "pt.HERO_POS not set correctly")
        testKing.move('left', V1)
        self.assertEqual(pt.HERO_POS, [2,1], "pt.HERO_POS not set correctly")
        testKing.move('right', V1)
        self.assertEqual(pt.HERO_POS, [2,2], "pt.HERO_POS not set correctly")
        testKing = King([2,2])
        testKing.move('gibberish', V1)
        self.assertEqual(testKing.position, [2,2], "King moved when given invalid input")
        testKing = King([2,2])
        orig = testKing.facing
        testKing.move('gibberish', V1)
        self.assertEqual(testKing.facing, orig, "Facing direction changed when given invalid input")
        testKing.move('left', V1)
        self.assertEqual(testKing.facing, 'left', "Left facing direction not set correctly")
        testKing.move('right', V1)
        self.assertEqual(testKing.facing, 'right', "Right facing direction not set correctly")
        testKing.move('up', V1)
        self.assertEqual(testKing.facing, 'up', "Up facing direction not set correctly")
        testKing.move('down', V1)
        self.assertEqual(testKing.facing, 'down', "Down facing direction not set correctly")

        xcoord = random.randint(1, len(vmap1)-2)
        ycoord = random.randint(1, len(vmap1[0])-2)
        while (xcoord, ycoord) in spawn_locations or (xcoord - 1, ycoord) in spawn_locations or (xcoord, ycoord - 1) in spawn_locations or (xcoord + 1, ycoord) in spawn_locations or (xcoord, ycoord + 1) in spawn_locations:
            xcoord = random.randint(1, len(vmap1)-2)
            ycoord = random.randint(1, len(vmap1[0])-2)
        cpyx = xcoord
        cpyy = ycoord
        # for up alive
        testKing = King([xcoord, ycoord])
        testKing.alive = False
        testKing.health = 0
        testKing.move('up', V1)
        self.assertEqual(testKing.position, [cpyx, cpyy], "King moved up when dead")
        xcoord = cpyx
        ycoord = cpyy
        # for down alive
        testKing2 = King([xcoord, ycoord])
        testKing2.alive = False
        testKing2.health = 0
        testKing2.move('down', V1)
        self.assertEqual(testKing2.position, [cpyx, cpyy], "King moved down when dead")
        xcoord = cpyx
        ycoord = cpyy
        # for left alive
        testKing3 = King([xcoord, ycoord])
        testKing3.alive = False
        testKing3.health = 0
        testKing3.move('left', V1)
        self.assertEqual(testKing3.position, [cpyx, cpyy], "King moved left when dead")
        xcoord = cpyx
        ycoord = cpyy
        # for right alive
        testKing4 = King([xcoord, ycoord])
        testKing4.alive = False
        testKing4.health = 0
        testKing.move('right', V1)
        self.assertEqual(testKing4.position, [cpyx, cpyy], "King moved right when dead")

        for times in range(0,50):
            xcoord = random.randint(1, len(vmap1)-1)
            ycoord = random.randint(0, len(vmap1[0])-1)
            while (xcoord, ycoord) in spawn_locations or (xcoord - 1, ycoord) in spawn_locations:
                xcoord = random.randint(1, len(vmap1)-1)
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            up_health = testKing.health
            up_max_health = testKing.max_health
            up_attack = testKing.attack
            up_aoe = testKing.AoE
            up_attack_radius = testKing.attack_radius
            up_alive = testKing.alive
            up_speed = testKing.speed
            testKing.move('up',V1)
            self.assertEqual(testKing.position, [xcoord - 1 , ycoord] , "incorrect up movement")
            self.assertEqual(testKing.health, up_health, "incorrect up health")
            self.assertEqual(testKing.max_health, up_max_health, "incorrect up max health")
            self.assertEqual(testKing.attack, up_attack, "incorrect up attack")
            self.assertEqual(testKing.AoE, up_aoe, "incorrect up AoE")
            self.assertEqual(testKing.attack_radius, up_attack_radius, "incorrect up attack radius")
            self.assertEqual(testKing.alive, up_alive, "incorrect up alive")
            self.assertEqual(testKing.speed, up_speed, "incorrect up speed")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-2)
            ycoord = random.randint(0, len(vmap1[0])-1)
            while (xcoord, ycoord) in spawn_locations or (xcoord + 1, ycoord) in spawn_locations:
                xcoord = random.randint(0, len(vmap1)-2)
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            up_health = testKing.health
            up_max_health = testKing.max_health
            up_attack = testKing.attack
            up_aoe = testKing.AoE
            up_attack_radius = testKing.attack_radius
            up_alive = testKing.alive
            up_speed = testKing.speed
            testKing.move('down',V1)
            self.assertEqual(testKing.position, [xcoord + 1 , ycoord] , "incorrect down movement")
            self.assertEqual(testKing.health, up_health, "incorrect up health")
            self.assertEqual(testKing.max_health, up_max_health, "incorrect up max health")
            self.assertEqual(testKing.attack, up_attack, "incorrect up attack")
            self.assertEqual(testKing.AoE, up_aoe, "incorrect up AoE")
            self.assertEqual(testKing.attack_radius, up_attack_radius, "incorrect up attack radius")
            self.assertEqual(testKing.alive, up_alive, "incorrect up alive")
            self.assertEqual(testKing.speed, up_speed, "incorrect up speed")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = random.randint(1, len(vmap1[0])-1)
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord - 1) in spawn_locations:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = random.randint(1, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            up_health = testKing.health
            up_max_health = testKing.max_health
            up_attack = testKing.attack
            up_aoe = testKing.AoE
            up_attack_radius = testKing.attack_radius
            up_alive = testKing.alive
            up_speed = testKing.speed
            testKing.move('left',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord - 1] , "incorrect left movement")
            self.assertEqual(testKing.health, up_health, "incorrect up health")
            self.assertEqual(testKing.max_health, up_max_health, "incorrect up max health")
            self.assertEqual(testKing.attack, up_attack, "incorrect up attack")
            self.assertEqual(testKing.AoE, up_aoe, "incorrect up AoE")
            self.assertEqual(testKing.attack_radius, up_attack_radius, "incorrect up attack radius")
            self.assertEqual(testKing.alive, up_alive, "incorrect up alive")
            self.assertEqual(testKing.speed, up_speed, "incorrect up speed")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = random.randint(0, len(vmap1[0])-2)
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord + 1) in spawn_locations:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = random.randint(0, len(vmap1[0])-2)
            testKing = King([xcoord, ycoord])
            up_health = testKing.health
            up_max_health = testKing.max_health
            up_attack = testKing.attack
            up_aoe = testKing.AoE
            up_attack_radius = testKing.attack_radius
            up_alive = testKing.alive
            up_speed = testKing.speed
            testKing.move('right',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord + 1] , "incorrect right movement")
            self.assertEqual(testKing.health, up_health, "incorrect up health")
            self.assertEqual(testKing.max_health, up_max_health, "incorrect up max health")
            self.assertEqual(testKing.attack, up_attack, "incorrect up attack")
            self.assertEqual(testKing.AoE, up_aoe, "incorrect up AoE")
            self.assertEqual(testKing.attack_radius, up_attack_radius, "incorrect up attack radius")
            self.assertEqual(testKing.alive, up_alive, "incorrect up alive")
            self.assertEqual(testKing.speed, up_speed, "incorrect up speed")
            

        for times in range(0,50):
            xcoord = 0
            ycoord = random.randint(0, len(vmap1[0])-1)
            while (xcoord, ycoord) in spawn_locations or (xcoord - 1, ycoord) in spawn_locations:
                xcoord = 0
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('up',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord] , "incorrect up movement on edge")

        for times in range(0,50):
            xcoord = len(vmap1) - 1
            ycoord = random.randint(0, len(vmap1[0])-1)
            while (xcoord, ycoord) in spawn_locations or (xcoord + 1, ycoord) in spawn_locations:
                xcoord = len(vmap1) - 1
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('down',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord] , "incorrect down movement on edge")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = 0
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord - 1) in spawn_locations:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = 0
            testKing = King([xcoord, ycoord])
            testKing.move('left',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord] , "incorrect left movement on edge")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = len(vmap1[0]) - 1
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord + 1) in spawn_locations:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = len(vmap1[0]) - 1
            testKing = King([xcoord, ycoord])
            testKing.move('right',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord] , "incorrect right movement on edge")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = len(vmap1[0]) - 1
            while (xcoord, ycoord) in spawn_locations or (xcoord - 1, ycoord) not in spawn_locations or (xcoord - 1, ycoord) in spec_locs:
                xcoord = random.randint(1, len(vmap1)-1)
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('up',V1)
            self.assertEqual(testKing.position, [xcoord , ycoord] , "incorrect up movement in case of buildings")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = len(vmap1[0]) - 1
            while (xcoord, ycoord) in spawn_locations or (xcoord + 1, ycoord) not in spawn_locations or (xcoord + 1, ycoord) in spec_locs:
                xcoord = random.randint(0, len(vmap1)-2)
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('down',V1)
            self.assertEqual(testKing.position, [xcoord , ycoord] , "incorrect down movement in case of buildings")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = len(vmap1[0]) - 1
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord - 1) not in spawn_locations or (xcoord ,ycoord - 1) in spec_locs:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = random.randint(1, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('left',V1)
            self.assertEqual(testKing.position, [xcoord , ycoord] , "incorrect left movement in case of buildings")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = len(vmap1[0]) - 1
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord + 1) not in spawn_locations or (xcoord, ycoord + 1) in spec_locs:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = random.randint(0, len(vmap1[0])-2)
            testKing = King([xcoord, ycoord])
            testKing.move('right',V1)
            self.assertEqual(testKing.position, [xcoord , ycoord] , "incorrect right movement in case of buildings")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = len(vmap1[0]) - 1
            while (xcoord, ycoord) in spawn_locations or (xcoord - 1, ycoord) not in spec_locs:
                xcoord = random.randint(1, len(vmap1)-1)
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('up',V1)
            self.assertEqual(testKing.position, [xcoord - 1 , ycoord] , "incorrect up movement in case of spec_coords")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = len(vmap1[0]) - 1
            while (xcoord, ycoord) in spawn_locations or (xcoord + 1, ycoord) not in spec_locs:
                xcoord = random.randint(0, len(vmap1)-2)
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('down',V1)
            self.assertEqual(testKing.position, [xcoord + 1, ycoord] , "incorrect down movement in case of spec_coords")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = len(vmap1[0]) - 1
            while (xcoord, ycoord) in spawn_locations or (xcoord ,ycoord - 1) not in spec_locs:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = random.randint(1, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('left',V1)
            self.assertEqual(testKing.position, [xcoord , ycoord - 1] , "incorrect left movement in case of spec_coords")

        for times in range(0,50):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = len(vmap1[0]) - 1
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord + 1) not in spec_locs:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = random.randint(0, len(vmap1[0])-2)
            testKing = King([xcoord, ycoord])
            testKing.move('right',V1)
            self.assertEqual(testKing.position, [xcoord , ycoord + 1] , "incorrect right movement in case of spec_coords")

        for speed in range(2,18):
            testKing2 = King([speed,2])
            testKing2.speed = speed
            testKing2.move('up',V1)
            self.assertEqual(testKing2.position, [0,2] , "incorrect up movement in case of speed > 1")

        for speed in range(2,17):
            testKing2 = King([1,3])
            testKing2.speed = speed
            testKing2.move('down',V1)
            self.assertEqual(testKing2.position, [speed+1,3] , "incorrect down movement in case of speed > 1")

        for speed in range(2,18):
            testKing2 = King([1,speed])
            testKing2.speed = speed
            testKing2.move('left',V1)
            self.assertEqual(testKing2.position, [1,0] , "incorrect left movement in case of speed > 1")

        for speed in range(2,17):
            testKing2 = King([1,1])
            testKing2.speed = speed
            testKing2.move('right',V1)
            self.assertEqual(testKing2.position, [1,speed+1] , "incorrect right movement in case of speed > 1")

if __name__ == '__main__':
    # create a test suite with the Test_Aggregate class
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKingMove)
    
    # run the test suite and capture the result
    result = unittest.TextTestRunner().run(suite)
    
    # check if all tests passed and create output file accordingly
    if result.wasSuccessful():
        with open('output.txt', 'w') as f:
            f.write('True')
    else:
        with open('output.txt', 'w') as f:
            f.write('False')
