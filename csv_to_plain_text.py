import os
import pandas as pd

csv_files = os.listdir('icdar2013/csv')
csv_files = ['eu-020-fnc.csv']

for file in csv_files:
    df = pd.read_csv(f'icdar2013/csv/{file}', dtype='string', sep=';')
    all_text = []
    next_table = True
    for i, entry in df.iterrows():
        if next_table:
            next_table = False
            continue
        text_row = ' '.join(entry.str.cat(sep=' ').split())
        if text_row == '':
            next_table = True
            continue

        all_text.append(text_row)

    with open(f'words/{file[:-4]}.txt', 'w') as f:
        f.write(' '.join(all_text))
