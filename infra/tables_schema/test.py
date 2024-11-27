import json
import unittest

import jq
import ndjson
from google.cloud import bigquery
from google.cloud import storage
import logging
import os
from typing import Dict
from typing import List
import functions_framework
import ndjson
from google.cloud import bigquery
from google.cloud import storage
from io import StringIO

class MyTestCase(unittest.TestCase):
    def test_something(self):
        storage_client = storage.Client()
        #gs://data-files-001/pubmed.json
        bucket = storage_client.get_bucket("data-files-001")
        blob = bucket.get_blob("pubmed.json")

        json_data_string = blob.download_as_string()
        json_data_as_dicts: List[Dict] = json.loads(json_data_string)
        print(json_data_as_dicts)

        print(jq.compile(".[]").input_value(json_data_as_dicts).text())
        client = bigquery.Client()
       # schema =[bigquery.SchemaField(name=x.get('name'),field_type=x.get('type'),mode=x.get('mode'),description=x.get('description')) for x in json_data_as_dicts]
       # print(schema)
        self.assertEqual(True, True)  # add assertion here





{"key01": "value01", "key02": "value02", "keyN": "valueN"}
{"key01": "value01", "key02": "value02", "keyN": "valueN"}
{"key01": "value01", "key02": "value02", "keyN": "valueN"}
if __name__ == '__main__':
    unittest.main()
