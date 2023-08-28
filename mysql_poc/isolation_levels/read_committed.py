import pymysql
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
        conn = pymysql.connect(host=host, port=port, user=user, password=pwd)
        return conn


if __name__ == "__main__":
    conn = SingletonThreaded.get_connection(
        "One",
        "127.0.0.1",
        3310,
        "admin",
        "admin123",
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute("""Show databases;""")
            print(cursor.fetchall())
            cursor.execute("use test;")
            cursor.execute(
                """create table test (id int primary key, value int) engine=innodb;"""
            )
            cursor.execute("""insert into test (id, value) values (1, 10), (2, 20);""")
            cursor.execute("""select @@transaction_ISOLATION;""")
            print(cursor.fetchall())
            cursor.execute(
                """set session transaction isolation level read committed;"""
            )  # ----T1
            cursor.execute("""begin;""")
            print("here")
            cursor.execute("UPDATE test SET value = 11 WHERE id = 1;")

            # start transaction T2
            with conn.cursor() as cursor_t2:
                print(cursor is cursor_t2)
                cursor_t2.execute(
                    """set session transaction isolation level read committed;"""
                )  # ----T2
                cursor_t2.execute("""begin;""")

                cursor_t2.execute("SELECT * from test where id = 1;")
                print(cursor_t2.fetchall())

                cursor_t2.execute("UPDATE test SET value = 12 WHERE id = 1;")
                cursor_t2.execute("""insert into test (id, value) values (3, 40);""")

                cursor_t2.execute("commit;")

            cursor.execute("SELECT * FROM test;")
            print(cursor.fetchall())

            cursor.execute("UPDATE test SET value = 21 WHERE id = 2;")
            cursor.execute("commit;")

            # Fetch and print the results within T1
            cursor.execute("SELECT * FROM test;")
            t1_results = cursor.fetchall()
            print("T1 results:")
            for row in t1_results:
                print(row)

            cursor.execute("drop table test;")

    except Exception as e:
        print(e)
    cursor.close()
