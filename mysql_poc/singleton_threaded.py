import MySQLdb as db
from threading import Lock, Thread
import time


class SingletonThreaded:
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
        conn = db.connect(host=host, port=port, user=user, password=pwd)
        return conn


def thread_1(name):
    conn = SingletonThreaded.get_connection(
        name,
        "127.0.0.1",
        3310,
        "admin",
        "admin123",
    )
    print("Thread {0} is operating".format(name))
    cursor = conn.cursor()
    print("cursor 1 -- ", cursor)
    try:
        cursor.execute("""SHOW databases;""")
        result = cursor.fetchall()
        print(result)
    except Exception as e:
        print(e)
    cursor.close()


def thread_2(name):
    conn = SingletonThreaded.get_connection(
        name,
        "127.0.0.1",
        3310,
        "admin",
        "admin123",
    )
    print("Thread {0} is operating".format(name))
    cursor = conn.cursor()
    print("cursor 2 -- ", cursor)
    try:
        cursor.execute("""SHOW databases;""")
        result = cursor.fetchall()
        print(result)
    except Exception as e:
        print(e)
    cursor.close()


def with_thread():
    thread1 = Thread(
        target=thread_1,
        args=(1,),
    )
    thread2 = Thread(
        target=thread_2,
        args=(2,),
    )
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print(len(SingletonThreaded.singleton_conn))


def with_thread_sequential():
    thread1 = Thread(
        target=thread_1,
        args=(1,),
    )
    thread2 = Thread(
        target=thread_2,
        args=(2,),
    )
    thread1.start()
    thread1.join()
    thread2.start()
    thread2.join()
    print(len(SingletonThreaded.singleton_conn))


if __name__ == "__main__":
    # with_thread()
    with_thread_sequential()
