import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
PACKAGE = 'battery_warranty_watch'

def read_csv(name):
    with (ROOT / 'data' / name).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))

def read_json(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

class ContractTests(unittest.TestCase):
    def test_package_name_and_data_directory(self):
        self.assertTrue(PACKAGE)
        self.assertTrue((ROOT / 'data').is_dir())

    def test_vehicle_ids_are_stable_across_sources(self):
        vehicles = {row['vehicle_id'] for row in read_csv('vehicles.csv')}
        telemetry = {row['vehicle_id'] for row in read_csv('telemetry.csv')}
        self.assertTrue(telemetry <= vehicles)

    def test_active_model_has_a_cutoff(self):
        models = read_json('model_registry.json')['models']
        self.assertTrue(all(row['trained_until'] for row in models if row['status'] == 'active'))
