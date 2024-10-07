# -*- coding: utf-8 -*-
import math
import random
import cocos
from cocos.sprite import Sprite

import define
from dot import Dot


class Snake(cocos.cocosnode.CocosNode):
    no = 0
    IDLE, CHASE, FLEE = range(3)  # 状态定义

    def __init__(self, is_enemy=False):
        super(Snake, self).__init__()
        self.is_dead = False
        self.angle = random.randrange(360)  # 目前角度
        self.angle_dest = self.angle  # 目标角度
        self.color = random.choice(define.ALL_COLOR)
        self.no = Snake.no
        Snake.no += 1
        if is_enemy:
            self.position = random.randrange(300, 1300), random.randrange(200, 600)
            if 600 < self.x < 1000:
                self.x += 400
            self.state = Snake.IDLE  # 初始状态
            self.chase_distance = 30  # 追踪距离
        else:
            self.position = random.randrange(700, 900), random.randrange(350, 450)
        self.is_enemy = is_enemy
        self.head = Sprite('circle.png', color=self.color)
        self.scale = 1.5
        eye = Sprite('circle.png')
        eye.y = 5
        eye.scale = 0.5
        eyeball = Sprite('circle.png', color=define.BLACK)
        eyeball.scale = 0.5
        eye.add(eyeball)
        self.head.add(eye)
        eye = Sprite('circle.png')
        eye.y = -5
        eye.scale = 0.5
        eyeball = Sprite('circle.png', color=define.BLACK)
        eyeball.scale = 0.5
        eye.add(eyeball)
        self.head.add(eye)

        self.add(self.head)

        self.speed = 150
        if not is_enemy:
            self.speed = 180
        self.path = [self.position] * 100

        self.schedule(self.update)
        if self.is_enemy:
            self.schedule_interval(self.ai, random.random() * 0.1 + 0.05)

    def add_body(self):
        b = Sprite('circle.png', color=self.color)
        b.scale = 1.5
        self.body.append(b)
        if self.x == 0:
            print(self.position)
        b.position = self.position
        try:
            self.parent.batch.add(b, 999 + 100*self.no - len(self.body))
        except:
            print(999 + 100*self.no - len(self.body))

    def init_body(self):
        self.score = 30
        self.length = 4
        self.body = []
        for i in range(self.length):
            self.add_body()

    def update(self, dt):
        self.angle = (self.angle + 360) % 360

        arena = self.parent
        if self.is_enemy:
            self.check_crash(arena.snake)
        for s in arena.enemies:
            if s != self and not s.is_dead:
                self.check_crash(s)
        if self.is_dead:
            return

        if abs(self.angle - self.angle_dest) < 2:
            self.angle = self.angle_dest
        else:
            if (0 < self.angle - self.angle_dest < 180) or (
                self.angle - self.angle_dest < -180):
                self.angle -= 500 * dt
            else:
                self.angle += 500 * dt
        self.head.rotation = -self.angle

        self.x += math.cos(self.angle * math.pi / 180) * dt * self.speed
        self.y += math.sin(self.angle * math.pi / 180) * dt * self.speed
        self.path.append(self.position)

        lag = int(round(1100.0 / self.speed))
        for i in range(len(self.body)):
            idx = (i + 1) * lag + 1
            self.body[i].position = self.path[-min(idx,len(self.path))]
            if self.body[i].x == 0:
                print(self.body[i].position)
        m_l = max(self.length * lag * 2, 60)
        if len(self.path) > m_l:
            self.path = self.path[int(-m_l * 2):]

    def update_angle(self, keys):
        x, y = 0, 0
        if 65361 in keys:  # 左
            x -= 1
        if 65362 in keys:  # 上
            y += 1
        if 65363 in keys:  # 右
            x += 1
        if 65364 in keys:  # 下
            y -= 1
        directs = ((225, 180, 135), (270, None, 90), (315, 0, 45))
        direct = directs[x + 1][y + 1]
        if direct is None:
            self.angle_dest = self.angle
        else:
            self.angle_dest = direct

    def add_score(self, s=1):
        if self.is_dead:
            return
        self.score += s
        l = (self.score - 6) / 6
        if l > self.length:
            self.length = l
            self.add_body()
    def get_distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    def ai(self, dt):
        self.angle_dest = (self.angle_dest + 360) % 360
        if (self.x < 100 and 90 < self.angle_dest < 270) or (
            self.x > define.WIDTH - 100 and (
                self.angle_dest < 90 or self.angle_dest > 270)
        ):
            self.angle_dest = 180 - self.angle_dest
        elif (self.y < 100 and self.angle_dest > 180) or (
            self.y > define.HEIGHT - 100 and self.angle_dest < 180
        ):
            self.angle_dest = -self.angle_dest
        else:
            arena = self.parent
            self.collision_detect(arena.snake)
            for s in arena.enemies:
                if s != self:
                    self.collision_detect(s)
        arena = self.parent
        player_distance = self.get_distance(arena.snake)
        # 状态转换
        if player_distance < self.chase_distance:
            self.state = Snake.CHASE
        else:
            self.state = Snake.IDLE

        # 根据状态进行不同的行为
        if self.state == Snake.CHASE:
            self.chase(arena.snake)
        elif self.state == Snake.IDLE:
            self.idle_behavior()

        if player_distance < self.chase_distance:
            self.state = Snake.CHASE
        else:
            self.state = Snake.IDLE
        if self.state == Snake.CHASE:
            nearby_enemies = self.detect_nearby_enemies(arena.enemies)
            if nearby_enemies:
                self.avoid_nearby_enemies(nearby_enemies)  # 避免碰撞
            else:
                self.chase(arena.snake)
                # self.avoid_obstacle()  # 进行避障
        elif self.state == Snake.IDLE:
            self.idle_behavior()
        if self.state == Snake.CHASE:
            self.chase(arena.snake)
            # self.avoid_obstacle()  # 进行避障
        elif self.state == Snake.IDLE:
            self.idle_behavior()


    def detect_nearby_enemies(self, enemies):
        nearby_enemies = []  # 存储邻近的敌蛇位置
        for enemy in enemies:
            if enemy != self:  # 确保不检测自身
                for b in enemy.body:
                    if self.is_near(b):
                        nearby_enemies.append(b)  # 记录邻近的敌蛇身体部分位置
        return nearby_enemies

    def avoid_nearby_enemies(self, nearby_enemies):
        # 随机改变方向，确保不直接朝向敌蛇身体
        # 这里可以根据敌蛇的位置决定转向
        for b in nearby_enemies:
            angle_to_enemy = math.degrees(math.atan2(b.y - self.y, b.x - self.x))
            if abs(angle_to_enemy - self.angle_dest) < 45:  # 如果在目标角度附近
                self.angle_dest += random.choice([-90, 90])  # 随机转90度
                self.angle_dest = self.angle_dest % 360  # 确保角度在0-360范围内
    def chase(self, player):
        # 计算目标角度
        angle_to_player = math.degrees(math.atan2(player.y - self.y, player.x - self.x))
        self.angle_dest = (angle_to_player + 360) % 360

        # 检测邻近的敌蛇
        nearby_enemies = self.detect_nearby_enemies(self.parent.enemies)
        if nearby_enemies:
            self.avoid_nearby_enemies(nearby_enemies)  # 避免敌蛇
    # def avoid_obstacle(self):
    def idle_behavior(self):
        # 随机移动或改变方向
        if random.random() < 0.005:  # 0.5%概率改变方向
            self.angle_dest = random.randrange(360)
    # def check_obstacle(self, direction):
    #     # 简单的障碍物检测（假设有一些障碍物）
    #     for obstacle in self.parent.obstacles:  # 假设场景中有障碍物列表
    #         if self.is_near(obstacle):
    #             return True
    #     return False

    def is_near(self, obstacle):
        return math.sqrt((self.x - obstacle.x) ** 2 + (self.y - obstacle.y) ** 2) < 50

    # def avoid_obstacle(self):
    #     if self.check_obstacle(self.angle_dest):
    #         self.angle_dest += 90  # 随机改变方向

    def collision_detect(self, other):
        if self.is_dead or other.is_dead:
            return
        for b in other.body:
            d_y = b.y - self.y
            d_x = b.x - self.x
            if abs(d_x) > 200 or abs(d_y) > 200:
                return
            if d_x == 0:
                if d_y > 0:
                    angle = 90
                else:
                    angle = -90
            else:
                angle = math.atan(d_y / d_x) * 180 / math.pi
                if d_x < 0:
                    angle += 180
            angle = (angle + 360) % 360
            if abs(angle - self.angle_dest) < 5:
                self.angle_dest += random.randrange(90, 270)

    def check_crash(self, other):
        if self.is_dead or other.is_dead:
            return
        if (self.x < 0 or self.x > define.WIDTH) or (
            self.y < 0 or self.y > define.HEIGHT
        ):
            self.crash()
            return
        for b in other.body:
            dis = math.sqrt((b.x - self.x) ** 2 + (b.y - self.y) ** 2)
            if dis < 24:
                self.crash()
                return

    def crash(self):
        if not self.is_dead:
            self.is_dead = True
            self.unschedule(self.update)
            self.unschedule(self.ai)
            arena = self.parent
            for b in self.body:
                arena.batch.add(Dot(b.position, b.color))
                arena.batch.add(Dot(b.position, b.color))
                arena.batch.remove(b)

            arena.remove(self)
            arena.add_enemy()
            del self.path
            if self.is_enemy:
                arena.enemies.remove(self)
                del self.body
                del self
            else:
                arena.parent.end_game()
