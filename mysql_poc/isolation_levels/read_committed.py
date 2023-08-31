import MySQLdb as db
from threading import Lock, Thread
from mysql.connector import pooling
import time


class ConnectionReusing:
    def __init__(self):
        pass

    def create_pool(self, **kwargs):
        cnx = pooling.MySQLConnectionPool(**kwargs)
        return cnx


def thread_1(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """set session transaction isolation level read committed;"""
        )  # ----T1
        cursor.execute("SELECT * FROM test;")
        print("thread 1 --- ", cursor.fetchall())

        cursor.execute("""begin;""")
        cursor.execute("UPDATE test SET value = 11 WHERE id = 1;")

        cursor.execute("SELECT * FROM test;")
        print("thread 1 --- ", cursor.fetchall())

        cursor.execute("UPDATE test SET value = 21 WHERE id = 2;")
        cursor.execute("commit;")


def thread_2(conn):
    # start transaction T2
    with conn.cursor() as cursor_t2:
        cursor_t2.execute(
            """set session transaction isolation level read committed;"""
        )  # ----T2

        cursor_t2.execute("""begin;""")
        cursor_t2.execute("SELECT * from test where id = 1;")
        print("thread 2 -- ", cursor_t2.fetchall())

        cursor_t2.execute("UPDATE test SET value = 12 WHERE id = 1;")
        cursor_t2.execute("""insert into test (id, value) values (3, 40);""")
        # cursor_t2.execute("commit;")
        cursor_t2.execute("""rollback;""")


if __name__ == "__main__":
    try:
        pool1_config = {
            "database": "test",
            "user": "admin",
            "password": "admin123",
            "port": 3310,
            "pool_name": "testing_pool",
            "pool_size": 5,
        }

        pool1 = ConnectionReusing()
        connection_pool = pool1.create_pool(**pool1_config)

        cnx1 = connection_pool.get_connection()
        cnx2 = connection_pool.get_connection()
        cursor = cnx1.cursor()
        cursor.execute("""Show databases;""")
        print(cursor.fetchall())
        cursor.execute("use test;")
        cursor.execute("""select @@transaction_ISOLATION;""")
        print(cursor.fetchall())
        cursor.execute(
            """create table test (id int primary key, value int) engine=innodb;"""
        )
        cursor.execute("""begin;""")
        cursor.execute("""insert into test (id, value) values (1, 10), (2, 20);""")
        cursor.execute("commit;")
        thread1 = Thread(
            target=thread_1,
            args=(cnx1,),
        )
        thread2 = Thread(
            target=thread_2,
            args=(cnx2,),
        )
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        cursor.execute("SELECT * FROM test;")
        print("Main thread --- ", cursor.fetchall())
        cursor.execute("drop table test;")
    except Exception as e:
        print(e)
