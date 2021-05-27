from bs4 import BeautifulSoup
import os
import re
import json
from bs4.element import PageElement

xml_files = [file for file in os.listdir(
    'icdar2013/xml') if file.endswith('str.xml')]

for file in xml_files:
    search = re.search(r'(.+?-.+?)-(.+)\.xml', file)
    document_name, page_number = search.groups()
    extracted_text = []
    cell_count = 0
    with open(f'icdar2013/xml/{file}') as f:
        xml_tree = BeautifulSoup(f, features='xml')
        cell_contents = xml_tree.select('table > region > cell > content')
        cell_count += len(cell_contents)
        content: PageElement
        for content in cell_contents:
            extracted_text.append(' '.join(content.string.strip().split()))
    with open(f'words/{document_name}.json', 'w') as f:
        json.dump({'text': ' '.join(extracted_text),
                   'cellCount': cell_count}, f)
