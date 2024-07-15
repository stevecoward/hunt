import csv
import json


class Csv:
    @staticmethod
    def write_to_file(data, output_path='hunt-export.csv'):
        headers = data[0].keys()
        if 'domain' in headers:
            ordered_headers = ['domain', 'source', 'category', 'checked_at']
        else:
            ordered_headers = ['source', 'category', 'checked_at']

        with open(output_path, 'w', newline='') as fh:
            writer = csv.DictWriter(fh, fieldnames=ordered_headers)
            writer.writeheader()
            writer.writerows(data) 
