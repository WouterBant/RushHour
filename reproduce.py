import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np


"""
To get results.csv just run the algorithms as described in README.md. This will automatically generate
output.csv with the moves and with python visualize.py a visualization will be visible.
"""

"""
To create board.csv in random_vs_compressed, do the following and run python main.py 1 board_number:
Where board_number is the board for which you want to retrieve the results.
"""
### In main.py replace:
# elif algorithm == 1:
#         algo = shortRandom.ShortenedPathRandom(startBoard, batch_size=3, number_batches=8, display=display)
#         algorithm_name = "Shortened Path Random"
#         path = algo.run()
### With:
# elif algorithm == 1:
#   algorithm_name = "Shortened Path Random"
#   with open("board.csv", "w", newline="") as move_file:
#   writer = csv.writer(move_file, delimiter=",")
#   writer.writerow(['Normal Random', 'Path Compressed Random'])
#   for _ in range(100):
#         algo = shortRandom.ShortenedPathRandom(startBoard, batch_size=1, number_batches=1, display=display)
#         pathLenRandom, pathLenCompressed = algo.run()
#         move_writer.writerow([pathLenRandom, pathLenCompressed])
### And in rushhourcode/algorithms/shortened_path_random.py replace:
# return self.runBF()
### With:
# return (len(path), len(self.runBF()))


"""To create overview.csv in random_vs_compressed, uncomment the following and run python reproduce.py:"""
# results = []
# for board in range(1, 8):
#     df = pd.read_csv(f'results/random_vs_compressed/board{board}.csv')
#     first_column_mean = df.iloc[:, 0].mean()
#     second_column_mean = df.iloc[:, 1].mean()
#     results.append([first_column_mean, second_column_mean, first_column_mean - second_column_mean])
# results = pd.DataFrame(results, columns=['Random', 'Path Compressed', 'Difference'])
# results.to_csv('overview.csv', index=False)


"""To create results.csv in distribution_random, uncomment the following and run python reproduce.py:"""
# results = []
# for board in range(1, 8):
#     df = pd.read_csv(f'results/random_vs_compressed/board{board}.csv')
#     first_column_mean = df.iloc[:, 0].mean()
#     first_column_std = df.iloc[:, 0].std()
#     first_column_min = df.iloc[:, 0].min()
#     first_column_max = df.iloc[:, 0].max()
#     results.append([first_column_mean, first_column_std, first_column_min, first_column_max])
# results = pd.DataFrame(results, columns=['mean', 'standard deviation', 'minimum', 'maximum'])
# results.to_csv('results.csv', index=False)


"""To create board.png's in distribution_random/histograms, uncomment the following and run python reproduce.py:"""
# for board in range(1, 8):
#     df = pd.read_csv(f'results/random_vs_compressed/board{board}.csv')
#     plt.hist(df.iloc[:, 0])
#     plt.xlabel('Number of steps')
#     plt.ylabel('Frequency')
#     plt.title(f'Distribution 100 random runs, board {board}')
#     plt.savefig(f'board{board}.png')
#     plt.clf()
