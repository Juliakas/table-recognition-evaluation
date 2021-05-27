import os
import pandas as pd
import json

text_files = os.listdir('words')
ocr_engine = 'vision_ai'
method = '2'

for file in text_files:
    with open(f'words/{file}') as f:
        text = f.read()

    words = text.split()
    file_prefix = file[:-5]
    csv_files = [csv for csv in os.listdir(
        f'results/TableNET/{ocr_engine}/csv{method}') if csv.startswith(file_prefix)]
    text_to_write = []
    cell_count = 0
    for csv in csv_files:
        text_lines = []
        try:
            df = pd.read_csv(
                f'results/TableNET/{ocr_engine}/csv{method}/{csv}', dtype='string')
        except(pd.errors.EmptyDataError):
            df = pd.DataFrame([])
        cell_count += int(df.count().sum())
        for i, entry in df.iterrows():
            text_row = ' '.join(entry.str.cat(sep=' ').split())
            text_lines.append(text_row)

        text_to_write.append(' '.join(text_lines))
    with open(f'results/TableNET/{ocr_engine}/words{method}/{file_prefix}.json', 'w') as f:
        json.dump({'text': ' '.join(' '.join(text_to_write).split()),
                   'cellCount': cell_count}, f)
