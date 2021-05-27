from PIL import Image
from bs4 import BeautifulSoup
from bs4.element import PageElement
import cv2
import os
import numpy as np
from pytesseract import image_to_string
import re
from google.cloud import vision
import json

ocr_engine = 'vision_ai'
actual_word_files = os.listdir('words/')
for file in actual_word_files:
    file_prefix = file[:-5]
    all_document_text = []
    cell_count = 0
    xml_files = [xml for xml in os.listdir(
        'results/CascadeTabNet/xml/') if xml.startswith(file_prefix)]
    for xml_file in xml_files:
        with open(f'results/CascadeTabNet/xml/{xml_file}') as f:
            table_img = cv2.imread(
                f'icdar2013/filtered_images/{xml_file[:-4]}.png')
            text_contents = []
            soup = BeautifulSoup(f, features='xml')
            cell_coords = soup.select('table > cell > Coords')
            cell_count += len(cell_coords)
            coord: PageElement
            for coord in cell_coords:
                (x1, y1), (x2, y2), (x3, y3), (x4, y4) = [
                    map(int, p.split(',')) for p in coord['points'].split()]
                # cv2.rectangle(table_img, (x1, y1), (x3, y3),
                #               color=(255, 0, 0), thickness=1)
                cropped = table_img[y1:y3, x1:x3].astype(np.uint8)
                if ocr_engine == 'tesseract':
                    text = ' '.join(image_to_string(
                        Image.fromarray(cropped)).split())
                elif ocr_engine == 'vision_ai':
                    client = vision.ImageAnnotatorClient()
                    image = vision.Image(content=cv2.imencode(
                        '.jpg', cropped)[1].tobytes())
                    response = client.text_detection(image=image)
                    texts = response.text_annotations
                    all_vision_ai_text = []
                    for text in texts:
                        all_vision_ai_text.append(text.description.strip())
                    text = ' '.join(all_vision_ai_text)
                else:
                    exit(1)
                # cv2.imshow('cell', cropped)
                # print(image_to_string(Image.fromarray(cropped)))
                # cv2.waitKey()
                if not text.isspace():
                    text_contents.append(text)

            # cv2.imshow('col', table_img)
            # cv2.waitKey()
        all_document_text.append(' '.join(text_contents))
    with open(f'results/CascadeTabNet/{ocr_engine}/words/{file_prefix}.json', 'w') as fw:
        json.dump({'text': re.sub(
            r'\s+', ' ', ' '.join(all_document_text)), 'cellCount': cell_count}, fw)
        print(f'written to {file_prefix}.json')
