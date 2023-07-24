### Create virtual env using
- python3 -m virtualenv venv env
- pip install -r requirements.txt
- docker-compose up -d -> to run mysql server

### Contains the code for MySql POC in python

- wait_timeout -> This is said to be the number of seconds the server waits for activity on a noninteractive connection before closing it.
- connect_timeout -> The number of seconds that the mysqld server waits to connect the packet before responding with a Bad handshake.
- sleep -> A sleeping MySQL query is an inactive open connection. When too many exist at the same time, the MySQL server will run out of connections,
            causing the server to be unable to process queries.

- Singleton connection
    - singleton.py
    - close() -> The Close method rolls back any pending transactions. When connection pooling is disabled it closes the connection to mysql server and can not be reused.
    - To check if required number of connections are made, go inside docker container and run mysql cli
        - docker exec -it mysql bash
        - mysql -u admin -p (admin123)
        - Run the command -> **show status where `variable_name` = 'Threads_connected';**
        - By default session wait timeout and interactive wait timeout is 28800 ( 8 hrs ), to check this -> **SELECT @@global.wait_timeout, @@session.wait_timeout;**
        - As soon as script finish running, the connections are closed. To overcome this and see number of connections made, have used for loop infinitely.
        - If script is running infinitely and we change wait time out to something smaller like 20 secs, connections will get closed after wait timeout.
        - We can change wait timeout globally like -> **SET GLOBAL wait_timeout = 20;** or session wise -> **SET SESSION wait_timeout = 20;**
- Connection pooling
    - pool.py
    - close() -> It puts back the connection into the pool and can be re-used.
- Relation between sleep, close and wait_timout ?
    - When we create any mysql connection, it remains open unitl wait_timeout. So if let's say wait_timout is 120 secs it will be open till 120 secs.
    - But if in mean time your connection is not performing any query, it will go into sleep state.
    - We can check that using **show full processlist;**
    - But let's say we want to close the connection, we can run close() method on connection object.
    - Again running **show full processlist;** will show connection one less.
    - To demonstrate this, see and run the code **python3 mysql_poc/singleton.py**. (I have used infinite loops so that connections do not close upon script finishing.)
    - In another terminal tab, open the docker mysql and run above commands.
- Connection re-using
    - connection_reusing.py
- Transaction Isolation Levels
- What happens with mysql connection when code breaks in between
    - If application is still up like a web server running then connection will be there in memory else will be lost.
- Connection loading
- MySql important config vars
- Optmizations of config vars
- Types of Indexing ..
- Types of joins mysql support
- Data types mysql support ..
