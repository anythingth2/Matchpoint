# %%
from typing import List
from game import ConsoleGame
import time
import numpy as np
# %%


class Node:
    def __init__(self, x, y, ):
        self.x = x
        self.y = y

    def __str__(self):
        return f'Node(x={self.x}, y={self.y})'


class DFS:
    def __init__(self, game: ConsoleGame,
                 root: Node = None,
                 childs: List['DFS'] = None,
                 paths: List[Node] = None):
        self.game = game
        self.root = root
        if childs:
            self.childs = childs
        else:
            self.childs = []
        if paths:
            self.paths = paths.copy()
        else:
            self.paths = []

    def calculate_cell_idx(self, x, y):
        height, width = self.game.shape
        return y*height + x

    def calculate_cell_position(self, idx):
        height, width = self.game.shape
        return idx % height, idx // height

    def find_paintable_nodes(self, game, x, y) -> List[Node]:
        height, width = game.shape
        nodes = []
        for idx in range(self.calculate_cell_idx(x, y) + 1, self.calculate_cell_idx(width-1, height-1) + 1):
            x, y = self.calculate_cell_position(idx)
            if game.is_paintable(x, y):
                nodes.append(Node(x, y))
        return nodes

    def search(self):
        _, painted_game = self.game.paint(
            self.root.x, self.root.y, inplace=False)
        self.paths.append(self.root)
        print(f'lv.{painted_game.count_painted_cell}'.center(16, '-'))
        painted_game.render()
        print('-'*16)
        if painted_game.check_result():
            print("WIN"*10)
            return self
        else:
            print('not match', np.argwhere(
                painted_game.answer_map != painted_game.map))
            pass

        paintable_nodes = self.find_paintable_nodes(
            painted_game, self.root.x, self.root.y)
        self.childs = []
        for node in paintable_nodes:
            self.childs.append(DFS(painted_game, root=node, paths=self.paths))

        for child in self.childs:
            # time.sleep(0.25)
            search_result = child.search()
            if search_result is not None:
                return search_result
        return None

# %%


class BFS:
    def __init__(self, game: ConsoleGame,
                 node: Node = None,
                 descendants: List['BFS'] = None,
                 paths: List[Node] = None,

                 ):
        self.game = game
        self.node = node
        self.level = 0

        if paths:
            self.paths = paths.copy()
        else:
            self.paths = [self.node]
        if descendants:
            self.descendants = descendants
        else:
            self.descendants = [self]

    def calculate_cell_idx(self, x, y):
        height, width = self.game.shape
        return y*height + x

    def calculate_cell_position(self, idx):
        height, width = self.game.shape
        return idx % height, idx // height

    def find_paintable_nodes(self, game, x, y) -> List[Node]:
        height, width = game.shape
        nodes = []
        for idx in range(self.calculate_cell_idx(x, y) + 1, self.calculate_cell_idx(width-1, height-1) + 1):
            x, y = self.calculate_cell_position(idx)
            if game.is_paintable(x, y):
                nodes.append(Node(x, y))
        return nodes

    def search(self):
        winners = []
        new_descendants = []
        for descendant in self.descendants:
            _, painted_game = descendant.game.paint(
                descendant.node.x, descendant.node.y, inplace=False)
            # print(f'lv.{painted_game.count_painted_cell}'.center(16, '-'))
            # painted_game.render()
            # print('-'*16)
            if painted_game.check_result():
                winners.append(descendant)
            for node in self.find_paintable_nodes(
                    painted_game, descendant.node.x, descendant.node.y):
                new_descendants.append(
                    BFS(painted_game, node, paths=descendant.paths+[node]))
        self.descendants = new_descendants
        self.level += 1
        return winners
# %%


class DLS:
    def __init__(self, game: ConsoleGame,
                 win: bool = False,
                 root: Node = None,
                 childs: List['DLS'] = None,
                 paths: List[Node] = None):
        self.game = game
        self.win = win
        self.root = root
        if childs:
            self.childs = childs
        else:
            self.childs = []
        if paths:
            self.paths = paths.copy()
        else:
            self.paths = []

    def calculate_cell_idx(self, x, y):
        height, width = self.game.shape
        return y*height + x

    def calculate_cell_position(self, idx):
        height, width = self.game.shape
        return idx % height, idx // height

    def find_paintable_nodes(self, game, x, y) -> List[Node]:
        height, width = game.shape
        nodes = []
        for idx in range(self.calculate_cell_idx(x, y) + 1, self.calculate_cell_idx(width-1, height-1) + 1):
            x, y = self.calculate_cell_position(idx)
            if game.is_paintable(x, y):
                nodes.append(Node(x, y))
        return nodes

    def search(self, maxDept):
        _, painted_game = self.game.paint(
            self.root.x, self.root.y, inplace=False)

        self.paths.append(self.root)

        print(f'lv.{painted_game.count_painted_cell}'.center(16, '-'))
        painted_game.render()
        print('-'*16)

        if painted_game.check_result():
            print("WIN"*10)
            self.win = True
            return self
        else:
            # print('not match', np.argwhere(
            #    painted_game.answer_map != painted_game.map))
            pass

        if maxDept <= 0:
            return False

        paintable_nodes = self.find_paintable_nodes(
            painted_game, self.root.x, self.root.y)
        self.childs = []

        for node in paintable_nodes:
            self.childs.append(DLS(painted_game, root=node, paths=self.paths))

        for child in self.childs:
            # time.sleep(1)
            search_result = child.search(maxDept-1)
            if search_result is not None:
                return search_result
        return None

    def isearch(self, maxDept):
        for i in range(maxDept):
            print("max ", i)
            winner = self.search(i)
            if self.win:
                return winner

# %%


game = ConsoleGame('Map/b.txt')
# init_x, init_y = -1, 0
init_x, init_y = game.answer_path[0]


# %%
