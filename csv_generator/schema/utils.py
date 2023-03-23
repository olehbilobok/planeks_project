import csv
import os
import time
from django.http import JsonResponse


class CSVManager:

    def __init__(self, schema, rows):
        self.schema = schema
        self.rows = rows

    def get_filename(self):
        return self.schema.user.username + '_' + self.schema.schema_name + '.csv'

    def get_file_header(self):
        return [column_name.column_name for column_name in self.schema.columns.order_by('order')]

    def file_writer(self):
        with open(os.path.abspath(f'schema/media/{self.get_filename()}'), 'w') as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=self.schema.get_column_separator_display(),
                quotechar=self.schema.get_string_character_display()
            )
            self.generate_fake_data(writer)
            self.schema.status = True
            self.schema.save()
            return JsonResponse({'success': 'Ready'})

    def generate_fake_data(self, writer):

        time.sleep(5)
        writer.writerow(self.get_file_header())

        for row in range(int(self.rows) + 1):
            data = [f'{column_type.get_type_display()}{row}' for column_type in self.schema.columns.order_by('order')]
            writer.writerow(data)






