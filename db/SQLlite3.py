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
        # check table, if not exist then create
        if not self.check_db():
            self.create_table()


    def create_connection(func) :
        def wrapper(inst, *args, **kwargs):
            cnn = sqlite3.connect(inst.db_name)
            logging.debug(f"Connetion Created for func: {func.__name__}")
            cur = cnn.cursor()
            logging.debug(f"Cursor Created for func: {func.__name__} with args: {args} and kwargs: {kwargs}")
            try:
                r = func(inst,cur, *args, **kwargs)
            except Exception as e:
                logging.error(f"Function ({func._name__}) Execution failed")
                logging.info("Initiating Roll Back")
                cnn.rollback()
                logging.info("Rollback completed")
            else:
                cnn.commit()
            finally:
                cur.close()
                logging.debug(f"Cursor Close for func: {func.__name__} ")
                cnn.close()
                logging.debug(f"Connection Close for func: {func.__name__} ")
            return r
        return wrapper

    @create_connection
    def check_db(self, cur,**kwargs):
        """

        :type cur: sqlite3.connection.cursor
        """
        if cur.execute('SELECT name FROM sqlite_master where name = ?',('d3',)).fetchone():
            logging.info("Table D3 not found!")
            return True
        return False


    @create_connection
    def create_table(self,cur,**kwargs):
        query = "CREATE TABLE d3 (UUID BLOB NOT NULL UNIQUE PRIMARY KEY , KEY1 string NOT NULL, KEY2 string NOT NULL, KEY3 string NOT NULL,DATA string NOT NULL );"
        cur.execute(query)
        logging.info("D3 Table Connected")

    @create_connection
    def add(self, cur,**kwargs):
        id = self.gen_uuid()
        query = "INSERT INTO d3 VALUES (?,?,?,?,?)"
        cur.execute(query, (id, kwargs['key1'], kwargs['key2'], kwargs['key3'], kwargs['data'],))
        logging.info(f"Entry updated for id: {id}")


    @create_connection
    def view(self, cur, **kwargs):
        query = "SELECT data FROM d3 WHERE uuid=? and key1=? and key2=? and key3=?"
        res = cur.execute(query,(kwargs['id'],kwargs['key1'],kwargs['key2'],kwargs['key3'],)).fetchone()
        logging.info(f"Entry with id: {kwargs['id']} accessed")
        return res

    @create_connection
    def delete(self, cur,**kwargs):
        query = "DELETE from d3 where uuid = ?"
        cur.execute(query,(kwargs['id'],))
        logging.info(f"Entry with id: {kwargs['id']} from database")


    def gen_uuid(self):
        id = uuid.uuid4()
        id = id.bytes
        return id


if __name__ == "__main__":
    db = RD_Manager("../test.sqlite3")
