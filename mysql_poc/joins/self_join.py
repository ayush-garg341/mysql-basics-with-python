import MySQLdb


class Singleton:
    _connection = None

    def __init__(self):
        pass

    @classmethod
    def get_connection(cls, thread_name, host, port, user, pwd):
        print("Executing {name} thread ".format(name=thread_name))

        if cls._connection is None:
            print("Connection does not exist")
            connection = cls.create_connection(host, port, user, pwd)
            cls._connection = connection
        return cls._connection

    @staticmethod
    def create_connection(host, port, user, pwd):
        print("Creating new connection")
        db = MySQLdb.connect(host=host, port=port, user=user, password=pwd)
        return db


def prepare_data(db_con):
    cursor = db_con.cursor()

    # Create test db
    create_db = cursor.execute(
        """CREATE DATABASE IF NOT EXISTS `test` COLLATE 'utf8_general_ci' ;"""
    )

    cursor.execute(
        """
        use test;
        """
    )

    # Drop tables already there in db
    cursor.execute(
        """
        DROP TABLE IF EXISTS employees;
        """
    )

    cursor.execute(
        """
        CREATE TABLE employees (
            employee_id INT PRIMARY KEY,
            employee_name VARCHAR(255) NOT NULL,
            manager_id INT
        );
        """
    )

    cursor.execute(
        """
        INSERT INTO employees (employee_id, employee_name, manager_id)
        VALUES
            (1, 'John Doe', NULL), -- John Doe is the top-level manager
            (2, 'Jane Smith', 1),   -- Jane Smith reports to John Doe
            (3, 'Bob Johnson', 1),  -- Bob Johnson also reports to John Doe
            (4, 'Alice Brown', 2);  -- Alice Brown reports to Jane Smith
        """
    )


def employee_manager(conn):
    cursor = conn.cursor()
    """
    Find the manager of each employee
    """
    cursor.execute(
        """
        SELECT e.employee_name AS employee, m.employee_name AS manager
        FROM employees e
        LEFT JOIN employees m ON e.manager_id = m.employee_id;
        """
    )
    print(cursor.fetchall())


if __name__ == "__main__":
    conn = Singleton.get_connection("1", "127.0.0.1", 3310, "root", "root")

    prepare_data(conn)
    employee_manager(conn)
