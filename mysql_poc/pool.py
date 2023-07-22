# Connection pooling..


from mysql.connector import connect


class PoolingMysqlConnection:
    def __init__(self):
        pass

    def create_pool(self, **kwargs):
        cnx = connect(**kwargs)


pool1_config = {
    "database": "test",
    "user": "admin",
    "password": "admin123",
    "port": 3310,
    "pool_name": "testing_pool",
    "pool_size": 5,
}

pool1 = PoolingMysqlConnection()
pool1.create_pool(**pool1_config)

while True:
    pass
