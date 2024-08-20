import os
from bs4 import BeautifulSoup
import csv

input_folder = 'log_Test'
output_folder = 'log_AfterConvert'
csv_file_prefix = 'output'
csv_file_extension = '.csv'

os.makedirs(output_folder, exist_ok=True)

def get_next_csv_filename(folder_path, prefix, extension):
    existing_files = [f for f in os.listdir(folder_path) if f.startswith(prefix) and f.endswith(extension)]
    file_numbers = [int(f[len(prefix):-len(extension)]) for f in existing_files if f[len(prefix):-len(extension)].isdigit()]
    next_number = max(file_numbers, default=0) + 1
    return os.path.join(folder_path, f"{prefix}{next_number}{extension}")

for filename in os.listdir(input_folder):
    if filename.endswith('.html'):
        html_path = os.path.join(input_folder, filename)
        next_csv_file = get_next_csv_filename(output_folder, csv_file_prefix, csv_file_extension)

        with open(html_path, 'r', encoding='utf-8') as f:
            contents = f.read()

        soup = BeautifulSoup(contents, 'html.parser')

        with open(next_csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            for element in soup.body.contents:
                if element.name == 'table':
                    break
                text = element.get_text(strip=True)
                if text:
                    writer.writerow([text])

            tables = soup.find_all('table')
            
            for table in tables:
                headers = []
                rows = table.find_all('tr')

                if rows:
                    header_row = rows[0]
                    headers = [th.text.strip() for th in header_row.find_all('th')]
                    
                    if not headers:
                        headers = [td.text.strip() for td in header_row.find_all('td')]

                    if headers:
                        writer.writerow(headers)
                    
                    for row in rows[1:]:
                        cols = row.find_all('td')
                        cols = [ele.text.strip() for ele in cols]
                        if cols:
                            writer.writerow(cols)

        print(f'Data from {filename} has been written to {next_csv_file}')
