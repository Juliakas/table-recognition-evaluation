from google.cloud import vision
from google.cloud.vision import AnnotateImageResponse
import os
import cv2
import numpy as np
from bs4 import BeautifulSoup
import re
import json
from pytesseract import image_to_string

ocr_engine = 'vision_ai'


def detect_text(img_np):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=cv2.imencode('.jpg', img_np)[1].tostring())
    response = client.text_detection(image=image)
    with open('./response.json', 'w') as f:
        f.write(AnnotateImageResponse.to_json(response))

    if (len(response.full_text_annotation.pages) > 1):
        raise Exception('Pages > 1')
    elif (len(response.full_text_annotation.pages) == 0):
        return []
    blocks = response.full_text_annotation.pages[0].blocks
    text_in_cells = []

    for block in blocks:
        if len(block.paragraphs) > 1:
            raise Exception('Paragraphs > 1')
        words = []
        for word in block.paragraphs[0].words:
            words.append(''.join(symbol.text for symbol in word.symbols))
        text_in_cells.append(' '.join(words))

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: '
                        'https://cloud.google.com/apis/design/errors'.format(
                            response.error.message))
    # print(text_in_cells)
    # cv2.waitKey()
    return re.sub(r'\s+', ' ', ' '.join(text_in_cells))


word_files = os.listdir('words/')
for file in word_files:
    document_name = file[:-5]
    images = [img for img in os.listdir(
        'icdar2013/filtered_images/') if img.startswith(document_name)]
    cell_count = 0
    document_texts = []
    for img in images:
        image_name = img[:-4]
        page_image = cv2.imread(f'icdar2013/filtered_images/{img}')
        with open(f'results/CascadeTabNet/xml2/{image_name}.xml') as xml_file:
            soup = BeautifulSoup(xml_file.read(), features='lxml')
        tables_coords = soup.select('table > Coords')
        table_contents = []
        for coords_tag in tables_coords:
            (x1, y1), _, (x3, y3), _ = [map(int, coord.split(','))
                                        for coord in coords_tag['points'].split()]
            table_img = page_image[y1:y3, x1:x3]
            # cv2.imshow('Table', table_img)
            # cv2.waitKey()
            if ocr_engine == 'vision_ai':
                text = detect_text(table_img)
                # image = vision.Image(content=cv2.imencode(
                #     '.jpg', table_img.astype(np.uint8))[1].tobytes())
                # client = vision.ImageAnnotatorClient()
                # response = client.document_text_detection(image=image)
                # paragraphs = [
                #     par for block in response.full_text_annotation.pages[0].blocks for par in block.paragraphs]
                # cell_count += 0
                # text = re.sub(r'\s+', ' ', response.full_text_annotation.text)
            elif ocr_engine == 'tesseract':
                text = image_to_string(table_img.astype(np.uint8))
                cell_count += len(text.split('\n'))
            else:
                exit(1)
            table_contents.append(text)
        document_texts.append(' '.join(table_contents))
    with open(f'results/CascadeTabNet/{ocr_engine}/words2/{document_name}.json', 'w') as f:
        json.dump({'text': ' '.join(document_texts),
                   'cellCount': cell_count}, f)
        print(f'written to {document_name}.json')

# for text in paragraphs:
#     v1, v2, v3, v4 = text.bounding_box.vertices
#     pts = np.array([[v1.x, v1.y], [v2.x, v2.y], [
#                    v3.x, v3.y], [v4.x, v4.y]], np.int32)
#     pts = pts.reshape((-1, 1, 2))
#     cv2.polylines(cv_img, [pts], True, color=(255, 0, 0))

# winname = "Detected text"
# cv2.namedWindow(winname)        # Create a named window
# cv2.moveWindow(winname, 40, 30)  # Move it to (40,30)
# cv2.imshow(winname, cv_img)
# cv2.waitKey()


# detect_text('data/Marmot_data/10.1.1.1.2013_64.bmp')
