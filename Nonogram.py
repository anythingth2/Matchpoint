#%%
import pygame
import sys
import Consistant
import numpy as np
import time
from game import ConsoleGame
from search import DFS, DLS, Node
import time

class Game:

    # ฟังก์ชันสำหรับ Draw

    def drawScreen(self,screen):
        font = pygame.font.Font('arial.ttf', 50)
        text = font.render('Select Stage', True, Consistant.BLUE)
        textrect = text.get_rect()
        textrect.centerx = 400
        textrect.centery = 50
        screen.blit(text, textrect)

        b = pygame.transform.smoothscale(pygame.image.load("B.png"),(180,180))
        screen.blit(b, [10,100])

        emoji = pygame.transform.smoothscale(pygame.image.load("emoji.png"),(180,180))
        screen.blit(emoji, [210,100])

        g = pygame.transform.smoothscale(pygame.image.load("G.png"),(180,180))
        screen.blit(g, [410,100])

        k = pygame.transform.smoothscale(pygame.image.load("K.png"),(180,180))
        screen.blit(k, [610,100])

        q = pygame.transform.smoothscale(pygame.image.load("Q.png"),(180,180))
        screen.blit(q, [10,340])

        r = pygame.transform.smoothscale(pygame.image.load("R.png"),(180,180))
        screen.blit(r, [210,340])

        s = pygame.transform.smoothscale(pygame.image.load("S.png"),(180,180))
        screen.blit(s, [410,340])

    def drawButton(self, screen):
        pygame.draw.rect(screen, Consistant.GREEN, (450, 450, 100, 50))
        pygame.draw.rect(screen, Consistant.RED, (650, 450, 100, 50))
        pygame.draw.rect(screen, Consistant.GREY, (550, 525, 100, 50))

        font = pygame.font.Font('arial.ttf', 20)
        text1 = font.render('DFS', True, (255, 255, 255))
        textrect1 = text1.get_rect()
        textrect1.centerx = 500
        textrect1.centery = 475
        screen.blit(text1, textrect1)

        text2 = font.render('DLS', True, (255, 255, 255))
        textrect2 = text2.get_rect()
        textrect2.centerx = 700
        textrect2.centery = 475
        screen.blit(text2, textrect2)

        text3 = font.render('Back', True, (0, 0, 0))
        textrect3 = text3.get_rect()
        textrect3.centerx = 600
        textrect3.centery = 550
        screen.blit(text3, textrect3)

    def draw_textRow(self, screen):
        font = pygame.font.Font('arial.ttf', 20)
        text = font.render(' ', True, (0, 0, 0))
        textrect = text.get_rect()
        textrect.centery = 25
        for i, row in enumerate(self.row_counts):
            textrect.centerx = 425
            for j, num in enumerate(row):
                text = font.render(str(num), True, (0, 0, 0))
                screen.blit(text, textrect)
                textrect.centerx = textrect.centerx+50
            textrect.centery = textrect.centery+50

    def draw_textColumn(self, screen):
        font = pygame.font.Font('arial.ttf', 20)
        text = font.render(' ', True, (0, 0, 0))
        textrect = text.get_rect()
        textrect.centerx = 25
        for i, column in enumerate(self.column_counts):
            textrect.centery = 425
            for j, num in enumerate(column):
                text = font.render(str(num), True, (0, 0, 0))
                screen.blit(text, textrect)
                textrect.centery = textrect.centery + 50
            textrect.centerx = textrect.centerx + 50

    def get_tile_color(self, tile_contents):
        tile_color = Consistant.GREY
        if tile_contents == True:
            tile_color = Consistant.BLUE
        return tile_color

    def draw_map(self,  _map=None):
        screen = self.screen
        if _map is None:
            _map = self.map
        for j, tile in enumerate(_map):
            for i, tile_contents in enumerate(tile):
                myrect = pygame.Rect(i*Consistant.BLOCK_WIDTH, j*Consistant.BLOCK_HEIGHT,
                                     Consistant.BLOCK_WIDTH, Consistant.BLOCK_HEIGHT)
                pygame.draw.rect(
                    screen, self.get_tile_color(tile_contents), myrect)

    def draw_grid(self, surface):
        for i in range(Consistant.NUMBER_OF_BLOCK_WIDE+1):
            new_height = round(i * Consistant.BLOCK_HEIGHT)
            new_width = round(i * Consistant.BLOCK_WIDTH)
            pygame.draw.line(surface, Consistant.BLACK, (0, new_height),
                             (Consistant.SCREEN_WIDTH, new_height), 2)
            pygame.draw.line(surface, Consistant.BLACK, (new_width, 0),
                             (new_width, Consistant.SCREEN_HEIGHT), 2)

    # Loop หลักของเกมอยู่ในนี้
    def game_loop(self, ):
        screen = self.screen
        #self.draw_map()
        self.stage = 0
        self.bg = pygame.image.load("Nonogram.png")

        while True:
<<<<<<< Updated upstream
            # กดปุ่ม X เพื่อออกจากโปรแกรม
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Event เมื่อคลิ๊กเมาส์
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    # คลิ๊กปุ่มทางขวา(สีเขียว)
                    if(550 > mouse[0] > 450 and 500 > mouse[1] > 450):
                        def render_func(_map):
                            self.draw_map( _map)
                            self.draw_grid(screen)
                            pygame.display.update()
                        self.green_search_algorithm.render_func = render_func
                        self.green_search_algorithm.search()
                        print('Number of node:',self.green_search_algorithm.count_node())
                        print(f'Time elapsed: {time.time() -self.green_search_algorithm.start_time} s')
                        # answer_actions = np.argwhere(
                        #     self.answer_map, )[:, ::-1]

                        # for x, y in answer_actions:
                        #     result = self.paint(x, y)
                            
                            # time.sleep(0.5)
                    # คลิ๊กปุ่มซ้าย(สีแดง)
                    elif(750 > mouse[0] > 650 and 500 > mouse[1] > 450):
                        def render_func(_map):
                            self.draw_map( _map)
                            self.draw_grid(screen)
                            pygame.display.update()
                        self.red_search_algorithm.render_func = render_func
                        self.red_search_algorithm.search()
                        print('Number of node:',self.red_search_algorithm.count_node())
                        print(f'Time elapsed: {time.time() -self.red_search_algorithm.start_time} s')
                        # answer_actions = np.argwhere(
                        #     self.answer_map, )[:, ::-1]

                        # for x, y in answer_actions:
                        #     result = self.paint(x, y)
                        #     self.draw_map(screen)
                        #     self.draw_grid(screen)
                        #     pygame.display.update()
                        #     time.sleep(0.5)
                        pass

                    elif(650 > mouse[0] > 550 and 575 > mouse[1] > 525):
                        self.draw_map()

            #self.draw_map()
            self.draw_grid(screen)
            self.draw_textRow(screen)
            self.draw_textColumn(screen)
            self.drawButton(screen)
            pygame.display.update()
=======
            # คลิ๊กปุ่ม X เพื่อออกจากโปรแกรม
            if self.stage == 0:
                screen.blit(self.bg,[0,0])
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.stage = 1
            
            elif self.stage == 1 :
                screen.fill(Consistant.WHITE)
                self.drawScreen(screen)
                pygame.display.update()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse = pygame.mouse.get_pos()
                            # คลิ๊กปุ่มทางขวา(สีเขียว)
                            if(190 > mouse[0] > 10 and 280 > mouse[1] > 100):
                                self.map_path = 'Map/B.txt'
                                self.answer_map = self.read_map(self.map_path)
                                self.map = np.full_like(self.answer_map, False)
                                self.row_counts = self.count_neighbours(
                                    self.answer_map, count_value=True)
                                self.column_counts = self.count_neighbours(
                                    self.answer_map.T, count_value=True)

                                console_game = ConsoleGame(self.map_path)
                                init_x, init_y = console_game.answer_path[0]
                                root = Node(init_x, init_y)
                                dfs = DFS(console_game, root=root, )
                                dls = DLS(console_game, max_depth=console_game.count_answer_cell, root=root,)
                                self.green_search_algorithm = dfs
                                self.red_search_algorithm = dls
                                screen.fill(Consistant.WHITE)
                                self.draw_map(self.map)
                                pygame.display.update()
                                self.stage = 2

                            elif(390 > mouse[0] > 210 and 280 > mouse[1] > 100):
                                self.map_path = 'Map/emoji.txt'
                                self.answer_map = self.read_map(self.map_path)
                                self.map = np.full_like(self.answer_map, False)
                                self.row_counts = self.count_neighbours(
                                    self.answer_map, count_value=True)
                                self.column_counts = self.count_neighbours(
                                    self.answer_map.T, count_value=True)

                                console_game = ConsoleGame(self.map_path)
                                init_x, init_y = console_game.answer_path[0]
                                root = Node(init_x, init_y)
                                dfs = DFS(console_game, root=root, )
                                dls = DLS(console_game, max_depth=console_game.count_answer_cell, root=root,)
                                self.green_search_algorithm = dfs
                                self.red_search_algorithm = dls
                                screen.fill(Consistant.WHITE)
                                self.draw_map(self.map)
                                pygame.display.update()
                                self.stage = 2
                            elif(590 > mouse[0] > 410 and 280 > mouse[1] > 100):
                                self.map_path = 'Map/G.txt'
                                self.answer_map = self.read_map(self.map_path)
                                self.map = np.full_like(self.answer_map, False)
                                self.row_counts = self.count_neighbours(
                                    self.answer_map, count_value=True)
                                self.column_counts = self.count_neighbours(
                                    self.answer_map.T, count_value=True)

                                console_game = ConsoleGame(self.map_path)
                                init_x, init_y = console_game.answer_path[0]
                                root = Node(init_x, init_y)
                                dfs = DFS(console_game, root=root, )
                                dls = DLS(console_game, max_depth=console_game.count_answer_cell, root=root,)
                                self.green_search_algorithm = dfs
                                self.red_search_algorithm = dls
                                screen.fill(Consistant.WHITE)
                                self.draw_map(self.map)
                                pygame.display.update()
                                self.stage = 2
                            elif(790 > mouse[0] > 610 and 280 > mouse[1] > 100):
                                self.map_path = 'Map/K.txt'
                                self.answer_map = self.read_map(self.map_path)
                                self.map = np.full_like(self.answer_map, False)
                                self.row_counts = self.count_neighbours(
                                    self.answer_map, count_value=True)
                                self.column_counts = self.count_neighbours(
                                    self.answer_map.T, count_value=True)

                                console_game = ConsoleGame(self.map_path)
                                init_x, init_y = console_game.answer_path[0]
                                root = Node(init_x, init_y)
                                dfs = DFS(console_game, root=root, )
                                dls = DLS(console_game, max_depth=console_game.count_answer_cell, root=root,)
                                self.green_search_algorithm = dfs
                                self.red_search_algorithm = dls
                                screen.fill(Consistant.WHITE)
                                self.draw_map(self.map)
                                pygame.display.update()
                                self.stage = 2
                            elif(190 > mouse[0] > 10 and 520 > mouse[1] > 340):
                                self.map_path = 'Map/Q.txt'
                                self.answer_map = self.read_map(self.map_path)
                                self.map = np.full_like(self.answer_map, False)
                                self.row_counts = self.count_neighbours(
                                    self.answer_map, count_value=True)
                                self.column_counts = self.count_neighbours(
                                    self.answer_map.T, count_value=True)

                                console_game = ConsoleGame(self.map_path)
                                init_x, init_y = console_game.answer_path[0]
                                root = Node(init_x, init_y)
                                dfs = DFS(console_game, root=root, )
                                dls = DLS(console_game, max_depth=console_game.count_answer_cell, root=root,)
                                self.green_search_algorithm = dfs
                                self.red_search_algorithm = dls
                                screen.fill(Consistant.WHITE)
                                self.draw_map(self.map)
                                pygame.display.update()
                                self.stage = 2
                            elif(390 > mouse[0] > 210 and 520 > mouse[1] > 340):
                                self.map_path = 'Map/R.txt'
                                self.answer_map = self.read_map(self.map_path)
                                self.map = np.full_like(self.answer_map, False)
                                self.row_counts = self.count_neighbours(
                                    self.answer_map, count_value=True)
                                self.column_counts = self.count_neighbours(
                                    self.answer_map.T, count_value=True)

                                console_game = ConsoleGame(self.map_path)
                                init_x, init_y = console_game.answer_path[0]
                                root = Node(init_x, init_y)
                                dfs = DFS(console_game, root=root, )
                                dls = DLS(console_game, max_depth=console_game.count_answer_cell, root=root,)
                                self.green_search_algorithm = dfs
                                self.red_search_algorithm = dls
                                screen.fill(Consistant.WHITE)
                                self.draw_map(self.map)
                                pygame.display.update()
                                self.stage = 2
                            elif(590 > mouse[0] > 410 and 520 > mouse[1] > 340):
                                self.map_path = 'Map/S.txt'
                                self.answer_map = self.read_map(self.map_path)
                                self.map = np.full_like(self.answer_map, False)
                                self.row_counts = self.count_neighbours(
                                    self.answer_map, count_value=True)
                                self.column_counts = self.count_neighbours(
                                    self.answer_map.T, count_value=True)

                                console_game = ConsoleGame(self.map_path)
                                init_x, init_y = console_game.answer_path[0]
                                root = Node(init_x, init_y)
                                dfs = DFS(console_game, root=root, )
                                dls = DLS(console_game, max_depth=console_game.count_answer_cell, root=root,)
                                self.green_search_algorithm = dfs
                                self.red_search_algorithm = dls
                                screen.fill(Consistant.WHITE)
                                self.draw_map(self.map)
                                pygame.display.update()
                                self.stage = 2

            elif self.stage == 2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    # Event เมื่อคลิ๊กเมาส์
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        # คลิ๊กปุ่มทางขวา(สีเขียว)
                        if(550 > mouse[0] > 450 and 500 > mouse[1] > 450):
                            def render_func(_map):
                                self.draw_map( _map)
                                self.draw_grid(screen)
                                pygame.display.update()
                            self.green_search_algorithm.render_func = render_func
                            self.green_search_algorithm.search()
                        # คลิ๊กปุ่มซ้าย(สีแดง)
                        elif(750 > mouse[0] > 650 and 500 > mouse[1] > 450):
                            def render_func(_map):
                                self.draw_map( _map)
                                self.draw_grid(screen)
                                pygame.display.update()
                            self.red_search_algorithm.render_func = render_func
                            self.red_search_algorithm.search()

                        #คลิ๊กปุ่ม Clear
                        elif(650 > mouse[0] > 550 and 575 > mouse[1] > 525):
                            #self.draw_map()
                            self.stage = 1

                #screen.fill(Consistant.WHITE)
                self.draw_grid(screen)
                self.draw_textRow(screen)
                self.draw_textColumn(screen)
                self.drawButton(screen)
                pygame.display.update()
>>>>>>> Stashed changes

    # Set Up ฉากหลังของ GAME
    def initialize_game(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (Consistant.SCREEN_WIDTH, Consistant.SCREEN_HEIGHT))
        pygame.display.set_caption(Consistant.TITLE)
        screen.fill(Consistant.WHITE)
        return screen

    # เมื่อเรียกใช้ Class Game
    def __init__(self, map_path=None, green_search_algorithm=None, red_search_algorithm=None):

        #self.map_path = map_path
        #self.answer_map = self.read_map(self.map_path)
        #self.map = np.full_like(self.answer_map, False)
        #self.row_counts = self.count_neighbours(
            #self.answer_map, count_value=True)
        #self.column_counts = self.count_neighbours(
            #self.answer_map.T, count_value=True)

        self.screen = self.initialize_game()
        
        #self.green_search_algorithm = green_search_algorithm
        #self.red_search_algorithm = red_search_algorithm
        self.time = 0

    # อ่าน MAP
    def read_map(self, map_path):
        with open(map_path, 'r') as f:
            lines = f.read().splitlines()
        map_matrix = np.array([list(line) for line in lines], dtype='object')
        map_matrix = map_matrix == 'O'
        return map_matrix

    def count_neighbour_vector(self, vector, count_value, is_output_str=False):
        vector = list(vector)
        neighbour_counts = []
        count = 0
        for v in vector:
            if v == count_value:
                count += 1
            else:
                if count > 0:
                    neighbour_counts.append(count)
                    count = 0
        if count > 0:
            neighbour_counts.append(count)
        if is_output_str:
            neighbour_counts = [str(count) for count in neighbour_counts]
        return neighbour_counts

    def count_neighbours(self, _map, **kwargs):
        return [self.count_neighbour_vector(vector, **kwargs) for vector in _map]

    # Logic ของ Game

    def check_rule(self, input_neighbours, label_neighbours):
        if len(input_neighbours) > len(label_neighbours):
            return False

        for i in range(len(input_neighbours)):
            if input_neighbours[i] > label_neighbours[i]:
                return False
        return True

    def paint(self, x, y):
        _map = self.map.copy()
        _map[y, x] = True
        input_row_neighbours = self.count_neighbour_vector(
            _map[y], count_value=True)
        input_column_neighbours = self.count_neighbour_vector(
            _map[:, x], count_value=True)
        if self.check_rule(input_row_neighbours, self.row_counts[y])\
                and self.check_rule(input_column_neighbours, self.column_counts[x]):
            self.map[y, x] = True
            return True
        else:
            return False

    def erase(self, x, y):
        self.map[y, x] = False

    def clear(self):
        self.map = np.full_like(self.answer_map, False)

    def check_result(self):
        return np.all(self.answer_map == self.map)


# %%

#%%
<<<<<<< Updated upstream
map_path = 'Map/R.txt'
console_game = ConsoleGame(map_path)
init_x, init_y = console_game.answer_path[0]
root = Node(init_x, init_y)
dfs = DFS(console_game, root=root, )
dls = DLS(console_game, max_depth=console_game.count_answer_cell, root=root,)
=======
#map_path = 'Map/B.txt'
#console_game = ConsoleGame(map_path)
#init_x, init_y = console_game.answer_path[0]
#root = Node(init_x, init_y)
#dfs = DFS(console_game, root=root, )
#dls = DLS(console_game, max_depth=console_game.count_answer_cell, root=root,)
>>>>>>> Stashed changes
#%%

#game = Game(map_path, green_search_algorithm=dfs, red_search_algorithm=dls)

#game = Game(green_search_algorithm=dfs, red_search_algorithm=dls)
game = Game()
# %%
game.initialize_game()
game.game_loop()