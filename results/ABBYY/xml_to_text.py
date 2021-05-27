import os
import json
from bs4 import BeautifulSoup
from bs4.element import PageElement

words_files = os.listdir('words')

for file in words_files:
    file_prefix = file[:-5]
    xml_files = [xml for xml in os.listdir(
        'results/ABBYY/xml') if xml.startswith(file_prefix)]
    all_text = []
    cell_count = 0
    for xml_file in xml_files:
        with open(f'results/ABBYY/xml/{xml_file}') as f:
            soup = BeautifulSoup(f, features='lxml')
            cell_count += len(soup.select(
                'page > block[blockType="Table"] > row > cell'))
            lines = soup.select(
                'page > block[blockType="Table"] > row > cell formatting')
            char: PageElement
            line: PageElement
            character_list = []
            for line in lines:
                line_text = []
                characters = line.findChildren()
                for char in characters:
                    line_text.append(
                        char.string if char.string else ' ')
                character_list.append(''.join(line_text))
            all_text.append(' '.join(' '.join(character_list).strip().split()))
    with open(f'results/ABBYY/words/{file_prefix}.json', 'w') as f:
        json.dump({'text': ' '.join(all_text), 'cellCount': cell_count}, f)
        print(f'Written to {file_prefix}.json')
