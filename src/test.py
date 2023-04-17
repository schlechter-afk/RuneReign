import unittest

from king import King
import village
import random
import points as pt

level = 1
V1 = village.createVillage(level)
spawn_locations = []

vmap1 = V1.map
for i in range(len(vmap1)):
    for j in range(len(vmap1[i])):
        if vmap1[i][j] != pt.BLANK:
            spawn_locations.append((i,j))   

# [0,0] to [17,35] (len-1,len-1) both inclusive are valid points
        
class TestKingMove(unittest.TestCase):
    def test_pt_heropos(self): # test if pt.HEROPOS is set correctly to position or not.
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

    def test_random_inp(self): # test if king moves when given random direction or not ?
        testKing = King([2,2])
        testKing.move('gibberish', V1)
        self.assertEqual(testKing.position, [2,2], "King moved when given invalid input")

    def test_facing_direction(self): # test if king changes facing direction correctly when given valid/invalid input.
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

    def test_alive_move(self): # test if king moves in either of 4 directions when alive.
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
        testKing.move('up', V1)
        self.assertEqual(testKing.position, [cpyx, cpyy], "King moved up when dead")
        xcoord = cpyx
        ycoord = cpyy
        # for down alive
        testKing2 = King([xcoord, ycoord])
        testKing2.alive = False
        testKing2.move('down', V1)
        self.assertEqual(testKing2.position, [cpyx, cpyy], "King moved down when dead")
        xcoord = cpyx
        ycoord = cpyy
        # for left alive
        testKing3 = King([xcoord, ycoord])
        testKing3.alive = False
        testKing3.move('left', V1)
        self.assertEqual(testKing3.position, [cpyx, cpyy], "King moved left when dead")
        xcoord = cpyx
        ycoord = cpyy
        # for right alive
        testKing4 = King([xcoord, ycoord])
        testKing4.alive = False
        testKing.move('right', V1)
        self.assertEqual(testKing4.position, [cpyx, cpyy], "King moved right when dead")


    def test_normal_up(self): # allowing movement from [1 to len-1 , 0 to len-1]
        for times in range(0,5000):
            xcoord = random.randint(1, len(vmap1)-1)
            ycoord = random.randint(0, len(vmap1[0])-1)
            while (xcoord, ycoord) in spawn_locations or (xcoord - 1, ycoord) in spawn_locations:
                xcoord = random.randint(1, len(vmap1)-1)
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('up',V1)
            self.assertEqual(testKing.position, [xcoord - 1 , ycoord] , "incorrect up movement")

    def test_normal_down(self): # allowing movement from [0 to len-2 , 0 to len-1]
        for times in range(0,5000):
            xcoord = random.randint(0, len(vmap1)-2)
            ycoord = random.randint(0, len(vmap1[0])-1)
            while (xcoord, ycoord) in spawn_locations or (xcoord + 1, ycoord) in spawn_locations:
                xcoord = random.randint(0, len(vmap1)-2)
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('down',V1)
            self.assertEqual(testKing.position, [xcoord + 1 , ycoord] , "incorrect down movement")

    def test_normal_left(self): # allowing movement from [0 to len-1 , 1 to len-1]
        for times in range(0,5000):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = random.randint(1, len(vmap1[0])-1)
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord - 1) in spawn_locations:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = random.randint(1, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('left',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord - 1] , "incorrect left movement")

    def test_normal_right(self): # allowing movement from [0 to len - 1 , 0 to len - 2]
        for times in range(0,5000):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = random.randint(0, len(vmap1[0])-2)
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord + 1) in spawn_locations:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = random.randint(0, len(vmap1[0])-2)
            testKing = King([xcoord, ycoord])
            testKing.move('right',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord + 1] , "incorrect right movement")

    def test_edge_up(self): # allowing movement from [0 , 0 to len-1]
        for times in range(0,5000):
            xcoord = 0
            ycoord = random.randint(0, len(vmap1[0])-1)
            while (xcoord, ycoord) in spawn_locations or (xcoord - 1, ycoord) in spawn_locations:
                xcoord = 0
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('up',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord] , "incorrect up movement on edge")

    def test_edge_down(self): # allowing movement from [len-1 , 0 to len-1 ]
        for times in range(0,5000):
            xcoord = len(vmap1) - 1
            ycoord = random.randint(0, len(vmap1[0])-1)
            while (xcoord, ycoord) in spawn_locations or (xcoord - 1, ycoord) in spawn_locations:
                xcoord = len(vmap1) - 1
                ycoord = random.randint(0, len(vmap1[0])-1)
            testKing = King([xcoord, ycoord])
            testKing.move('down',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord] , "incorrect down movement on edge")

    def test_edge_left(self): # allowing movement from [0 to len-1 , 0]
        for times in range(0,5000):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = 0
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord - 1) in spawn_locations:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = 0
            testKing = King([xcoord, ycoord])
            testKing.move('left',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord] , "incorrect left movement on edge")

    def test_edge_right(self): # allowing movement from [0 to len - 1 , len - 1]
        for times in range(0,5000):
            xcoord = random.randint(0, len(vmap1)-1)
            ycoord = len(vmap1[0]) - 1
            while (xcoord, ycoord) in spawn_locations or (xcoord, ycoord + 1) in spawn_locations:
                xcoord = random.randint(0, len(vmap1)-1)
                ycoord = len(vmap1[0]) - 1
            testKing = King([xcoord, ycoord])
            testKing.move('right',V1)
            self.assertEqual(testKing.position, [xcoord, ycoord] , "incorrect right movement on edge")

unittest.main()