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
        DROP TABLE IF EXISTS departments;
        """
    )

    cursor.execute(
        """
        CREATE TABLE employees (
            employee_id INT PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            department_id INT
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE departments (
            department_id INT PRIMARY KEY,
            department_name VARCHAR(255)
        );
        """
    )

    cursor.execute(
        """
        INSERT INTO employees (employee_id, first_name, last_name, department_id)
        VALUES
            (1, 'John', 'Doe', 101),
            (2, 'Jane', 'Smith', 102),
            (3, 'Bob', 'Johnson', 101);
        """
    )

    cursor.execute(
        """
        INSERT INTO departments (department_id, department_name)
        VALUES
            (101, 'HR'),
            (102, 'Finance');
        """
    )


def employee_dept(conn):
    cursor = conn.cursor()
    """
    Find the dept of each employee
    """
    cursor.execute(
        """
        SELECT *
        FROM employees
        NATURAL JOIN departments;
        """
    )
    print(cursor.fetchall())


if __name__ == "__main__":
    conn = Singleton.get_connection("1", "127.0.0.1", 3310, "root", "root")

    prepare_data(conn)
    employee_dept(conn)
