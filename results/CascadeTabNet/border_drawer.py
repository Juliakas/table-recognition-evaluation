from bs4 import BeautifulSoup
from bs4.element import PageElement
import cv2
import numpy as np

file_prefix = 'us-010-2'
# file_prefix = 'us-016-2'


with open(f'results/CascadeTabNet/xml2/{file_prefix}.xml') as f:
    soup = BeautifulSoup(f.read(), features='lxml')

image = cv2.imread(f'icdar2013/filtered_images/{file_prefix}.png')

all_cell_coords = soup.select('table > Coords')

coord: PageElement
for coord in all_cell_coords:
    (x1, y1), _, (x3, y3), _ = [map(int, c.split(','))
                                for c in coord['points'].split()]
    cv2.rectangle(image, (x1, y1), (x3, y3),
                  color=(0, 0, 255), thickness=2)

winname = "image"
cv2.namedWindow(winname)        # Create a named window
cv2.moveWindow(winname, 40, 30)  # Move it to (40,30)
cv2.imshow('image', image)
cv2.waitKey()
