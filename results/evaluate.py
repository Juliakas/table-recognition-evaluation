import pandas as pd
import os
import re
from collections import Counter
import json

words = '2'
table_engine = 'CascadeTabNet'
ocr_engine = 'vision_ai'
eval_type = 'words'

files = os.listdir(f'results/{table_engine}/{ocr_engine}/words')
df_rows = []

for file in files:
    with open(f'results/{table_engine}/{ocr_engine}/words{words}/{file}') as f:
        predicted_json = json.load(f)
        predicted_text = str.lower(predicted_json['text'])
        predicted_cell_count = predicted_json['cellCount']
    with open(f'words/{file}') as f:
        actual_json = json.load(f)
        actual_text = str.lower(actual_json['text'])
        actual_cell_count = actual_json['cellCount']
    if eval_type == 'words':
        tokens = predicted_text.split()
        actual_text = actual_text.split()
    elif eval_type == 'characters':
        tokens = [char for char in predicted_text if not re.match(r'\s', char)]
        actual_text = [
            char for char in actual_text if not re.match(r'\s', char)]
    else:
        exit(1)

    pred_counter = Counter(tokens)
    correct_count = 0
    missed_count = 0

    for expected_word in actual_text:
        if expected_word in pred_counter:
            correct_count += 1
            pred_counter[expected_word] -= 1
            if pred_counter[expected_word] == 0:
                del pred_counter[expected_word]
        else:
            missed_count += 1

    inserted_count = sum(pred_counter.values())
    error_count = inserted_count + missed_count
    cell_count_distance = abs(actual_cell_count - predicted_cell_count)

    df_rows.append(
        {'Document name': file[:-5],
         'Correct count': correct_count,
         'Missed count': missed_count,
         'Inserted count': inserted_count,
         'Error count': error_count,
         'Accuracy': round(1 - (error_count/(error_count + correct_count)), 2),
         'Predicted cell count': predicted_cell_count,
         'Actual cell count': actual_cell_count,
         'Cell count distance': cell_count_distance})

df = pd.DataFrame(df_rows)
correct_total = df['Correct count'].sum()
missed_total = df['Missed count'].sum()
inserted_total = df['Inserted count'].sum()
error_total = df['Error count'].sum()
average_accuracy = round(df['Accuracy'].mean(), 2)
predicted_cell_count = df['Predicted cell count'].sum()
actual_cell_count = df['Actual cell count'].sum()
total_cell_count_dist = df['Cell count distance'].sum()
df_rows.append({'Document name': 'Totals',
                'Correct count': correct_total,
                'Missed count': missed_total,
                'Inserted count': inserted_total,
                'Error count': error_total,
                'Accuracy': average_accuracy,
                'Predicted cell count': predicted_cell_count,
                'Actual cell count': actual_cell_count,
                'Cell count distance': total_cell_count_dist})
df = pd.DataFrame(df_rows)

df.to_csv(
    f'results/{table_engine}/{ocr_engine}/score{words}/{eval_type}.csv', index=False)
