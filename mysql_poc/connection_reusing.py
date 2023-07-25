"""
Connection re-use while pooling enabled.
Will make six threads and pool of 5.
Will see how 6th thread gets assigned one of the connection object of pool.
Will also see how to check if connection is alive or dead.
"""


from threading import Lock, Thread
from mysql.connector import pooling
import time


class ConnectionReusing:
    def __init__(self):
        pass

    def create_pool(self, **kwargs):
        cnx = pooling.MySQLConnectionPool(**kwargs)
        return cnx


def thread_connection(db_connection, name, sleep):
    print("name : {0}, db conn : {1}".format(name, db_connection))
    print("sleep after : {}".format(sleep))
    time.sleep(sleep)
    db_connection.close()
    print("closed connection by {0}".format(name))


if __name__ == "__main__":
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
    cnx5 = connection_pool.get_connection()
    con_list = [cnx1, cnx2, cnx3, cnx4, cnx5]

    # Spqwn 5 threads with different timeouts
    thread_list = []

    for i in range(5):
        thread = Thread(
            target=thread_connection,
            args=(
                con_list[i],
                "{0}th thread".format(i),
                (i + 1) * 10,
            ),
        )
        thread.start()
        thread_list.append(thread)

    time.sleep(15)

    thread = Thread(
        target=thread_connection,
        args=(
            connection_pool.get_connection(),
            "6th thread",
            1 * 15,
        ),
    )
    thread.start()
    thread_list.append(thread)

    for thread in thread_list:
        thread.join()
