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
        DROP TABLE IF EXISTS customers;
        """
    )

    cursor.execute(
        """
        DROP TABLE IF EXISTS orders;
        """
    )

    cursor.execute(
        """
        DROP TABLE IF EXISTS order_details;
        """
    )

    # Create customer table if not exist
    cursor.execute(
        """CREATE TABLE customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone_number VARCHAR(20),
            status VARCHAR(20),
            address TEXT
        );"""
    )

    # create table orders
    cursor.execute(
        """
        CREATE TABLE orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            order_date DATE NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL
        );
        """
    )

    # create table order details
    cursor.execute(
        """
        CREATE TABLE order_details (
            detail_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            quantity INT NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            total_price DECIMAL(10, 2) NOT NULL
        );
        """
    )

    # insert data into customers table
    cursor.execute(
        """
        INSERT INTO customers (customer_name, email, phone_number, status, address)
        VALUES
            ('John Doe', 'john.doe@example.com', '555-123-4567', 'ACTIVE'  ,'123 Main St, Anytown, USA'),
            ('Jane Smith', 'jane.smith@example.com', '555-987-6543', 'ACTIVE' ,'456 Elm St, Othertown, USA'),
            ('Bob Johnson', 'bob.johnson@example.com', '555-555-5555', 'INACTIVE' ,'789 Oak St, Anycity, USA'),
            ('Michael Clarke', 'clarke.michael@example.com', '555-456-8762', 'ACTIVE' ,'809 Oak St, Arizona, USA');
        """
    )

    # insert data into orders table
    cursor.execute(
        """
        INSERT INTO orders (customer_id, order_date, total_amount)
        VALUES
            (1, '2023-01-15', 250.00),
            (1, '2023-02-20', 175.00),
            (2, '2023-01-30', 120.00),
            (3, '2023-03-10', 350.00);

        """
    )

    # insert data into order details table
    cursor.execute(
        """
        INSERT INTO order_details (order_id, product_name, quantity, unit_price, total_price)
        VALUES
            (1, 'Widget A', 5, 41.00, 205.00),
            (1, 'Widget B', 3, 15.00, 45.00),
            (2, 'Widget A', 5, 35.00, 175.00),
            (3, 'Widget C', 3, 40.00, 120.00),
            (4, 'Widget B', 10, 35.00, 350.00);
        """
    )


def customers_with_no_orders(conn):
    cursor = conn.cursor()
    """
    It will fetch all the customers with active status, whether they have orders or not.
    If no order is found for any active customer, order_id will be NULL
    """
    cursor.execute(
        """
        SELECT customers.customer_name, orders.order_id
        FROM customers
        LEFT JOIN orders ON customers.customer_id = orders.customer_id
        WHERE customers.status = 'ACTIVE';
        """
    )
    print(cursor.fetchall())


def customers_with_specific_order_date(conn):
    cursor = conn.cursor()
    """
    It will fetch all the orders placed between specific dates.
    If no customer is found with order placed on specific date, no result will be return.
    Essentially turning left join into inner join
    """
    cursor.execute(
        """
        SELECT customers.customer_name, orders.order_id
        FROM customers
        LEFT JOIN orders ON customers.customer_id = orders.customer_id
        WHERE orders.order_date <= '2023-01-01';
        """
    )
    print(cursor.fetchall())


if __name__ == "__main__":
    conn = Singleton.get_connection("1", "127.0.0.1", 3310, "root", "root")

    prepare_data(conn)
    customers_with_no_orders(conn)
    customers_with_specific_order_date(conn)
