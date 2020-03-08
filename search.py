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
                 paths: List[Node] = None,
                 count_node= 0,
                 render_func=None):
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
        self.render_func = render_func
        self.start_time = time.time()
        

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
        if self.render_func is None:
            painted_game.render()
        else:
            self.render_func(painted_game.map.copy())
        print('-'*16)
        if painted_game.check_result():
            print("WIN"*10)
            return self
        else:
            print('not match', np.argwhere(
                painted_game.answer_map != painted_game.map))

        paintable_nodes = self.find_paintable_nodes(
            painted_game, self.root.x, self.root.y)
        self.childs = []
        for node in paintable_nodes:
            self.childs.append(DFS(painted_game, root=node, paths=self.paths, render_func=self.render_func, count_node=self.count_node))

        for child in self.childs:
            time.sleep(0.25)
            search_result = child.search()
            if search_result is not None:
                return search_result
        return None
    def count_node(self, ):
        return sum([child.count_node() for child in self.childs]) + 1

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
                max_depth,
                 win: bool = False,
                 root: Node = None,
                 childs: List['DLS'] = None,
                 paths: List[Node] = None,
                 
                 render_func=None):
        self.game = game
        self.max_depth = max_depth
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
        
        self.render_func = render_func
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

    def _search(self, maxDept):
        _, painted_game = self.game.paint(
            self.root.x, self.root.y, inplace=False)

        self.paths.append(self.root)

        print(f'lv.{painted_game.count_painted_cell}'.center(16, '-'))
        if self.render_func is None:
            painted_game.render()
        else:
            self.render_func(painted_game.map.copy())
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
            self.childs.append(DLS(painted_game, max_depth=self.max_depth, root=node, paths=self.paths, render_func=self.render_func, ))

        for child in self.childs:
            time.sleep(0.25)
            search_result = child._search(maxDept-1)
            if search_result is not None:
                return search_result
        return None

    def search(self, ):
        for i in range(self.max_depth):
            print("max ", i)
            winner = self._search(i)
            if self.win:
                return winner

# %%


# game = ConsoleGame('Map/Q.txt')
# # init_x, init_y = -1, 0
# init_x, init_y = game.answer_path[0]

# root = Node(init_x, init_y)
# # %%
# search = DLS(game, root=root)
# search.isearch(game.count_answer_cell)

# %%
