Isolation Levels
G0: Write Cycles (dirty writes)
G1a: Aborted Reads (dirty reads, cascaded aborts)
Remember:-  A transaction can typically see its own changes before it commits. In most relational database systems, the changes made within a transaction are immediately visible to that transaction itself, even before the transaction is committed.
- Read Uncommitted
    - A transaction can see changes to data made by other transactions that are not committed yet.
    - With this isolation level, there is always chance of getting a “Dirty-Read”.
    - MySQL "read uncommitted" prevents Write Cycles (G0) by locking updated rows.
    - MySQL "read uncommitted" does not prevent Aborted Reads (G1a):
    - There might be some race conditions on row which is updated by both the transactions.
        - It depends upon who acquires lock first while updating.
        - Sometime (sometime not) we see newly inserted (thread 2) row with id 3 in thread 1 because in read uncommitted we can see uncommitted changes in another transaction.
    - In the example shown, both T1, T2 tries to update row with id = 1, which might cause issues since updating same row acquires locks.
        - Then it might depend on several factors in another transaction (T2) who is updating same row like ...
            - If that lock is still held by transaction (T1), then T2 won't be able to make the changes.
            - Or when T2 tried to acquire lock, was the lock released by T1, if released T2 can safely update the row.
            - In some cases lock is released by transaction after certain timeout.
    - This is the reason in the main thread we are seeing id 1 with value either 11 or 12.
    - But there is consistency in id 2 value as this is updated by T1 only.
    -  In this isolation level, you can read uncommitted changes made by other transactions, including rows that are locked by other transactions. This can lead to dirty reads, where you see data that might not end up being committed.

- Read Committed
    - When reading from db, you will only see data that has been committed. ( No dirty reads )
    - When writing to the db, you will only overwrite data that has been committed. ( No dirty writes )
    - This level allows transactions to see only committed changes made by other transactions.
    - In this we notice that thread2 does not get row id 1 result. Why ?
        - Becuase that row is locked by another Transaction T1.
    - When we see row id 3 in T1, it means that T2 has already been committed. To make sure this is happening, we can add a rollback in T2 and check if that still happening.
        - When we rollback in T2, no changes are reflected in T1 and main thread.
    - In this isolation level, you can only read committed changes made by other transactions. If a row is locked by another transaction, attempting to select that row will either block until the lock is released or return after a timeout, depending on the database system's configuration.

- Snapshot Isolation
    - The idea is each transaction reads from a consistent snapshot of the database i.e transaction sees all the data that was committed in the db at the start of transaction.
    - Even if data is subsequently changed by another transaction, each transaction sees only the old data from that particular point in time.
    - Boon for backups and analytics.
    - Key :- Readers never block writers and writers never block readers.
    - The db must potentially keep several different committed version of an object, because various in progress transactions may need to see the state of db at different points in time.
    - Uses MVCC (multi version concurrency control)
    - Snapshot is like a screenshot of committed data in the db.
    - Read committed uses a separate snapshot for each query ( in a transaction ), while snapshot isolation uses the same snapshot for an entire transaction.
    - Transaction Ids are used to tag data written by transaction.
        - When a transaction reads from database, txn Ids are used to decide which objects it can see and which are visible.
    - An update is converted into delete and create.
    - An object is visible if both the conditions are true:-
        - At the time when reader's transaction started, tha transaction that created the object had already committed..
        - The object is not marked for deletion or if it is, that transaction that requested the deletion had not yet committed at the time when the reader's transaction started.
    - Another way to put visibility of an object:
        - When transactions start, they are given an ever increasing txn id.
        - Let's say a txn start reading objects from db, there will be three cases:-
            - All txn that are in progress at that point in time ( not committed yet ), even though they are eventually committed will be ignored.
            - All txn that are aborted later, will be ignored.
            - All txn with id greater than the current txn will be ignored.
            - Rest all other objects will be visible to current txn.
    - New version is created everytime a value is changed rather than updating value inplace.
    - But mysql does not provide native support for snapshot isolation. ( https://stackoverflow.com/questions/9880555/how-to-set-innodb-in-mysql-to-the-snapshot-isolation-level )

- Repeatable Read
    - It Ensures that once a transaction reads a row of data, that data will remain unchanged for the duration of the transaction. This is achieved by placing shared locks on the rows being read.
    - These locks prevent other transactions from modifying the locked rows until the reading transaction completes.
    - When one transaction holds a lock on a row, another transaction attempting to access the same locked row might be blocked until the lock is released.
    - Here's what typically happens in "Repeatable Read" isolation:
        - Lock Acquisition:- When Transaction A reads a row in the "Repeatable Read" isolation level, it acquires a shared lock on that row. This lock prevents other transactions from acquiring an exclusive (write) lock on the same row, ensuring that the data isn't modified while Transaction A is using it.
        - Blocked Transaction:- If Transaction B attempts to read the same row that Transaction A has locked, Transaction B will be blocked until the lock held by Transaction A is released. This ensures that Transaction B sees a consistent view of the data and doesn't read data that might change before it is committed.
        - Lock Release:- Once Transaction A releases the shared lock (typically by committing or rolling back the transaction), Transaction B is unblocked and can proceed to access the row.
    - If you're experiencing situations where Transaction B is blocked and not returning any data, it's likely because the row it's trying to access is currently locked by Transaction.
    - Once Transaction A releases the lock, Transaction B should be able to access the row and retrieve the data.
- Serializable Isolation

