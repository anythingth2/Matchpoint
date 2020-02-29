import pygame
import sys
import Consistant
import numpy as np
import time

class Game:

#ฟังก์ชันสำหรับ Draw 

    def drawButton(self,screen):
        pygame.draw.rect(screen,Consistant.GREEN,(450,450,100,50))
        pygame.draw.rect(screen,Consistant.RED,(650,450,100,50))
        pygame.draw.rect(screen,Consistant.GREY,(550,525,100,50))
    
        font = pygame.font.Font('arial.ttf',20)
        text1 = font.render('Answer1',True,(255,255,255))
        textrect1 = text1.get_rect()
        textrect1.centerx = 500
        textrect1.centery = 475
        screen.blit(text1,textrect1)

        text2 = font.render('Answer2',True,(255,255,255))
        textrect2 = text2.get_rect()
        textrect2.centerx = 700
        textrect2.centery = 475
        screen.blit(text2,textrect2)

        text3 = font.render('Clear',True,(0,0,0))
        textrect3 = text3.get_rect()
        textrect3.centerx = 600
        textrect3.centery = 550
        screen.blit(text3,textrect3)

    def draw_textRow(self,screen):
        font = pygame.font.Font('arial.ttf',20)
        text = font.render(' ',True,(0,0,0))
        textrect = text.get_rect()
        textrect.centery = 25
        for i, row in enumerate(self.row_counts):
            textrect.centerx = 425
            for j, num in enumerate(row):
                text = font.render(str(num),True,(0,0,0))
                screen.blit(text,textrect)
                textrect.centerx = textrect.centerx+50
            textrect.centery = textrect.centery+50

    def draw_textColumn(self,screen):
        font = pygame.font.Font('arial.ttf',20)
        text = font.render(' ',True,(0,0,0))
        textrect = text.get_rect()
        textrect.centerx = 25
        for i, column in enumerate(self.column_counts):
            textrect.centery = 425
            for j, num in enumerate(column):
                text = font.render(str(num),True,(0,0,0))
                screen.blit(text,textrect)
                textrect.centery = textrect.centery + 50
            textrect.centerx = textrect.centerx + 50

    def get_tile_color(self,tile_contents):
        tile_color = Consistant.GREY
        if tile_contents == True:
            tile_color = Consistant.BLUE
        return tile_color

    def draw_map(self,screen):
        for j, tile in enumerate(self.map):
            for i, tile_contents in enumerate(tile):
                myrect = pygame.Rect(i*Consistant.BLOCK_WIDTH,j*Consistant.BLOCK_HEIGHT,Consistant.BLOCK_WIDTH,Consistant.BLOCK_HEIGHT)
                pygame.draw.rect(screen,self.get_tile_color(tile_contents),myrect)

    def draw_grid(self,surface):
        for i in range(Consistant.NUMBER_OF_BLOCK_WIDE+1):
            new_height = round(i * Consistant.BLOCK_HEIGHT)
            new_width = round(i * Consistant.BLOCK_WIDTH)
            pygame.draw.line(surface,Consistant.BLACK, (0,new_height), (Consistant.SCREEN_WIDTH,new_height),2)
            pygame.draw.line(surface,Consistant.BLACK,(new_width,0), (new_width,Consistant.SCREEN_HEIGHT),2)      

    ### Loop หลักของเกมอยู่ในนี้
    def game_loop(self,screen):

        while True:
            #กดปุ่ม X เพื่อออกจากโปรแกรม
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #Event เมื่อคลิ๊กเมาส์
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    #คลิ๊กปุ่มทางขวา(สีเขียว)
                    if(550 > mouse[0] > 450 and 500 > mouse[1] > 450):
                        answer_actions = np.argwhere(self.answer_map, )[:, ::-1]

                        for x,y in answer_actions:
                            result = self.paint(x, y)
                            self.draw_map(screen)
                            self.draw_grid(screen)
                            pygame.display.update()
                            time.sleep(0.5)
                    #คลิ๊กปุ่มซ้าย(สีแดง)
                    elif(750 > mouse[0] > 650 and 500 > mouse[1] > 450):
                        answer_actions = np.argwhere(self.answer_map, )[:, ::-1]

                        for x,y in answer_actions:
                            result = self.paint(x, y)
                            self.draw_map(screen)
                            self.draw_grid(screen)
                            pygame.display.update()
                            time.sleep(0.5)

                    elif(650 > mouse[0] > 550 and 575 > mouse[1] > 525):
                        self.clear()

            self.draw_map(screen)
            self.draw_grid(screen)
            self.draw_textRow(screen)
            self.draw_textColumn(screen)
            self.drawButton(screen)
            pygame.display.update()

    #Set Up ฉากหลังของ GAME
    def initialize_game(self):
        pygame.init()
        screen = pygame.display.set_mode((Consistant.SCREEN_WIDTH,Consistant.SCREEN_HEIGHT))
        pygame.display.set_caption(Consistant.TITLE)
        screen.fill(Consistant.WHITE)
        return screen

    #เมื่อเรียกใช้ Class Game
    def __init__(self , map_path):

        self.map_path = map_path
        self.answer_map = self.read_map(self.map_path)
        self.map = np.full_like(self.answer_map, False)
        self.row_counts = self.count_neighbours(
            self.answer_map, count_value=True)
        self.column_counts = self.count_neighbours(
            self.answer_map.T, count_value=True)

        screen = self.initialize_game()
        
        #เรียกใช้ Game Loop
        self.game_loop(screen)

    #อ่าน MAP
    def read_map(self , map_path):
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

    #Logic ของ Game

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
        