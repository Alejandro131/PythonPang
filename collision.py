import math
from pang.settings import *
from pang.vec2d import Vec2D
from pang.hook import HookType


def calc_angle(point):
    """Function that takes a Vec2D object and calculates the angle between it
    and the vector with coordinates (1, 0)
    """
    x1, y1 = 1, 0
    x2, y2 = point.x, point.y
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return 180 * math.acos(inner_product/(len1*len2)) / math.pi


def ball_to_box(ball, box, solid=False):
    """Ball to box collision detection algorithm using voronoi regions.
    Calculates which region the ball is in based on this map:
    1|2|3
    4|0|5
    6|7|8
    Fixates the ball's position so that the objects no longer collide if solid
    is set to True and returns a Vec2D object representing the directions
    which the ball needs to change.
    """
    radius = ball.radius
    region = -1
    box_x_edge = 0
    box_y_edge = 0
    force_x = 0
    force_y = 0
    ball_x_fixate = 0
    ball_y_fixate = 0
    if ball.x > box.x + box.width:  # 3 or 5 or 8
        if ball.y > box.y + box.height:  # 8
            box_x_edge = box.x + box.width
            box_y_edge = box.y + box.height
            if (ball.x-box_x_edge)**2 + (ball.y-box_y_edge)**2 < radius**2:
                region = 8
        elif ball.y < box.y:  # 3
            box_x_edge = box.x + box.width
            box_y_edge = box.y
            if (ball.x-box_x_edge)**2 + (ball.y-box_y_edge)**2 < radius**2:
                region = 3
        else:  # 5
            if box.x + box.width >= ball.x - radius:
                region = 5
                ball_x_fixate = 2 * (box.x+box.width-(ball.x-radius))
                force_x = -1
    elif ball.x < box.x:  # 1 or 4 or 6
        if ball.y > box.y + box.height:  # 6
            box_x_edge = box.x
            box_y_edge = box.y + box.height
            if (ball.x-box_x_edge)**2 + (ball.y-box_y_edge)**2 < radius**2:
                region = 6
        elif ball.y < box.y:  # 1
            box_x_edge = box.x
            box_y_edge = box.y
            if (ball.x-box_x_edge)**2 + (ball.y-box_y_edge)**2 < radius**2:
                region = 1
        else:  # 4
            if box.x <= ball.x + radius:
                region = 4
                ball_x_fixate = 2 * (box.x-(ball.x+radius))
                force_x = -1
    else:  # 2 or 7 or 0
        if ball.y >= box.y + box.height:  # 7
            if box.y + box.height >= ball.y - radius:
                region = 7
                ball_y_fixate = 2 * (box.y+box.height-(ball.y-radius))
                force_y = -1
        elif ball.y <= box.y:  # 2
            if box.y <= ball.y + radius:
                region = 2
                ball_y_fixate = 2 * (box.y-(ball.y+radius))
                force_y = -1
        else:  # 0
            region = 0
            if ball.force.y >= 0:  # this is actually the same as 2
                ball_y_fixate = 2 * (box.y-(ball.y+radius))
                force_y = -1
            else:  # this is actually the same as 7
                ball_y_fixate = 2 * (box.y+box.height-(ball.y-radius))
                force_y = -1
    if solid:
        if region in [1, 3, 6, 8]:

            delta_x = ball.x - box_x_edge
            delta_y = ball.y - box_y_edge

            if region in [1, 6]:
                if ball.force.x > 0:
                    force_x = -1
            else:
                if ball.force.x < 0:
                    force_x = -1

            if region in [1, 3]:
                if ball.force.y > 0:
                    force_y = -1
            else:
                if ball.force.y < 0:
                    force_y = -1

            angle = calc_angle(Vec2D(delta_x, delta_y))
            if angle > 90.5:
                angle %= 90

            if region in [1, 6]:
                if angle <= 31:
                    force_x = 0
                elif angle >= 59:
                    force_y = 0
            else:
                if angle <= 31:
                    force_y = 0
                elif angle >= 59:
                    force_x = 0

            if force_x and force_y:
                force_length = ((delta_x)**2+(delta_y)**2) ** .5
                lengthen_y = radius/force_length - 1
                lengthen_x = lengthen_y * ball.force.x / ball.force.y
                ball_x_fixate = 2 * delta_x * lengthen_x
                ball_y_fixate = 2 * delta_y * lengthen_y
            elif force_x:
                x_pos = (radius**2-(box_y_edge-ball.y)**2) ** .5
                if ball.x > box_x_edge:
                    x_pos = ball.x - x_pos
                    ball_x_fixate = 2 * (box_x_edge-x_pos)
                else:
                    x_pos += ball.x
                    ball_x_fixate = 2 * (box_x_edge-x_pos)
            elif force_y:
                y_pos = (radius**2-(box_x_edge-ball.x)**2) ** .5
                if ball.y > box_y_edge:
                    y_pos = ball.y - y_pos
                    ball_y_fixate = 2 * (box_y_edge-y_pos)
                else:
                    y_pos += ball.y
                    ball_y_fixate = 2 * (box_y_edge-y_pos)

            ball.position += (ball_x_fixate, ball_y_fixate)

        elif region in [0, 2, 4, 5, 7]:
            ball.position += (ball_x_fixate, ball_y_fixate)

    if region != -1:
        return Vec2D(force_x, force_y)


def player_to_ladder(player, box):
    center_x = player.x + player.width/2
    if int(center_x) in range(int(box.x), int(box.x + box.width) + 1):
        if int(player.y + player.height) in \
           range(int(box.y), int(box.y + box.height) + 1):
            return True


def box_to_box(box1, box2, player=False, bonus=False, hook=False):
    """Separating Axis Theorem used for AABB collision and different fixations
    based on parameters. If one of the flags is set to True, the first object
    should be movable and the second static.
    """
    if (abs(box1.x + box1.width/2 - (box2.x+box2.width/2)) >=
       (box1.width/2 + box2.width/2)):
        return False

    if (abs(box1.y + box1.height/2 - (box2.y+box2.height/2)) >=
       (box1.height/2 + box2.height/2)):
        return False

    if player:
        if int(box1.y + box1.height) in range(int(box2.y + 10)):
            box1.position = Vec2D(box1.x, box2.y - box1.height)
            box1.force = Vec2D(box1.force.x, 0)
        else:
            if box1.x + box1.width - box2.x < box2.x + box2.width - box1.x:
                box1.position = Vec2D(box2.x - box1.width, box1.y)
            else:
                box1.position = Vec2D(box2.x + box2.width, box1.y)

    if bonus:
        box1.position = Vec2D(box1.x, box2.y - box1.height)
        box1.force = Vec2D(box1.force.x, 0)
        box1.fall = False

    if hook and box1.y > box2.y:
        if box1.hook_type == HookType.chain:
            fixation = box2.y + box2.height - box1.y
            box1.position += (0, fixation)
            box1.size -= (0, fixation)
            box1.expand = False
        elif box1.hook_type == HookType.rope:
            box1.to_kill = True

    return True
