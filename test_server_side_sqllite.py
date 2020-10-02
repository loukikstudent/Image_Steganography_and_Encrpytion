import unittest
from server_side_methods.db.SQLlite3 import RD_Manager


class TestServerSideSQLLITE(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.instance = RD_Manager("../unit_testing.sqlite3")

    def test_db(self):
        # Testing if the tables exists
        self.assertTrue(self.instance.check_db())

        # Testing if adding into table is possible
        id = self.instance.add(key="123123", data="helloWorld!")

        # Testing if the added record can be accessed
        result = self.instance.view(id=id, key="123123")
        self.assertEqual("helloWorld!", result[0])

        # Testing if record can be deleted
        self.instance.delete(id=id)
        result = self.instance.view(id=id, key="123123")
        self.assertIsNone(result)