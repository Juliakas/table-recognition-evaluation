from bs4 import BeautifulSoup
import os
import re
from bs4.element import PageElement

xml_files = [file for file in os.listdir(
    'icdar2013/xml') if file.endswith('str.xml')]

for file in xml_files:
    pages_to_preserve = set()
    with open(f'icdar2013/xml/{file}') as f:
        xml_tree = BeautifulSoup(f, features='xml')
        table_regions: PageElement
        for table_regions in xml_tree.find_all('region'):
            pages_to_preserve.add(table_regions['page'])

    images = [img for img in os.listdir(
        'icdar2013/images') if img.startswith(file[:-7])]
    for img_file_name in images:
        search = re.search(r'(.+?-.+?)-(.+)\.png', img_file_name)
        document_name, page_number = search.groups()
        page_number = page_number.lstrip('0')
        if page_number in pages_to_preserve:
            os.system(
                f'cp icdar2013/images/{img_file_name} icdar2013/filtered_images/{img_file_name}')
