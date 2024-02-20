import random
import numpy
import pprint

# 0 = space, 1 = player, 2 = enemy, 3 = obstacle

class Entity:
    at_x = 0
    at_y = 0
    size_x = 0
    size_y = 0
    symbol = 0

    def around(self, mapa):
        if self.at_x == 0:
            left = 3
        else:
            left = mapa[self.at_y][self.at_x - 1]
        if self.at_x == self.size_x - 1:
            right = 3
        else:
            right = mapa[self.at_y][self.at_x + 1]
        if self.at_y == 0:
            up = 3
        else:
            up = mapa[self.at_y - 1][self.at_x]
        if self.at_y == self.size_y - 1:
            down = 3
        else:
            down = mapa[self.at_y + 1][self.at_x]
        return (left, right, up, down)

    def spawn(self, mapa):
        while True:
            ran_x = random.randint(0, self.size_x - 1)
            ran_y = random.randint(0, self.size_y - 1)
            if mapa[ran_y][ran_x] == 0:
                mapa[ran_y][ran_x] = self.symbol
                self.at_x = ran_x
                self.at_y = ran_y
                return mapa
            else:
                continue

    def move(self, mapa, dir):
        if dir == "left":
            left = self.around(mapa)[0]
            if left == 0:
                mapa[self.at_y][self.at_x - 1] = self.symbol
                mapa[self.at_y][self.at_x] = 0
                self.at_x -= 1
                return mapa
            return left
        if dir == "right":
            right = self.around(mapa)[1]
            if right == 0:
                mapa[self.at_y][self.at_x + 1] = self.symbol
                mapa[self.at_y][self.at_x] = 0
                self.at_x += 1
                return mapa
            return right
        if dir == "up":
            up = self.around(mapa)[2]
            if up == 0:
                mapa[self.at_y - 1][self.at_x] = self.symbol
                mapa[self.at_y][self.at_x] = 0
                self.at_y -= 1
                return mapa
            return up
        if dir == "down":
            down = self.around(mapa)[3]
            if down == 0:
                mapa[self.at_y + 1][self.at_x] = self.symbol
                mapa[self.at_y][self.at_x] = 0
                self.at_y += 1
                return mapa
            return down

    def __init__(self, size_x, size_y, symbol):
        self.size_x = size_x 
        self.size_y = size_y 
        self.symbol = symbol 

def main(rate = 1):
    print("レート"+str(rate))
    size_x = 12
    size_y = 8
    mapa = [[0 for j in range(size_x)] for i in range(size_y)]
    enemy_count = rate
    flags = [0 for i in range(4)]

    achieved = 0
    player = Entity(size_x, size_y, 1)
    mapa = player.spawn(mapa)
    enemies = []

    for i in range(enemy_count):
        enemies.append(Entity(size_x, size_y, 2))
        mapa = enemies[i].spawn(mapa)
    while True:
        #pprint.pprint(mapa)
        printer(mapa, size_x, size_y, flags)
        key = input("移動したい方向を入力してください。left/right/up/down: ")
        if key == "l":
            key = "left"
        if key == "r":
            key = "right"
        if key == "u":
            key = "up"
        if key == "d":
            key = "down"
        if key != "left" and key != "right" and key != "up" and key != "down":
            continue
        moved = player.move(mapa, key)
        if moved == 3:
            pass
        if moved == 2:
            print("敵にぶつかりました")
            return 1
        enemy_moved = enemy_walk(mapa, enemies)
        if enemy_moved == 1:
            print("敵に捕まりました")
            return 1
        p_x = player.at_x
        p_y = player.at_y
        if p_x == 0 and p_y == 0:
            flags[0] = 1
        if p_x == size_x - 1 and p_y == 0:
            flags[1] = 1
        if p_x == 0 and p_y == size_y - 1:
            flags[2] = 1
        if p_x == size_x - 1 and p_y == size_y - 1:
            flags[3] = 1
        achieved = flags[0] + flags[1] + flags[2] + flags[3]
        if achieved == 4:
            print("ゲームクリア")
            break

def enemy_walk(mapa, entity):
    for i in entity:
        while True:
            ran = random.randint(0, 3)
            if ran == 0:
                dir = "right"
            if ran == 1:
                dir = "left"
            if ran == 2:
                dir = "up"
            if ran == 3:
                dir = "down"
            moved = i.move(mapa, dir)
            if moved == 2 or moved == 3:
                continue
            if moved == 1:
                return 1
            break

def printer(mapa, size_x, size_y, flags):
    for i in range(size_y):
        for j in range(size_x):
            char = mapa[i][j]
            if char == 0:
                #if flags[0] == true and 
                if j == 0 and i == 0 and flags[0] == 0:
                    print("\033[38;2;0;153;68m■ ", end="")
                    print("\x1b[39m", end="")
                elif j == size_x - 1 and i == 0 and flags[1] == 0:
                    print("\033[38;2;0;153;68m■ ", end="")
                    print("\x1b[39m", end="")
                elif j == 0 and i == size_y - 1 and flags[2] == 0:
                    print("\033[38;2;0;153;68m■ ", end="")
                    print("\x1b[39m", end="")
                elif j == size_x - 1 and i == size_y - 1 and flags[3] == 0:
                    print("\033[38;2;0;153;68m■ ", end="")
                    print("\x1b[39m", end="")
                else:
                    print("■ ", end="")
            elif char == 1:
                print("\033[38;2;0;160;233m■ ", end="")
                print("\x1b[39m", end="")
            elif char == 2:
                print("\033[38;2;230;0;18m■ ", end="")
                print("\x1b[39m", end="")
        print("")

if __name__ == "__main__":
    for i in range(20):
        returning = main(i + 1) 
        if returning == 1:
            break