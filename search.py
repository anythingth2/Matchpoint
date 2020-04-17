# %%
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List
from game import ConsoleGame, count_neighbour_vector
import time
import numpy as np
from tqdm import tqdm, trange
from fractions import Fraction

# %%
DELAY = 0.25


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
                 count_node=0,
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
    
    @property
    def name(self):
        return 'DFS'

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
            painted_game.render()
            # print('not match', np.argwhere(
            #     painted_game.answer_map != painted_game.map))

        paintable_nodes = self.find_paintable_nodes(
            painted_game, self.root.x, self.root.y)
        self.childs = []
        for node in paintable_nodes:
            self.childs.append(DFS(painted_game, root=node, paths=self.paths,
                                   render_func=self.render_func, count_node=self.count_node))

        for child in self.childs:
            time.sleep(DELAY)
            search_result = child.search()
            if search_result is not None:
                return search_result
        return None

    def count_node(self, ):
        return sum([child.count_node() for child in self.childs]) + 1


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

    @property
    def name(self):
        return 'BFS'

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


class DLS:
    def __init__(self, game: ConsoleGame,
                 max_depth=None,
                 win: bool = False,
                 root: Node = None,
                 childs: List['DLS'] = None,
                 paths: List[Node] = None,

                 render_func=None):
        self.game = game
        if max_depth is None:
            self.max_depth = game.count_answer_cell
        else:
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

        self.start_time = time.time()

    @property
    def name(self):
        return 'DLS'

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
            painted_game.render()
            # print('not match', np.argwhere(
            #    painted_game.answer_map != painted_game.map))

            pass

        if maxDept <= 0:
            return False

        paintable_nodes = self.find_paintable_nodes(
            painted_game, self.root.x, self.root.y)
        self.childs = []

        for node in paintable_nodes:
            self.childs.append(DLS(painted_game, max_depth=self.max_depth,
                                   root=node, paths=self.paths, render_func=self.render_func, ))

        for child in self.childs:
            time.sleep(DELAY)
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

    def count_node(self, ):
        return sum([child.count_node() for child in self.childs]) + 1
# %%


def search_pattern(vector, counts):
    def criteria(_vector):
        return count_neighbour_vector(_vector, True) == counts
    blank_idxes = np.argwhere(~vector).squeeze(axis=1)

    patterns = []
    for idx in blank_idxes:
        painted_vector = vector.copy()
        painted_vector[idx] = True
        founded_patterns = search_pattern(painted_vector, counts)

        if founded_patterns is not None:

            patterns.extend(founded_patterns)

    if len(patterns) == 0 and criteria(vector):
        patterns.append(vector)
    return patterns


def find_patterns(vector, counts):
    patterns = search_pattern(
        vector, counts=counts)
    if len(patterns) == 0:
        return patterns, np.zeros(len(vector), dtype=np.float)
    patterns = np.unique(patterns, axis=0)
    probs = patterns.sum(
        axis=0) / len(patterns)
    return patterns, probs


def calculate_probability_table(game: ConsoleGame):
    prob_table = np.zeros(game.shape, dtype=np.float)
    horizontal_pattern_table = []
    horizontal_prob_table = []
    for vector, counts in (zip(game.map, game.row_counts)):
        patterns, probs = find_patterns(vector, counts)
        horizontal_pattern_table.append(patterns)
        horizontal_prob_table.append(probs)
    horizontal_prob_table = np.array(horizontal_prob_table)

    vertical_pattern_table = []
    vertical_prob_table = []
    for vector, counts in (zip(game.map.T, game.column_counts)):
        patterns, probs = find_patterns(vector, counts)
        vertical_pattern_table.append(patterns)
        vertical_prob_table.append(probs)
    vertical_prob_table = np.array(vertical_prob_table)
    for y in range(game.map.shape[0]):
        for x in range(game.map.shape[1]):
            prob_table[y, x] = (vertical_prob_table[x, y] *
                                horizontal_prob_table[y, x])
    return prob_table
def heuristic_o(game: ConsoleGame):
    return np.random.random(game.shape)

def plot_prob_table(prob_table):
    def float2fraction(v):
        fraction = Fraction(v).limit_denominator()
        return f'{fraction.numerator}/{fraction.denominator}'
    plt.clf()
    ax = sns.heatmap(prob_table, annot=np.vectorize(
        float2fraction)(prob_table), fmt='', cbar=False)
    # plt.show(block=False)

    plt.draw()
    plt.pause(DELAY)
    # plt.draw()
    plt.savefig('tmp_prob_fig.pdf')


class GBFS:
    def __init__(self, game: ConsoleGame,
                 root: Node = None,
                 
                 childs: List['GBFS'] = None,
                 h_func_type='h1',
                 paths: List[Node] = None,
                 render_func = None):
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
        # self.prob = self.calculate_probability(self.game)
        self.prob_table = None
        self.render_func = render_func
        
        self.h_func_type = h_func_type
    @property
    def name(self):
        return 'GBFS'

    def calculate_cell_idx(self, x, y):
        height, width = self.game.shape
        return y*height + x

    def calculate_cell_position(self, idx):
        height, width = self.game.shape
        return idx % height, idx // height

    def find_paintable_nodes(self, game, x, y) -> List[Node]:
        height, width = game.shape
        nodes = []
        # for idx in range(self.calculate_cell_idx(x, y) + 1, self.calculate_cell_idx(width-1, height-1) + 1):
        for idx in range(self.calculate_cell_idx(width-1, height-1) + 1):
            x, y = self.calculate_cell_position(idx)
            if game.is_paintable(x, y):
                nodes.append(Node(x, y))
        return nodes
    

    def calculate_probability(self, game: ConsoleGame):
        
        if self.prob_table is None:
            if self.h_func_type == 'h2':
                self.prob_table = heuristic_o(game)
            else:
                self.prob_table = calculate_probability_table(game)
            

        # plot_prob_table(prob_table)
        return self.prob_table

    def sort_by_prob(self, game: ConsoleGame, nodes: List['Node']):
        print('sorting...')
        prob_table = self.calculate_probability(game)

        def prob_scoring(node):
            return prob_table[node.y, node.x]

        def order_index_scoring(node):
            return -np.ravel_multi_index((node.y, node.x), dims=game.shape)

        sorted_nodes = sorted(nodes, key=lambda node: (
            prob_scoring(node), order_index_scoring(node)), reverse=True)
        sorted_probs = [prob_table[node.y, node.x] for node in sorted_nodes]
        print('sorted')
        return sorted_nodes, sorted_probs

    def search(self):
        _, painted_game = self.game.paint(
            self.root.x, self.root.y, inplace=False)
        self.paths.append(self.root)
        print(f'lv.{painted_game.count_painted_cell}'.center(16, '-'))
        painted_game.render()
        
        print('-'*16)
        

        paintable_nodes = self.find_paintable_nodes(
            painted_game, self.root.x, self.root.y)
        paintable_nodes, probs = self.sort_by_prob(
            painted_game, paintable_nodes)
        self.render_func(painted_game.map.copy(), self.prob_table)
        
        print('\n'.join([f'{str(node)}\t{prob}' for node,
                         prob in zip(paintable_nodes, probs)]))
        if painted_game.check_result():
            print("WIN"*10)
            return self
        else:
            # print('not match', np.argwhere(
            #     painted_game.answer_map != painted_game.map))
            pass
        self.childs = []
        for node in paintable_nodes:
            self.childs.append(GBFS(painted_game, root=node, paths=self.paths, render_func=self.render_func))

        for child in self.childs:
            time.sleep(DELAY)
            print(f'search to {str(child.root)}')
            # input('k?')
            search_result = child.search()
            if search_result is not None:
                return search_result
        return None

# %%


# game = ConsoleGame('Map/B6.txt')


# # %%
# init_x, init_y = game.answer_path[0]
# root = Node(init_x, init_y)
# gbfs = GBFS(game, root=root)
# gbfs.search()
