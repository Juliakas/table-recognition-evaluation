import os

pdf_files = os.listdir('icdar2013/pdfs')

for file in pdf_files:
    os.system(
        f'pdftoppm icdar2013/pdfs/{file} icdar2013/images/{file[:-4]} -png')
