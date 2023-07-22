### Create virtual env using
- python3 -m virtualenv venv env
- pip install -r requirements.txt
- docker-compose up -d -> to run mysql server

### Contains the code for MySql POC in python

- Singleton connection
    - singleton.py
- Connection pooling
    - pool.py
    - To check if required number of connections are made, go inside docker container and run mysql cli
        - docker exec -it mysql bash
        - mysql -u admin -p (admin123)
        - Run the command -> **show status where `variable_name` = 'Threads_connected';**
        - By default session wait timeout and interactive wait timeout is 28800 ( 8 hrs ), to check this -> **SELECT @@global.wait_timeout, @@session.wait_timeout;**
        - As soon as script finish running, the connections are closed. To overcome this and see number of connections made, have used for loop infinitely.
        - If script is running infinitely and we change wait time out to something smaller like 20 secs, connections will get closed after wait timeout.
        - We can change wait timeout globally like -> **SET GLOBAL wait_timeout = 20;** or session wise -> **SET SESSION wait_timeout = 20;**
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
