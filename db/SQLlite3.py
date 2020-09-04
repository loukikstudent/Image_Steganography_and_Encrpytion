import sqlite3
import logging
import uuid
from functools import wraps

logging.basicConfig(level=logging.DEBUG)


class RD_Manager:
    def __init__(self, db_name: str):
        """

        :rtype: object
        """
        self.db_name = db_name
        # self.connection, self.cursor = self.create_connection()
        # if not self.check_db():

    def create_connection(func):
        def wrapper(inst, *args, **kwargs):
            cnn = sqlite3.connect("../"+inst.db_name)
            logging.debug(f"Connetion Created for func: {func.__name__} with args: {args} and kwargs: {kwargs}")
            cour = cnn.cursor()
            cour.close()
            r = func(inst,cnn, *args, **kwargs)
            cnn.close()
            return r
        logging.debug(f"Connetion Close for func: {func.__name__} ")
        return wrapper

    @create_connection
    def check_db(self, cnn, *args, **kwargs):
        cour = cnn.cursor()
        c = cour.execute('SELECT name FROM sqlite_master').fetchall()
        cour.close()
        print(c)

    # def create_connection(self):
    #     con = sqlite3.connect(self.db_name)
    #     c = con.cursor()
    #     logging.debug("Connection Created")
    #     return con, c

    @create_connection
    def create_table(self):
        query = "CREATE TABLE d3 (UUID BLOB NOT NULL UNIQUE PRIMARY KEY , KEY1 string NOT NULL, KEY2 string NOT NULL, KEY3 string NOT NULL,DATA string NOT NULL );"
        self.cursor.execute(query)

        logging.info("Prime Table Connected")

    def add_d3(self, key1: str, key2: str, key3: str, data: str):
        id = self.gen_uuid()
        query = "INSERT INTO d3 VALUES (?,?,?,?,?)"
        self.c.execute(query, (id, key1, key2, key3, data,))
        self.connection.commit()

    def gen_uuid(self):
        id = uuid.uuid4()
        id = id.bytes
        return id


if __name__ == "__main__":
    db = RD_Manager("test.sqlite3")
    db.check_db()
