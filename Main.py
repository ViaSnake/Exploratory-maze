
import pyxel
import random
import json

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.u = 0
        self.v = 0
        self.last_vector = None
        self.last_move = 0
        self.point = 0
        self.last_draw_vector = None
        self.data_json = "assets/points.json"

    def get_x(self):
        return int(self.x)

    def set_x(self, value):
        self.x = value

    def get_y(self):
        return int(self.y)

    def set_y(self, value):
        self.y = value

    def get_u(self):
        return int(self.u)

    def set_u(self, value):
        self.u = value

    def get_v(self):
        return int(self.v)

    def set_v(self, value):
        self.v = value

    def get_last_vector(self):
        return str(self.last_vector)

    def set_last_vector(self, value):
        self.last_vector = value

    def get_last_draw_vector(self):
        return str(self.last_draw_vector)

    def set_last_draw_vector(self, value):
        self.last_draw_vector = value

    def get_last_move(self):
        return int(self.last_move)

    def set_last_move(self, value):
        self.last_move = value

    def get_player_x(self):
        x = int(self.x)
        u = int(self.u)
        return x / 8 + u

    def get_player_y(self):
        y = int(self.y)
        v = int(self.v)
        return y / 8 + v

    def get_point(self):
        return int(self.point)

    def get_tile_point(self, tile):
        data = json.load(open(self.data_json, 'r'))
        point = data['tiles'][str(tile)]
        return int(point)

    def add_tile_point(self, tile):
        data = json.load(open(self.data_json, 'r'))
        point = data['tiles'][str(tile)]
        self.point += int(point)

class Time:
    def __init__(self):
        self.time = 0

    def get_time(self):
        return self.time

    def count(self):
        self.time += 1
        
class Map:
    def __init__(self):
        self.tilemap = None
        self.data_json = 'assets/maps.json'

    def set_tilemap(self, tilemap):
        self.tilemap = tilemap

    def get_tilemap(self):
        return self.tilemap

    def get_start_x(self):
        tm = str(self.tilemap)
        data = json.load(open(self.data_json, 'r'))
        start_x = data[tm]['start']['x']

        return start_x

    def get_start_y(self):
        tm = str(self.tilemap)
        data = json.load(open(self.data_json, 'r'))
        start_y = data[tm]['start']['y']

        return start_y

    def get_warp_x(self, tile):
        tm = str(self.tilemap)
        tile = str(tile)
        data = json.load(open(self.data_json, 'r'))
        warp_x = data[tm]['warps'][tile]['x']

        return warp_x

    def get_warp_y(self, tile):
        tm = str(self.tilemap)
        tile = str(tile)
        data = json.load(open(self.data_json, 'r'))
        warp_y = data[tm]['warps'][tile]['y']

        return warp_y

    def get_warp_u(self, tile):
        tm = str(self.tilemap)
        tile = str(tile)
        data = json.load(open(self.data_json, 'r'))
        warp_u = data[tm]['warps'][tile]['u']

        return warp_u

    def get_warp_v(self, tile):
        tm = str(self.tilemap)
        tile = str(tile)
        data = json.load(open(self.data_json, 'r'))
        warp_v = data[tm]['warps'][tile]['v']

        return warp_v

class Score:
    def __init__(self):
        self.score = 0

    def set(self, value):
        self.score = value

    def get(self):
        return self.score

class Log:
    def __init__(self):
        self.log = []

    def append(self, item):
        self.log.append(item)

    def get(self, value):
        item = self.log[value]
        return item

    def get_length(self):
        length = len(self.log)
        return length

class Main:
    def __init__(self):
        pyxel.init(128, 160, caption="Exploratory maze", fps=60)
        pyxel.load('assets/tilemap.pyxres', True, True, False, False)

        self.Map = Map()
        self.Score = Score()
        self.Log = Log()

        self.isFirstStartup = True
        self.isGamedClear = False
        self.isGamedOver = False
        self.isInitialized = False
        self.isHard = False

        self.isTitle = True
        self.isInProgress = False

        self.Log.append("Load completed")
        self.Log.append("Version 2.0.3")

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_G):
            if self.isHard == True:
                self.isHard = False
                self.isInitialized = False
                self.Log.append("STATIC MAP MODE!")
            else:
                self.isHard = True
                self.isInitialized = False
                self.Log.append("DYNAMIC MAP MODE!")

        if self.isInitialized == False:
            self.initialize()

        if self.isTitle:

            if (pyxel.mouse_x >= 8 * 4 and pyxel.mouse_x <= 8 * 12 and
                    pyxel.mouse_y >= 8 * 8 and pyxel.mouse_y <= 8 * 10):

                if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                    self.isTitle = False
                    self.isInProgress = True
                    self.Log.append("GAME START")

            elif (pyxel.mouse_x >= 8 * 4 and pyxel.mouse_x <= 8 * 12 and
                  pyxel.mouse_y >= 8 * 12 and pyxel.mouse_y <= 8 * 14):

                if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                    pyxel.quit()

        elif self.isInProgress:

            if pyxel.btnp(pyxel.KEY_R):
                self.isInitialized = False
                self.isTitle = True

            if self.Time.get_time() == 15000:
                self.isGamedOver = True
                self.Log.append("Time over")

            if self.isGamedClear or self.isGamedOver:
                self.isInProgress = False

            self.player_control()
            self.Time.count()

        elif self.isGamedClear or self.isGamedOver:
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                self.isGamedClear = False
                self.isGamedOver = False
                self.isInitialized = False
                self.isTitle = True

    def draw(self):
        x = self.Player.get_x()
        y = self.Player.get_y()
        tm = self.Map.get_tilemap()
        u = self.Player.get_u()
        v = self.Player.get_v()

        pyxel.cls(0)

        # MESSAGE
        pyxel.rectb(2, 130, 76, 28, 7)
        pyxel.rectb(80, 130, 46, 28, 7)

        pyxel.text(5, 133, self.Log.get(self.Log.get_length() - 1), 7)
        pyxel.text(5, 140, self.Log.get(self.Log.get_length() - 2), 7)
        pyxel.text(5, 147, self.Log.get(self.Log.get_length() - 3), 7)

        pyxel.text(83, 133, "{0:>3} POINT".format(self.Player.get_point()), 7)
        pyxel.text(83, 140, "{0:>.1f} SEC".format(
            self.Time.get_time() / 60), 7)

        if self.isTitle:

            pyxel.mouse(True)

            # bltm(x, y, tm, u, v, w, h, [colkey])
            pyxel.bltm(0, 0, 0, 0, 0, 16, 16)

            pyxel.text(128 / 2 - (3 * len("Exploratory maze") +
                                  (len("Exploratory maze") - 1)) / 2, 8 * 3, "Exploratory maze", 0)

            # START : WIDTH 19 dots, HEIGHT 5 dots
            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * len("START") +
                                  (len("START") - 1)) / 2, 8 * 9 - 2, "START", 0)

            # EXIT : WIDTH 15 dots, HEIGHT 5 dots
            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * len("EXIT") + (len("EXIT") - 1)
                                  ) / 2,  8 * 13 - 2, "EXIT", 0)

        elif self.isInProgress:

            pyxel.mouse(False)

            # bltm(x, y, tm, u, v, w, h, [colkey])
            pyxel.bltm(0, 0, tm, u, v, 16, 16)

            if self.Player.get_last_vector() == "RIGHT":
                # blt(x, y, img, u, v, w, h, [colkey])
                pyxel.blt(x, y, 1, 8, 0, 8, 8, 4)
                self.Player.set_last_draw_vector("RIGHT")

            elif self.Player.get_last_vector() == "LEFT":
                # blt(x, y, img, u, v, w, h, [colkey])
                pyxel.blt(x, y, 1, 16, 0, 8, 8, 4)
                self.Player.set_last_draw_vector("LEFT")

            elif (self.Player.get_last_vector() == "UP" or self.Player.get_last_vector() == "DOWN") and self.Player.get_last_draw_vector() == "RIGHT":
                # blt(x, y, img, u, v, w, h, [colkey])
                pyxel.blt(x, y, 1, 8, 0, 8, 8, 4)
                self.Player.set_last_draw_vector("RIGHT")

            elif (self.Player.get_last_vector() == "UP" or self.Player.get_last_vector() == "DOWN") and self.Player.get_last_draw_vector() == "LEFT":
                # blt(x, y, img, u, v, w, h, [colkey])
                pyxel.blt(x, y, 1, 16, 0, 8, 8, 4)
                self.Player.set_last_draw_vector("LEFT")

            else:
                # blt(x, y, img, u, v, w, h, [colkey])
                pyxel.blt(x, y, 1, 8, 0, 8, 8, 4)
                self.Player.set_last_draw_vector("RIGHT")

        elif self.isGamedClear:

            score = str(round(self.Score.get()))
            time = str(round(self.Time.get_time() / 60, 1))

            pyxel.mouse(True)

            # bltm(x, y, tm, u, v, w, h, [colkey])
            pyxel.bltm(0, 0, 0, 16, 0, 16, 16)

            # CLEAR : WIDTH 15 dots, HEIGHT 5 dots
            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * len("CLEAR") + (len("CLEAR") - 1)) / 2,
                       128 / 16 * 4 - 5 / 2, "CLEAR", 0)

            # SCORE : WIDTH 15 dots, HEIGHT 5 dots
            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * 5 + 4) / 2,
                       128 / 2, "SCORE", 0)

            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * len(score) + (len(score) - 1)
                                  ) / 2, 128 / 2 + 8, "{0}".format(score), 0)

            # TIME : WIDTH 15 dots, HEIGHT 5 dots
            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * 4 + 3) / 2,
                       128 / 2 + 20, "TIME", 0)

            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * len(time) + (len(time)) - 1) /
                       2, 128 / 2 + 28, "{0} sec".format(time), 0)

        elif self.isGamedOver:

            score = str(round(self.Score.get()))
            time = str(round(self.Time.get_time() / 60, 1))

            pyxel.mouse(True)

            # bltm(x, y, tm, u, v, w, h, [colkey])
            pyxel.bltm(0, 0, 0, 16, 0, 16, 16)

            # CLEAR : WIDTH 15 dots, HEIGHT 5 dots
            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * len("GAME OVER") + (len("GAME OVER") - 1)) / 2,
                       128 / 16 * 4 - 5 / 2, "GAME OVER", 0)

            # SCORE : WIDTH 15 dots, HEIGHT 5 dots
            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * 5 + 4) / 2,
                       128 / 2, "SCORE", 0)

            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * len(score) + (len(score) - 1)
                                  ) / 2, 128 / 2 + 8, "{0}".format(score), 0)

            # TIME : WIDTH 15 dots, HEIGHT 5 dots
            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * 4 + 3) / 2,
                       128 / 2 + 20, "TIME", 0)

            # text(x, y, s, col)
            pyxel.text(128 / 2 - (3 * len(time) + (len(time)) - 1) /
                       2, 128 / 2 + 28, "{0} sec".format(time), 0)

    def player_control(self):
        x = self.Player.get_x()
        y = self.Player.get_y()
        u = self.Player.get_u()
        v = self.Player.get_v()
        player_x = self.Player.get_player_x()
        player_y = self.Player.get_player_y()
        tm = self.Map.get_tilemap()
        last_vector = self.Player.get_last_vector()
        self.Player.set_last_move(self.Player.get_last_move() + 1)
        last_move = self.Player.get_last_move()

        if last_move > 8:
            if ((pyxel.tilemap(tm).get(player_x, player_y - 1) >= 128 and pyxel.tilemap(tm).get(player_x, player_y - 1) < 160) or
                    (pyxel.tilemap(tm).get(player_x, player_y - 1) >= 32 and pyxel.tilemap(tm).get(player_x, player_y - 1) < 96)):
                if (pyxel.btn(pyxel.KEY_W) and pyxel.btn(pyxel.KEY_S) == False or
                        pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_DOWN) == False or
                        pyxel.btn(pyxel.GAMEPAD_1_UP) and pyxel.btn(pyxel.GAMEPAD_1_DOWN) == False or
                        pyxel.btn(pyxel.GAMEPAD_2_UP) and pyxel.btn(pyxel.GAMEPAD_2_DOWN) == False):
                    self.Player.set_last_move(0)
                    self.Player.set_last_vector("UP")
                    if y < 8:
                        self.Player.set_v(v - 16)
                        self.Player.set_y(8 * 16)

            if ((pyxel.tilemap(tm).get(player_x, player_y + 1) >= 128 and pyxel.tilemap(tm).get(player_x, player_y + 1) < 160) or
                    (pyxel.tilemap(tm).get(player_x, player_y + 1) >= 32 and pyxel.tilemap(tm).get(player_x, player_y + 1) < 96)):
                if (pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_W) == False or
                        pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_UP) == False or
                        pyxel.btn(pyxel.GAMEPAD_1_DOWN) and pyxel.btn(pyxel.GAMEPAD_1_UP) == False or
                        pyxel.btn(pyxel.GAMEPAD_2_DOWN) and pyxel.btn(pyxel.GAMEPAD_2_UP) == False):
                    self.Player.set_last_move(0)
                    self.Player.set_last_vector("DOWN")
                    if y > 112:
                        self.Player.set_v(v + 16)
                        self.Player.set_y(-8)

            if ((pyxel.tilemap(tm).get(player_x - 1, player_y) >= 128 and pyxel.tilemap(tm).get(player_x - 1, player_y) < 160) or
                    (pyxel.tilemap(tm).get(player_x - 1, player_y) >= 32 and pyxel.tilemap(tm).get(player_x - 1, player_y) < 96)):
                if (pyxel.btn(pyxel.KEY_A) and pyxel.btn(pyxel.KEY_D) == False or
                        pyxel.btn(pyxel.KEY_LEFT) and pyxel.btn(pyxel.KEY_RIGHT) == False or
                        pyxel.btn(pyxel.GAMEPAD_1_LEFT) and pyxel.btn(pyxel.GAMEPAD_1_RIGHT) == False or
                        pyxel.btn(pyxel.GAMEPAD_2_LEFT) and pyxel.btn(pyxel.GAMEPAD_2_RIGHT) == False):
                    self.Player.set_last_move(0)
                    self.Player.set_last_vector("LEFT")
                    if x < 8:
                        self.Player.set_u(u - 16)
                        self.Player.set_x(8 * 16)

            if ((pyxel.tilemap(tm).get(player_x + 1, player_y) >= 128 and pyxel.tilemap(tm).get(player_x + 1, player_y) < 160) or
                    (pyxel.tilemap(tm).get(player_x + 1, player_y) >= 32 and pyxel.tilemap(tm).get(player_x + 1, player_y) < 96)):
                if (pyxel.btn(pyxel.KEY_D) and pyxel.btn(pyxel.KEY_A) == False or
                        pyxel.btn(pyxel.KEY_RIGHT) and pyxel.btn(pyxel.KEY_LEFT) == False or
                        pyxel.btn(pyxel.GAMEPAD_1_RIGHT) and pyxel.btn(pyxel.GAMEPAD_1_LEFT) == False or
                        pyxel.btn(pyxel.GAMEPAD_2_RIGHT) and pyxel.btn(pyxel.GAMEPAD_2_LEFT) == False):
                    self.Player.set_last_move(0)
                    self.Player.set_last_vector("RIGHT")
                    if x > 112:
                        self.Player.set_u(u + 16)
                        self.Player.set_x(-8)

            if (pyxel.tilemap(tm).get(player_x, player_y) >= 64 and pyxel.tilemap(tm).get(player_x, player_y) < 96):
                tile = pyxel.tilemap(tm).get(player_x, player_y)

                self.Player.add_tile_point(tile)
                pyxel.tilemap(tm).set(player_x, player_y, 128)
                self.Log.append("GOT {0} POINTS".format(
                    self.Player.get_tile_point(tile)))

            if pyxel.tilemap(tm).get(player_x, player_y) == 33:
                self.Player.set_x(self.Map.get_warp_x(33))
                self.Player.set_y(self.Map.get_warp_y(33))
                self.Player.set_u(self.Map.get_warp_u(33))
                self.Player.set_v(self.Map.get_warp_v(33))
                self.Log.append("WARP!")

            if pyxel.tilemap(tm).get(player_x, player_y) == 34:
                self.Player.set_x(self.Map.get_warp_x(34))
                self.Player.set_y(self.Map.get_warp_y(34))
                self.Player.set_u(self.Map.get_warp_u(34))
                self.Player.set_v(self.Map.get_warp_v(34))
                self.Log.append("WARP!")

            if pyxel.tilemap(tm).get(player_x, player_y) == 32:
                self.isGamedClear = True
                self.isinitialized = False

                point = self.Player.get_point()
                time = self.Time.get_time() / 60

                self.Score.set(point * 700 + (1 / (time) * 1000) * 10)
                self.Log.append("GAME CLEAR")

        elif last_move <= 8:
            if last_vector == "UP":
                self.Player.set_y(y - 1)
            elif last_vector == "DOWN":
                self.Player.set_y(y + 1)
            elif last_vector == "LEFT":
                self.Player.set_x(x - 1)
            elif last_vector == "RIGHT":
                self.Player.set_x(x + 1)

    def initialize(self):
        self.Log.append("Iinitialize...")
        self.Time = Time()
        self.Score = Score()
        pyxel.load('assets/tilemap.pyxres', True, True, False, False)

        if self.isHard:
            self.Map.set_tilemap(6)
            self.generator()
        else:
            self.Map.set_tilemap(random.randint(1, 5))

        self.Player = Player(self.Map.get_start_x(), self.Map.get_start_y())
        self.isInitialized = True

    def generator(self):
        TILEMAP = []
        WIDTH = 33
        HEIGHT = 33
        _list = [64, 64, 64, 64, 64, 64, 64, 64, 64,
                 64, 65, 65, 65, 65, 65, 66, 66, 66, 67, 67]
        _list = _list + [128]*(16*16 - len(_list))

        for x in range(0, WIDTH):
            row = []
            for y in range(0, HEIGHT):
                if (x == 0 or y == 0 or x == WIDTH - 1 or y == HEIGHT - 1):
                    tile = 192
                else:
                    tile = 128
                row.append(tile)
            TILEMAP.append(row)

        for x in range(2, WIDTH - 1, 2):
            for y in range(2, HEIGHT - 1, 2):
                TILEMAP[x][y] = 192
                while True:
                    if y == 2:
                        direction = random.randrange(0, 4)
                    else:
                        direction = random.randrange(0, 3)
                    _x = x
                    _y = y
                    if direction == 0:
                        _x += 1
                    elif direction == 1:
                        _y += 1
                    elif direction == 2:
                        _x -= 1
                    elif direction == 3 or direction == 4:
                        _y -= 1
                    if TILEMAP[_x][_y] != 192:
                        TILEMAP[_x][_y] = 192
                        break

        while(_list):
            for x in range(1, WIDTH - 2, 2):
                for y in range(1, HEIGHT - 2, 2):
                    wall_count = 0
                    if TILEMAP[x + 1][y] == 192:
                        wall_count += 1
                    if TILEMAP[x - 1][y] == 192:
                        wall_count += 1
                    if TILEMAP[x][y + 1] == 192:
                        wall_count += 1
                    if TILEMAP[x][y - 1] == 192:
                        wall_count += 1
                    if random.random() <= 0.5 and wall_count >= 3 and _list:
                        choice = random.choice(_list)
                        TILEMAP[x][y] = choice
                        _list.remove(choice)

        TILEMAP[WIDTH - 2][HEIGHT - 2] = 32
        _x = 0
        _y = 0

        for row in TILEMAP:
            _x = 0
            for tile in row:
                if tile == 128:
                    pyxel.tilemap(6).set(_x, _y, 128)
                    pyxel.tilemap(6).set(_x + 1, _y, 128)
                    pyxel.tilemap(6).set(_x, _y + 1, 128)
                    pyxel.tilemap(6).set(_x + 1, _y + 1, 128)
                elif tile == 192:
                    pyxel.tilemap(6).set(_x, _y, 192)
                    pyxel.tilemap(6).set(_x + 1, _y, 192)
                    pyxel.tilemap(6).set(_x, _y + 1, 192)
                    pyxel.tilemap(6).set(_x + 1, _y + 1, 192)
                elif tile == 64:
                    pyxel.tilemap(6).set(_x, _y, 64)
                    pyxel.tilemap(6).set(_x + 1, _y, 128)
                    pyxel.tilemap(6).set(_x, _y + 1, 128)
                    pyxel.tilemap(6).set(_x + 1, _y + 1, 128)
                elif tile == 65:
                    pyxel.tilemap(6).set(_x, _y, 65)
                    pyxel.tilemap(6).set(_x + 1, _y, 128)
                    pyxel.tilemap(6).set(_x, _y + 1, 128)
                    pyxel.tilemap(6).set(_x + 1, _y + 1, 128)
                elif tile == 66:
                    pyxel.tilemap(6).set(_x, _y, 66)
                    pyxel.tilemap(6).set(_x + 1, _y, 128)
                    pyxel.tilemap(6).set(_x, _y + 1, 128)
                    pyxel.tilemap(6).set(_x + 1, _y + 1, 128)
                elif tile == 67:
                    pyxel.tilemap(6).set(_x, _y, 67)
                    pyxel.tilemap(6).set(_x + 1, _y, 128)
                    pyxel.tilemap(6).set(_x, _y + 1, 128)
                    pyxel.tilemap(6).set(_x + 1, _y + 1, 128)
                elif tile == 32:
                    pyxel.tilemap(6).set(_x, _y, 128)
                    pyxel.tilemap(6).set(_x + 1, _y, 128)
                    pyxel.tilemap(6).set(_x, _y + 1, 128)
                    pyxel.tilemap(6).set(_x + 1, _y + 1, 32)
                _x += 2
            _y += 2


if __name__ == '__main__':
    Main()
