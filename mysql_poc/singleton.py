from MySQLdb import _mysql
from threading import Lock


class Singleton:
    _connection = None

    def __init__(self):
        pass

    @classmethod
    def get_connection(cls, host, port, user, pwd):
        # create a lock
        lock = Lock()

        # acquire the lock
        lock.acquire()
        if cls._connection is None:
            print("Connection does not exist")
            connection = cls.create_connection(host, port, user, pwd)
            cls._connection = connection
        lock.release()
        return cls._connection

    @staticmethod
    def create_connection(host, port, user, pwd):
        print("Creating new connection")
        db = _mysql.connect(host=host, port=port, user=user, password=pwd)
        return db
        # print(db)
        # db.query("""SHOW databases""")

        # r = db.store_result()
        # print(r)
        # print(r.fetch_row(maxrows=0))


db_object1 = Singleton.get_connection("127.0.0.1", 3310, "admin", "admin123")
db_object2 = Singleton.get_connection("127.0.0.1", 3310, "admin", "admin123")

print(db_object1)
print(db_object2)
