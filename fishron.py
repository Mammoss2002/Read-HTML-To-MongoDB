import os
import csv
import json
from pymongo import MongoClient

input_folder = 'log_AfterConvert'

def insert_data_to_mongodb(data, client, db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    result = collection.insert_one(data)
    print(f"Data has been inserted with ID: {result.inserted_id}")

client = MongoClient('mongodb://localhost:27017/')
db_name = 'myDatabase'
collection_name = 'internDatabase'

for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        csv_filename = os.path.join(input_folder, filename)
        start_parsing = False
        header = None
        report_info = {}
        data_dict = {}

        with open(csv_filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                if not start_parsing:
                    if len(row) > 0 and ':' in row[0]:
                        key_value = row[0].split(':', 1)
                        if len(key_value) == 2:
                            key = key_value[0].strip()
                            value = key_value[1].strip()
                            if key in ['Serial number', 'Start Date/Time', 'End Date/Time']:
                                report_info[key] = value
                    elif row[0] == 'Process Step' and row[1] == 'Data Name' and row[2] == 'Data Value' and row[3] == 'Unit of Measure' and row[4] == 'Device ID' and row[5] == 'Is Parametric' and row[6] == 'Lower Limit' and row[7] == 'Upper Limit' and row[8] == 'Status':
                        header = row
                        data_dict = {key: [] for key in header}
                        start_parsing = True
                    continue

                if start_parsing:
                    for i, key in enumerate(header):
                        if i < len(row) and row[i].strip():
                            data_dict[key].append(row[i])
                        else:
                            data_dict[key].append("null")

        final_output = {
            "Serial number": report_info.get('Serial number', 'null'),
            "Start Date/Time": report_info.get('Start Date/Time', 'null'),
            "End Date/Time": report_info.get('End Date/Time', 'null'),
            **{key: data_dict.get(key, []) for key in header}
        }
        insert_data_to_mongodb(final_output, client, db_name, collection_name)
