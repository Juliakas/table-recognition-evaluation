import os
import json
from bs4 import BeautifulSoup
from bs4.element import PageElement
import cv2
import math

# file_prefix = 'us-014-3'
file_prefix = 'eu-014-2'
image = cv2.imread(f'icdar2013/filtered_images/{file_prefix}.png')

with open(f'results/ABBYY/xml/{file_prefix}.xml') as f:
    soup = BeautifulSoup(f, features='lxml')
    cells = soup.select(
        'page > block[blockType="Table"] > row > cell')
    for cell in cells:
        lines = cell.select('line')
        min_x, min_y, max_x, max_y = math.inf, math.inf, -math.inf, -math.inf
        for line in lines:
            x1, y1, x2, y2 = map(
                int, [line['l'], line['t'], line['r'], line['b']])
            min_x, min_y, max_x, max_y = min(min_x, x1), min(
                min_y, y1), max(max_x, x2), max(max_y, y2)
        if lines:
            cv2.rectangle(image, (min_x, min_y),
                          (max_x, max_y), (0, 0, 255), 2)
cv2.imshow('Image', image)
cv2.waitKey()
