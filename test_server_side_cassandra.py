import unittest
from server_side_methods.db.Cassandra import Cassandra_db
import json


class TestServerSide(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.instance = Cassandra_db('d3', 'test')

    def test_keyspace(self):
        # Testing if the keyspace Exists
        self.assertTrue(self.instance.cluster.metadata.keyspaces['d3'])

        # Testing if the table exists
        self.assertTrue('test' in self.instance.cluster.metadata.keyspaces['d3'].tables)

        # Testing adding data into the tabel
        jsonData = {'uuid': '100', 'key': '12341234', 'data': 'helloWorld!'}
        jsonData_dumped = json.dumps(jsonData)
        
        self.assertTrue(self.instance.add(jsonData_dumped))
        result = self.instance.get(jsonData_dumped)
        self.assertEqual(jsonData['data'], [i for i in result][0]['data'])