# %%
import cv2
import numpy as np
# %%

img_path = 'Map/w.png'
output_path = 'Map/w6.txt'
map_resolution = np.array((6, 6)) 

img = cv2.imread(img_path)
img = cv2.resize(img, tuple(map_resolution),)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, img = cv2.threshold(img, 127, 1, cv2.THRESH_TRIANGLE)
img = img == 0

table = np.full_like(img, ' ', dtype='object',)
table[img] = 'O'
output_lines = [''.join(row) + '\n' for row in table]
output_lines[-1] = output_lines[-1][:-1]

with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)


# %%
