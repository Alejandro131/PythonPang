import unittest

from pang.ball import Ball
from pang.vec2d import Vec2D
from pang.collision import *
from pang.obstacle import Obstacle


class BallToBoxCollisionTest(unittest.TestCase):

    def setUp(self):
        self.balls = []
        self.results = []
        self.box = Obstacle(Vec2D(200, 200), Vec2D(200, 200))
        self.balls.append(Ball(150, Vec2D(200, 100), Vec2D(50, 50)))
        self.results.append((Vec2D(200, 0), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(200, 100), Vec2D(-50, 50)))
        self.results.append((Vec2D(200, 0), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(400, 100), Vec2D(50, 50)))
        self.results.append((Vec2D(400, 0), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(400, 100), Vec2D(-50, 50)))
        self.results.append((Vec2D(400, 0), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(450, 200 - 50*(3**.5)),
                               Vec2D(50, 50)))
        self.results.append((Vec2D(450, 3.76), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(450, 200 - 50*(3**.5)),
                               Vec2D(-50, 50)))
        self.results.append((Vec2D(450, 3.76), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(400 + 50*(3**.5), 150),
                               Vec2D(-50, 50)))
        self.results.append((Vec2D(596.24, 150), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(400 + 50*(3**.5), 150),
                               Vec2D(-50, -50)))
        self.results.append((Vec2D(596.24, 150), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(500, 200), Vec2D(-50, 50)))
        self.results.append((Vec2D(600, 200), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(500, 200), Vec2D(-50, -50)))
        self.results.append((Vec2D(600, 200), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(500, 400), Vec2D(-50, 50)))
        self.results.append((Vec2D(600, 400), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(500, 400), Vec2D(-50, -50)))
        self.results.append((Vec2D(600, 400), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(400 + 50*(3**.5), 450),
                               Vec2D(-50, 50)))
        self.results.append((Vec2D(596.24, 450), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(400 + 50*(3**.5), 450),
                               Vec2D(-50, -50)))
        self.results.append((Vec2D(596.24, 450), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(450, 400 + 50*(3**.5)),
                               Vec2D(50, -50)))
        self.results.append((Vec2D(450, 596.24), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(450, 400 + 50*(3**.5)),
                               Vec2D(-50, -50)))
        self.results.append((Vec2D(450, 596.24), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(400, 500), Vec2D(50, -50)))
        self.results.append((Vec2D(400, 600), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(400, 500), Vec2D(-50, -50)))
        self.results.append((Vec2D(400, 600), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(200, 500), Vec2D(50, -50)))
        self.results.append((Vec2D(200, 600), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(200, 500), Vec2D(-50, -50)))
        self.results.append((Vec2D(200, 600), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(150, 400 + 50*(3**.5)),
                               Vec2D(50, -50)))
        self.results.append((Vec2D(150, 596.24), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(150, 400 + 50*(3**.5)),
                               Vec2D(-50, -50)))
        self.results.append((Vec2D(150, 596.24), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(200 - 50*(3**.5), 450),
                               Vec2D(50, -50)))
        self.results.append((Vec2D(3.76, 450), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(200 - 50*(3**.5), 450),
                               Vec2D(50, 50)))
        self.results.append((Vec2D(3.76, 450), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(100, 400), Vec2D(50, -50)))
        self.results.append((Vec2D(0, 400), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(100, 400), Vec2D(50, 50)))
        self.results.append((Vec2D(0, 400), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(100, 200), Vec2D(50, -50)))
        self.results.append((Vec2D(0, 200), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(100, 200), Vec2D(50, 50)))
        self.results.append((Vec2D(0, 200), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(200 - 50*(3**.5), 150),
                               Vec2D(50, -50)))
        self.results.append((Vec2D(3.76, 150), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(200 - 50*(3**.5), 150),
                               Vec2D(50, 50)))
        self.results.append((Vec2D(3.76, 150), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(150, 200 - 50*(3**.5)),
                               Vec2D(50, 50)))
        self.results.append((Vec2D(150, 3.76), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(150, 200 - 50*(3**.5)),
                               Vec2D(-50, 50)))
        self.results.append((Vec2D(150, 3.76), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(300, 100), Vec2D(50, 50)))
        self.results.append((Vec2D(300, 0), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(300, 100), Vec2D(-50, 50)))
        self.results.append((Vec2D(300, 0), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(450, 100), Vec2D(50, 50)))
        self.results.append((Vec2D(450, 17.16), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(450, 100), Vec2D(-50, 50)))
        self.results.append((Vec2D(450, 17.16), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(450, 150), Vec2D(50, 50)))
        self.results.append((Vec2D(450, -32.84), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(450, 150), Vec2D(-50, 50)))
        self.results.append((Vec2D(337.87, 37.87), Vec2D(-1, -1)))
        self.balls.append(Ball(150, Vec2D(450, 150), Vec2D(-50, -50)))
        self.results.append((Vec2D(632.84, 150), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(500, 150), Vec2D(-50, 50)))
        self.results.append((Vec2D(582.84, 150), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(500, 150), Vec2D(-50, -50)))
        self.results.append((Vec2D(582.84, 150), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(500, 300), Vec2D(-50, 50)))
        self.results.append((Vec2D(600, 300), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(500, 300), Vec2D(-50, -50)))
        self.results.append((Vec2D(600, 300), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(500, 450), Vec2D(-50, 50)))
        self.results.append((Vec2D(582.84, 450), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(500, 450), Vec2D(-50, -50)))
        self.results.append((Vec2D(582.84, 450), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(450, 450), Vec2D(-50, 50)))
        self.results.append((Vec2D(632.84, 450), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(450, 450), Vec2D(-50, -50)))
        self.results.append((Vec2D(562.13, 562.13), Vec2D(-1, -1)))
        self.balls.append(Ball(150, Vec2D(450, 450), Vec2D(50, -50)))
        self.results.append((Vec2D(450, 632.84), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(450, 500), Vec2D(-50, -50)))
        self.results.append((Vec2D(450, 582.84), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(450, 500), Vec2D(50, -50)))
        self.results.append((Vec2D(450, 582.84), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(300, 500), Vec2D(-50, -50)))
        self.results.append((Vec2D(300, 600), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(300, 500), Vec2D(50, -50)))
        self.results.append((Vec2D(300, 600), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(150, 500), Vec2D(-50, -50)))
        self.results.append((Vec2D(150, 582.84), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(150, 500), Vec2D(50, -50)))
        self.results.append((Vec2D(150, 582.84), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(150, 450), Vec2D(-50, -50)))
        self.results.append((Vec2D(150, 632.84), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(150, 450), Vec2D(50, -50)))
        self.results.append((Vec2D(262.13, 562.13), Vec2D(-1, -1)))
        self.balls.append(Ball(150, Vec2D(150, 450), Vec2D(50, 50)))
        self.results.append((Vec2D(-32.84, 450), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(100, 450), Vec2D(50, -50)))
        self.results.append((Vec2D(17.16, 450), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(100, 450), Vec2D(50, 50)))
        self.results.append((Vec2D(17.16, 450), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(100, 300), Vec2D(50, -50)))
        self.results.append((Vec2D(0, 300), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(100, 300), Vec2D(50, 50)))
        self.results.append((Vec2D(0, 300), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(100, 150), Vec2D(50, -50)))
        self.results.append((Vec2D(17.16, 150), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(100, 150), Vec2D(50, 50)))
        self.results.append((Vec2D(17.16, 150), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(150, 150), Vec2D(50, -50)))
        self.results.append((Vec2D(-32.84, 150), Vec2D(-1, 0)))
        self.balls.append(Ball(150, Vec2D(150, 150), Vec2D(50, 50)))
        self.results.append((Vec2D(37.87, 37.87), Vec2D(-1, -1)))
        self.balls.append(Ball(150, Vec2D(150, 150), Vec2D(-50, 50)))
        self.results.append((Vec2D(150, -32.84), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(150, 100), Vec2D(50, 50)))
        self.results.append((Vec2D(150, 17.16), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(150, 100), Vec2D(-50, 50)))
        self.results.append((Vec2D(150, 17.16), Vec2D(0, -1)))
        self.balls.append(Ball(150, Vec2D(0, 0), Vec2D(50, 0)))
        self.results.append((Vec2D(0, 0), None))

    def tearDown(self):
        del self.box
        del self.balls
        del self.results

    def test_edge_collision(self):
        for test_index in [32, 33, 41, 42, 50, 51, 59, 60]:
            result = ball_to_box(self.balls[test_index], self.box, True)
            self.assertEqual(self.results[test_index][1], result)
            self.assertEqual(self.results[test_index][0],
                             self.balls[test_index].position)
            self.assertFalse(ball_to_box(self.balls[test_index],
                                         self.box, True))

    def test_edge_limit_collision(self):
        for test_index in [0, 1, 2, 3, 8, 9, 10, 11, 16, 17, 18, 19, 24, 25,
                           26, 27]:
            result = ball_to_box(self.balls[test_index], self.box, True)
            self.assertEqual(self.results[test_index][1], result)
            self.assertEqual(self.results[test_index][0],
                             self.balls[test_index].position)
            self.assertFalse(ball_to_box(self.balls[test_index],
                                         self.box, True))

    def test_vertex_collision(self):
        for test_index in [34, 35, 36, 37, 38, 39, 40, 43, 44, 45, 46, 47, 48,
                           49, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65,
                           66, 67]:
            result = ball_to_box(self.balls[test_index], self.box, True)
            self.assertEqual(self.results[test_index][1], result)
            self.assertEqual(self.results[test_index][0],
                             self.balls[test_index].position)
            self.assertFalse(ball_to_box(self.balls[test_index],
                                         self.box, True))

    def test_vertex_limit_collision(self):
        for test_index in [4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29,
                           30, 31]:
            result = ball_to_box(self.balls[test_index], self.box, True)
            self.assertEqual(self.results[test_index][1], result)
            self.assertEqual(self.results[test_index][0],
                             self.balls[test_index].position)
            self.assertFalse(ball_to_box(self.balls[test_index],
                                         self.box, True))

    def test_no_collision(self):
        result = ball_to_box(self.balls[68], self.box, True)
        self.assertEqual(self.results[68][1], result)
        self.assertEqual(self.results[68][0], self.balls[68].position)
        self.assertFalse(ball_to_box(self.balls[68], self.box, True))


class CalculateAngleTest(unittest.TestCase):

    def test_angle(self):
        self.assertAlmostEqual(0, calc_angle(Vec2D(1, 0)))
        self.assertAlmostEqual(30, calc_angle(Vec2D((3**.5) / 2, .5)))
        self.assertAlmostEqual(30, calc_angle(Vec2D((3**.5) / 2, -.5)))
        self.assertAlmostEqual(45, calc_angle(Vec2D(1, 1)))
        self.assertAlmostEqual(45, calc_angle(Vec2D(1, -1)))
        self.assertAlmostEqual(60, calc_angle(Vec2D(.5, (3**.5) / 2)))
        self.assertAlmostEqual(60, calc_angle(Vec2D(.5, -(3**.5) / 2)))
        self.assertAlmostEqual(90, calc_angle(Vec2D(0, 1)))
        self.assertAlmostEqual(90, calc_angle(Vec2D(0, -1)))
        self.assertAlmostEqual(120, calc_angle(Vec2D(-.5, (3**.5) / 2)))
        self.assertAlmostEqual(120, calc_angle(Vec2D(-.5, -(3**.5) / 2)))
        self.assertAlmostEqual(135, calc_angle(Vec2D(-1, 1)))
        self.assertAlmostEqual(135, calc_angle(Vec2D(-1, -1)))
        self.assertAlmostEqual(150, calc_angle(Vec2D(-(3**.5) / 2, .5)))
        self.assertAlmostEqual(150, calc_angle(Vec2D(-(3**.5) / 2, -.5)))
        self.assertAlmostEqual(180, calc_angle(Vec2D(-1, 0)))


class BoxToBoxCollisionTest(unittest.TestCase):

    def setUp(self):
        self.box = Obstacle(Vec2D(200, 200), Vec2D(200, 200))
        self.test_boxes = []
        self.test_boxes.append(Obstacle(Vec2D(400, 100), Vec2D(100, 250)))
        self.test_boxes.append(Obstacle(Vec2D(100, 400), Vec2D(250, 100)))
        self.test_boxes.append(Obstacle(Vec2D(100, 200), Vec2D(250, 100)))
        self.test_boxes.append(Obstacle(Vec2D(100, 200), Vec2D(250, 300)))
        self.test_boxes.append(Obstacle(Vec2D(200, 100), Vec2D(100, 250)))
        self.test_boxes.append(Obstacle(Vec2D(200, 100), Vec2D(300, 250)))
        self.test_boxes.append(Obstacle(Vec2D(200, 200), Vec2D(300, 100)))
        self.test_boxes.append(Obstacle(Vec2D(200, 200), Vec2D(100, 100)))
        self.test_boxes.append(Obstacle(Vec2D(200, 200), Vec2D(100, 300)))
        self.test_boxes.append(Obstacle(Vec2D(200, 200), Vec2D(300, 300)))
        self.test_boxes.append(Obstacle(Vec2D(200, 200), Vec2D(300, -50)))
        self.test_boxes.append(Obstacle(Vec2D(200, 200), Vec2D(500, 500)))
        self.test_boxes.append(Obstacle(Vec2D(200, 200), Vec2D(500, 300)))
        self.test_boxes.append(Obstacle(Vec2D(200, 200), Vec2D(400, 200)))
        self.test_boxes.append(Obstacle(Vec2D(200, 200), Vec2D(200, 0)))
        self.player_results = []
        self.test_boxes.append(Obstacle(Vec2D(80, 100), Vec2D(200, 105)))
        self.player_results.append(Vec2D(200, 100))
        self.test_boxes.append(Obstacle(Vec2D(80, 100), Vec2D(350, 115)))
        self.player_results.append(Vec2D(400, 115))
        self.test_boxes.append(Obstacle(Vec2D(80, 100), Vec2D(250, 115)))
        self.player_results.append(Vec2D(120, 115))

    def tearDown(self):
        del self.box
        del self.test_boxes
        del self.player_results

    def test_inside(self):
        for test_index in range(0, 2):
            self.assertTrue(box_to_box(self.test_boxes[test_index], self.box))

    def test_outside(self):
        for test_index in range(2, 6):
            self.assertTrue(box_to_box(self.test_boxes[test_index], self.box))

    def test_vertex(self):
        for test_index in range(6, 10):
            self.assertTrue(box_to_box(self.test_boxes[test_index], self.box))

    def test_no_collision(self):
        for test_index in range(10, 13):
            self.assertFalse(box_to_box(self.test_boxes[test_index], self.box))

    def test_adjacent_edge(self):
        for test_index in range(13, 15):
            self.assertFalse(box_to_box(self.test_boxes[test_index], self.box))

if __name__ == '__main__':
    unittest.main()
