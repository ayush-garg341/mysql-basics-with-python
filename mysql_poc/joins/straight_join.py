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
        DROP TABLE IF EXISTS projects;
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
        CREATE TABLE projects (
            project_id INT AUTO_INCREMENT PRIMARY KEY,
            project_name VARCHAR(255) NOT NULL,
            start_date DATE,
            end_date DATE,
            description TEXT,
            employee_id INT
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

    cursor.execute(
        """
        INSERT INTO projects (project_name, start_date, end_date, description, employee_id)
        VALUES
            ('Project A', '2023-01-10', '2023-03-15', 'This is Project A', 1),
            ('Project B', '2023-02-15', '2023-04-30', 'Project B details', 2),
            ('Project C', '2023-03-01', '2023-05-20', 'Description for Project C', 3),
            ('Project D', '2023-04-20', '2023-06-30', 'Details for Project D', 2);
        """
    )


def straight_join(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM employees
        STRAIGHT_JOIN departments ON employees.department_id = departments.department_id
        STRAIGHT_JOIN projects ON employees.employee_id = projects.employee_id;
        """
    )
    print(cursor.fetchall())


if __name__ == "__main__":
    conn = Singleton.get_connection("1", "127.0.0.1", 3310, "root", "root")

    prepare_data(conn)
    straight_join(conn)
