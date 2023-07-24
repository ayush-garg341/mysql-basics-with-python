from MySQLdb import _mysql
from threading import Lock, Thread
import time


class SingletonWithoutThread:
    _connection = None
    singleton_conn = set()

    def __init__(self):
        pass

    @classmethod
    def get_connection(cls, thread_name, host, port, user, pwd):
        print("Executing {name} thread ".format(name=thread_name))

        if cls._connection is None:
            print("Connection does not exist")
            connection = cls.create_connection(host, port, user, pwd)
            cls._connection = connection
        cls.singleton_conn.add(cls._connection)
        return cls._connection

    @staticmethod
    def create_connection(host, port, user, pwd):
        print("Creating new connection")
        db = _mysql.connect(host=host, port=port, user=user, password=pwd)
        return db


def without_thread():
    db1 = SingletonWithoutThread.get_connection(
        1, "127.0.0.1", 3310, "admin", "admin123"
    )
    db2 = SingletonWithoutThread.get_connection(
        2, "127.0.0.1", 3310, "admin", "admin123"
    )
    print(db1 is db2)
    print(len(SingletonWithoutThread.singleton_conn))
    time.sleep(10)
    db1.close()


class SingletonWithThread:
    _connection = None
    singleton_conn = set()
    _lock = Lock()

    def __init__(self):
        pass

    @classmethod
    def get_connection(cls, thread_name, host, port, user, pwd):
        cls._lock.acquire()
        print("Executing {name} thread ".format(name=thread_name))
        if cls._connection is None:
            print("Connection does not exist")
            connection = cls.create_connection(host, port, user, pwd)
            cls._connection = connection
        cls.singleton_conn.add(cls._connection)
        cls._lock.release()
        return cls._connection

    @staticmethod
    def create_connection(host, port, user, pwd):
        print("Creating new connection")
        db = _mysql.connect(host=host, port=port, user=user, password=pwd)
        return db


def with_thread():
    thread1 = Thread(
        target=SingletonWithThread.get_connection,
        args=(
            1,
            "127.0.0.1",
            3310,
            "admin",
            "admin123",
        ),
    )
    thread2 = Thread(
        target=SingletonWithThread.get_connection,
        args=(
            2,
            "127.0.0.1",
            3310,
            "admin",
            "admin123",
        ),
    )
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print(len(SingletonWithThread.singleton_conn))


if __name__ == "__main__":
    without_thread()
    print("--------------------------")
    with_thread()
    while True:
        pass
