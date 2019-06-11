
#--------------------------------------------------------------- LIBRARIES ---------------------------------------------------------------#

import pgzrun # pip install pgzero

#--------------------------------------------------------------- CONSTANTS ---------------------------------------------------------------#

WIDTH = 448
HEIGHT = 576

STRIDE = 16

#ROWS = HEIGHT / STRIDE
#COLS = WIDTH / STRIDE

#---------------------------------------------------------------- CLASSES ----------------------------------------------------------------#

class Game(object):

    def __init__(self):
        self.i = 0
        self.high_score = 0
        self.frames = 0
        self.one_up_score = 0
        self.level = 1
        self.state = 'load'
        self.background_image = 'load.png'
        self.background_position = (0, 0)
        self.ready_image = 'ready.png'
        self.ready_position = (11, 20)
        self.one_up_image = 'oneup.png'
        self.one_up_position = (4, 0)
        self.high_score_image = 'highscore.png'
        self.high_score_position = (9, 0)
        self.wall_positions = []

    def draw_background(self):
        draw_image(self.background_image, self.background_position)

    def draw_one_up(self):
        draw_image(self.one_up_image, self.one_up_position)
        self.draw_one_up_counter()

    def draw_one_up_counter(self):
        i = -1
        position = (6, 1)
        for character in str(self.one_up_score):
            i += 1
            draw_image(str(character), (position[0] + i, position[1]))

    def draw_high_score(self):
        draw_image(self.high_score_image, self.high_score_position)
        self.draw_high_score_counter()

    def draw_high_score_counter(self):
        i = -1
        position = (15, 1)
        for character in str(self.high_score):
            i += 1
            draw_image(str(character), (position[0] + i, position[1]))

    def draw_ready(self):
        draw_image(self.ready_image, self.ready_position)

    def find_characters(self):
        self.wall_positions = []
        small_pellet.positions = []
        large_pellet.positions = []
        with open('maze.txt', 'r') as file:
            for y, line in enumerate(file):
                for x, character in enumerate(line):
                    if character == '1':
                        self.wall_positions.append((x, y))
                    elif character == '2':
                        small_pellet.positions.append((x, y))
                    elif character == '3':
                        large_pellet.positions.append((x, y))

    def set_load(self):
        self.state = 'load'
        self.one_up_score = 0
        self.high_score = 0
        self.background_position = (0, 0)
        self.background_image = 'load.png'
        player.lives = 2
        self.find_characters()

    def set_start(self):
        self.state = 'start'
        self.background_position = (0, 3)
        self.background_image = 'maze.png'
        fruit.position = [(14, 20)]
        blinky.position = blinky.start
        #pinky.position = pinky.start
        #inky.position = inky.start
        #clyde.position = clyde.start
        player.image = 'pacman1.png'
        player.position = player.start
        sounds.intro.play()

    def set_play(self):
        self.state = 'play'

    def set_intermission(self):
        self.state = 'intermission'
        self.find_characters()
        self.background_image = 'intermission.png'

    def draw_load(self):
        screen.clear()
        self.draw_background()
        self.draw_one_up()
        self.draw_high_score()

    def draw_start(self):
        screen.clear()
        self.draw_background()
        self.draw_one_up()
        self.draw_high_score()
        self.draw_ready()
        small_pellet.draw()
        large_pellet.draw()
        warp_gate_1.draw()
        warp_gate_2.draw()
        player.draw_live_counter()
        player.draw_fruit_counter()
        player.draw()
        blinky.draw()
        #pinky.draw()
        #inky.draw()
        #clyde.draw()

    def draw_play(self):
        screen.clear()
        self.draw_background()
        self.draw_one_up()
        self.draw_high_score()
        small_pellet.draw()
        large_pellet.draw()
        fruit.draw()
        warp_gate_1.draw()
        warp_gate_2.draw()
        player.draw_live_counter()
        player.draw_fruit_counter()
        player.draw()
        blinky.draw()
        #pinky.draw()
        #inky.draw()
        #clyde.draw()

    def draw_intermission(self):
        screen.clear()
        self.draw_one_up()
        self.draw_high_score()
        self.draw_background()


class Player(object):

    def __init__(self):
        self.i = 0
        self.speed = 8
        self.lives = 2
        self.lives_position = (4, 34)
        self.lives_image = 'pacmanleft2.png'
        self.fruit_eaten = 0
        self.fruit_position = (23, 34)
        self.fruit_image = 'cherry.png'
        self.image = 'pacman1' 
        self.start = (14, 26)
        self.position = self.start
        self.stored_direction = ''
        self.current_direction = ''

    def draw(self):
        draw_image(self.image, (self.position[0] - 0.5, self.position[1] - 0.5))

    def draw_live_counter(self):
        i = -0.86
        for live in range (self.lives):
            i += 0.86
            draw_image(self.lives_image, (self.lives_position[0] + live + i, self.lives_position[1]))

    def draw_fruit_counter(self):
        i = -0.86
        for fruit in range (self.fruit_eaten):
            i += 0.86
            draw_image(self.fruit_image, (self.fruit_position[0] - fruit - i, self.fruit_position[1]))

    def animate(self):
        self.i += 1
        self.image = 'pacman' + self.current_direction + str(self.i)
        if self.i == 2:
            self.i = 0

    def move(self):
        if self.can_move():
            self.animate()
            self.position = new_position
            self.collide()

    def can_move(self):
        global new_position
        dx = 0
        dy = 0
        if self.current_direction == 'left':
            dx = -1
        elif self.current_direction == 'up':
            dy = -1
        elif self.current_direction == 'right':
            dx = 1
        elif self.current_direction == 'down':
            dy = 1
        new_position = (self.position[0] + dx, self.position[1] + dy)
        if new_position in game.wall_positions:
            return  False
        else:
            return True

    def set_direction(self):
        if keyboard.left:
            self.current_direction = 'left'
        elif keyboard.up:
            self.current_direction = 'up'
        elif keyboard.right:
            self.current_direction = 'right'
        elif keyboard.down:
            self.current_direction = 'down'
        if self.can_move():
            self.stored_direction = self.current_direction
        else:
            self.current_direction = self.stored_direction

    def collide(self):
        if self.position in small_pellet.positions:
            game.high_score += small_pellet.points
            game.one_up_score += small_pellet.points
            if game.one_up_score >= 10000:
                game.one_up_score = game.one_up_score % 10000
                self.lives += 1
            small_pellet.positions.remove(self.position)
            if len(small_pellet.positions) <= 0:
                game.level += 1
                game.set_intermission()

        elif self.position in large_pellet.positions:
            game.high_score += large_pellet.points
            game.one_up_score += large_pellet.points
            if game.one_up_score >= 10000:
                game.one_up_score = game.one_up_score % 10000
                self.lives += 1
            large_pellet.positions.remove(self.position)
            blinky.set_fright()
            #pinky.set_fright()
            #inky.set_fright()
            #clyde.set_fright()

        elif self.position in fruit.position:
            player.fruit_eaten += 1
            game.high_score += fruit.points
            game.one_up_score += fruit.points
            if game.one_up_score >= 10000:
                game.one_up_score = game.one_up_score % 10000
                self.lives += 1
            fruit.position.remove(self.position)

        elif self.position == warp_gate_1.position:
            self.position = (warp_gate_2.position[0] - 1, warp_gate_2.position[1])

        elif self.position == warp_gate_2.position:
            self.position = (warp_gate_1.position[0] + 1, warp_gate_1.position[1])


class smallPellet(object):

    def __init__(self):
        self.points = 10
        self.image = 'smallpellet.png'
        self.positions = []

    def draw(self):
        for pellet_position in self.positions:
            draw_image(self.image, (pellet_position[0], pellet_position[1]))


class largePellet(object):

    def __init__(self):
        self.points = 100
        self.image = 'largepellet.png'
        self.positions = []

    def draw(self):
        for pellet_position in self.positions:
            draw_image(self.image, (pellet_position[0], pellet_position[1]))


class Fruit(object):

    def __init__(self):
        self.points = 1000
        self.image = 'cherry.png'
        self.position = []
    
    def draw(self):
        try:
            draw_image(self.image, (self.position[0][0] - 0.5, self.position[0][1] - 0.5))
        except IndexError:
            pass


class warpGate(object):
    
    def __init__(self, image, position):
        self.image = image
        self.position = position

    def draw(self):
        draw_image(self.image, (self.position[0] - 0.5, self.position[1] - 0.5))


class Ghost(object):

    def __init__(self, name, behaviour, image, start, chase_target, scatter_target):
        self.i = 0
        self.name = name
        self.behaviour = behaviour
        self.image = image
        self.spawn = (14, 17)
        self.start = start
        self.position = self.start
        self.wait_target = self.position
        self.chase_target = chase_target
        self.scatter_target = scatter_target
        self.current_target = self.wait_target
        self.speed = player.speed + 0.50 * player.speed

    def draw(self):
        draw_image(self.image, (self.position[0] - 0.5, self.position[1] - 0.5))

    def check_direction(self):
        if self.set_direction() == (1, 0):
            return 'right'
        elif self.set_direction() == (-1, 0):
            return 'left'
        elif self.set_direction() == (0, 1):
            return 'down'
        elif self.set_direction() == (0, -1):
            return 'up'
        else:
            pass

    def animate(self):
        self.i += 1
        if self.i > 2:
            self.i = 2
        if self.behaviour != 'fright' and self.behaviour != 'eyes':
            self.image = self.name + self.check_direction() + str(self.i)
        elif self.behaviour == 'fright':
            self.image = 'scared' + str(self.i)
        elif self.behaviour == 'eyes':
            self.image = 'eyes' + self.check_direction()
        if self.i >= 2:
            self.i = 0

    def collide(self):
        if self.position == player.position and self.behaviour == 'chase' or self.position == player.position and self.behaviour == 'scatter':
            player.lives -= 1
            if player.lives >= 0:
                game.set_start()
            elif player.lives < 0:
                game.set_load()

        elif self.position == player.position and self.behaviour == 'fright':
            self.set_eyes()
            game.high_score += 200
            game.one_up_score += 200
            if game.one_up_score >= 10000:
                game.one_up_score = game.one_up_score % 10000
                player.lives += 1

        elif self.behaviour == 'scatter' and self.position == self.scatter_target or self.behaviour == 'fright' and self.position == self.scatter_target:
            self.set_chase()

        elif self.position == self.spawn and self.behaviour == 'eyes':
            self.set_chase()

    def move(self):
        self.direction = self.set_direction()
        try:
            self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
            self.animate()
        except TypeError:
            pass
        self.collide()

    def set_direction(self):
        next_cell = self.find_next_move()
        try:
            x = next_cell[0] - self.position[0]
            y = next_cell[1] - self.position[1]
            return (x, y)
        except TypeError:
            pass

    def find_next_move(self):
        path = self.BFS([int(self.position[0]), int(self.position[1])], [int(self.current_target[0]), int(self.current_target[1])])
        try:
            return path[1]
        except IndexError:
            pass

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(36)]
        for cell in game.wall_positions:
            if cell[0] < 28 and cell[1] < 36:
                grid[int(cell[1])][int(cell[0])] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({'Current': current, 'Next': next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step['Next'] == target:
                    target = step['Current']
                    shortest.insert(0, step['Current'])
        return shortest

    def set_scatter(self):
        self.current_target = self.scatter_target
        self.behaviour = 'scatter'

    def set_chase(self):
        self.current_target = self.chase_target
        self.image = self.name + '1'
        self.behaviour = 'chase'

    def set_fright(self):
        if self.behaviour != 'eyes':
            self.behaviour = 'fright'
            self.current_target = self.scatter_target
            self.image = 'scared1.png'

    def set_eyes(self):
        self.current_target = self.spawn
        self.image = 'scared1.png'
        self.behaviour = 'eyes'

#---------------------------------------------------------------- OBJECTS ----------------------------------------------------------------#

game = Game()
player = Player()
small_pellet = smallPellet()
large_pellet = largePellet()
fruit = Fruit()
warp_gate_1 = warpGate('warpgate1.png', (1, 17))
warp_gate_2 = warpGate('warpgate2.png', (26, 17))
blinky = Ghost('blinky', 'chase', 'blinky1.png', (14, 14), player.position, (26, 4))
#pinky = Ghost('pinky', 'wait', 'pinky1.png', (13, 17), player.position, (1, 4))
#inky = Ghost('inky', 'wait', 'inky1.png', (11, 17), player.position, (1, 32))
#clyde = Ghost('clyde', 'wait', 'clyde1.png', (15, 17), player.position, (26, 32))

#---------------------------------------------------------------- HELPER -----------------------------------------------------------------#

def draw_image(image, position):
    screen.blit(image, (position[0] * STRIDE, position[1] * STRIDE))

#----------------------------------------------------------------- MAIN ------------------------------------------------------------------#

def update():
    if game.state == 'load':
        if keyboard.space:
            game.find_characters()
            game.set_start()

    elif game.state == 'start':
        clock.schedule(game.set_play, 4.6)

    elif game.state == 'play':
        player.set_direction()
        game.frames += 1

        if game.frames % player.speed == 0:
            player.move()
            if blinky.behaviour == 'chase':
                blinky.current_target = player.position
            #if pinky.behaviour == 'chase':
                #pinky.current_target = player.position
            #if inky.behaviour == 'chase':
                #inky.current_target = player.position
            #if clyde.behaviour == 'chase':
                #clyde.current_target = player.position

        if game.frames % blinky.speed == 0:
            blinky.move()
            #pinky.move()
            #inky.move()
            #clyde.move()

        #if game.frames % 240 == 0 and pinky.behaviour == 'wait':
            #pinky.set_scatter()

        #if game.frames % 480 == 0 and inky.behaviour == 'wait':
            #inky.set_scatter()

        #if game.frames % 720 == 0 and clyde.behaviour == 'wait':
            #clyde.set_scatter()

    elif game.state == 'intermission':
        if keyboard.space:
            game.set_start()

def draw():
    if game.state == 'load':
        game.draw_load()
    elif game.state == 'start':
        game.draw_start()
    elif game.state == 'play':
        game.draw_play()
    elif game.state == 'intermission':
        game.draw_intermission()

#--------------------------------------------------------------- RUN SCRIPT --------------------------------------------------------------#

pgzrun.go()

#---------------------------------------------------------------- SOURCES ----------------------------------------------------------------#

# Python Documentation: https://docs.python.org
# Pygame Zero Documentation: https://pygame-zero.readthedocs.io/en/stable/index.html
# Image Spritesheets: https://www.spriters-resource.com/arcade/pacman/
# Sounds: "Insert website  url I do not remember"
# Breadth-First-Search: https://en.wikipedia.org/wiki/Breadth-first_search
# General Game Shell & BFS Implementation: https://www.youtube.com/playlist?list=PLryDJVmh-ww3AMl8NSjp9YygWWTOfePu7
