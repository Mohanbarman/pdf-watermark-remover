from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
import bs4
import sys
import os


def remove_watermark(svg_in_path, svg_out_path, is_first=False):
    with open(svg_in_path, 'r') as f:
        data = f.read()

    soup = BeautifulSoup(data, 'html.parser')
    elems = soup.findAll(attrs={"data-name": "Artifact", "id": "Layer-1"})
    # Removing watermark elements
    for i in elems:
        i.decompose()

    # Only for first page of the pdf
    if (is_first):
        elems = soup.findAll(attrs={'data-name': 'P', 'id': 'Layer-1'})
        elems[0].decompose()
        elems[1].decompose()

    with open(svg_out_path, 'w') as f:
        f.write(str(soup))

def svg_to_pdf(input_dir, output_dir):
    filenames = os.listdir(input_dir)
    filenames.sort()
    for filename in filenames:
        output_path = f'{output_dir}/{filename.replace(".svg", ".pdf")}'
        os.system(f'rsvg-convert -f pdf -o {output_path} {input_dir}/{filename}')
        print(f'pdf saved : {output_path}')

def join_pdfs(input_dir, output_filename):
    filenames = os.listdir(input_dir)
    filenames.sort()
    all_files = ''

    for filename in filenames:
        all_files += f'{input_dir}/{filename} '

    os.system(f'pdfunite {all_files} {output_filename}')
    print(f'All pdfs merged into {output_filename}')


filenames = os.listdir('pdfs')
filenames.sort()

for i, filename in enumerate(filenames):
    remove_watermark(f'pdfs/{filename}', f'output/{filename}', i==0)
    print(f'watermark removed : output/{filename}')

svg_to_pdf('output', 'output_pdfs')
join_pdfs('output_pdfs', 'final.pdf')