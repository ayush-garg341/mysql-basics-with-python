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
            """set session transaction isolation level repeatable read;"""
        )  # ----T1
        cursor.execute("SELECT * FROM test;")
        print("thread 1 --- ", cursor.fetchall())

        cursor.execute("commit;")


def thread_2(conn):
    # start transaction T2
    with conn.cursor() as cursor_t2:
        cursor_t2.execute(
            """set session transaction isolation level read committed;"""
        )  # ----T2

        cursor_t2.execute("""begin;""")
        cursor_t2.execute("SELECT * from test;")
        print("thread 2 -- ", cursor_t2.fetchall())

        cursor_t2.execute("UPDATE test SET value = 12 WHERE id = 1;")
        cursor_t2.execute("""insert into test (id, value) values (3, 40);""")
        cursor_t2.execute("SELECT * from test")
        print("thread 2 -- ", cursor_t2.fetchall())
        cursor_t2.execute("commit;")
        print("thread 2 committed")


def thread_3(conn):
    with conn.cursor() as cursor_t3:
        cursor_t3.execute(
            """set session transaction isolation level read committed;"""
        )  # ----T2

        cursor_t3.execute("""begin;""")

        cursor_t3.execute("SELECT * from test")
        print("thread 3 -- ", cursor_t3.fetchall())
        cursor_t3.execute("UPDATE test SET value = 22 WHERE id = 2;")
        cursor_t3.execute("""insert into test (id, value) values (4, 50);""")
        cursor_t3.execute("SELECT * from test")
        print("thread 3 -- ", cursor_t3.fetchall())
        cursor_t3.execute("commit;")
        print("thread 3 committed")


def thread_4(conn):
    with conn.cursor() as cursor_t4:
        cursor_t4.execute(
            """set session transaction isolation level read committed;"""
        )  # ----T2

        cursor_t4.execute("""begin;""")

        cursor_t4.execute("SELECT * from test")
        print("thread 4 -- ", cursor_t4.fetchall())
        cursor_t4.execute("""insert into test (id, value) values (5, 60);""")
        cursor_t4.execute("SELECT * from test")
        print("thread 4 -- ", cursor_t4.fetchall())
        cursor_t4.execute("commit;")
        print("thread 4 committed")


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
        cnx3 = connection_pool.get_connection()
        cnx4 = connection_pool.get_connection()
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
        thread3 = Thread(
            target=thread_3,
            args=(cnx3,),
        )
        thread4 = Thread(
            target=thread_4,
            args=(cnx4,),
        )
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        cursor.execute("SELECT * FROM test;")
        print("Main thread --- ", cursor.fetchall())
        cursor.execute("drop table test;")
    except Exception as e:
        print(e)
