from django.core.management.base import BaseCommand, CommandError
from inventory.models import Item
import csv


class Command(BaseCommand):
    help = 'Imports inventory from a CSV to add new items or update stats on existing items'

    def add_arguments(self, parser):
        parser.add_argument('input_file', nargs=1, type=str)

    def handle(self, *args, **options):
        print(options['input_file'])
        with open(options['input_file'][0]) as input_file:
            csvreader = csv.reader(input_file)
            header_row = next(csvreader)
            # first column has no header value, but we expect it to be the ID.
            header_row[0] = 'internal_id'
            header_row = [i.lower().strip() for i in header_row]
            print(header_row)
            for row in csvreader:
                print(row)
                row_data = dict(zip(header_row, row))
                # we will require, at a minimum, an internal id, item name and a quantity in stock to ensure that the
                # row represents a valid item.
                if not row_data['internal_id'] or not row_data['name'] or not row_data['quantity in stock']:
                    continue

                inventory_metadata = {
                    'name': row_data['name'],
                    'description': row_data['description'],
                    'vendor': row_data['vendor']
                }
                try:
                    inventory_metadata['unit_price'] = float(row_data['unit price'].strip('$'))
                except ValueError:
                    inventory_metadata['unit_price'] = 0

                try:
                    inventory_metadata['qty_in_stock'] = int(row_data['quantity in stock'])
                except ValueError:
                    inventory_metadata['qty_in_stock'] = 0

                try:
                    inventory_metadata['reorder_level'] = int(row_data['reorder level'])
                except ValueError:
                    inventory_metadata['reorder_level'] = 0

                try:
                    inventory_metadata['qty_in_reorder'] = int(row_data['quantity in reorder'])
                except ValueError:
                    inventory_metadata['qty_in_reorder'] = 0

                try:
                    inventory_metadata['t_code'] = row_data['t-code']
                except KeyError:
                    inventory_metadata['t_code'] = None

                Item.objects.update_or_create(internal_id=row_data['internal_id'], defaults=inventory_metadata)





