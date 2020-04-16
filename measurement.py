# %%
from game import ConsoleGame
from search import DFS, DLS, GBFS, Node
import pandas as pd
import tracemalloc
import time
# %%
tracemalloc.start()

current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

# %%
search_algorithms = [GBFS, DFS, DLS, ]
output_path = 'measurement_w6_dls.csv'
n_episode = 10
map_paths = ['Map/w6.txt', ]

measurements = []
for search_algorithm in search_algorithms:
    for map_path in map_paths:
        for ep in range(n_episode):

            game = ConsoleGame(map_path, )

            init_x, init_y = game.answer_path[0]
            root = Node(init_x, init_y)

            start_time = time.time()
            tracemalloc.start()
            _, start_peak = tracemalloc.get_traced_memory()

            search = search_algorithm(game, root=root,)
            search.search()

            end_time = time.time()
            _, end_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            measurement = {
                'episode': ep,
                'map': map_path,
                'algorithm': search.name,
                'peak_memory_usage(KB)': (end_peak - start_peak)/10**3,
                'time_usage(S)': end_time - start_time
            }
            measurements.append(measurement)
            print(measurement)
            measurement_df = pd.DataFrame(measurements)
            measurement_df.to_csv(output_path)
measurement_df = pd.DataFrame(measurements)
measurement_df.to_csv(output_path)
# %%
