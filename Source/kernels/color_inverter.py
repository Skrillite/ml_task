from cv2 import *
from numpy import *

imgs = input().split() 

for path in imgs:
    img = imread(path, IMREAD_GRAYSCALE)
    for w in range(img.shape[0]):
        for h in range(img.shape[1]):
            img[w][h] = 255 - img[w][h]

    imwrite(path, img)
    print(f"img {path} is done!")