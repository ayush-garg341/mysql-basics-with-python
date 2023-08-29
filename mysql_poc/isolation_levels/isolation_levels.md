Isolation Levels
G0: Write Cycles (dirty writes)
G1a: Aborted Reads (dirty reads, cascaded aborts)
- Read Uncommitted
    - A transaction can see changes to data made by other transactions that are not committed yet.
    - With this isolation level, there is always chance of getting a “Dirty-Read”.
    - MySQL "read uncommitted" prevents Write Cycles (G0) by locking updated rows.
    - MySQL "read uncommitted" does not prevent Aborted Reads (G1a):
    - There might be some race conditions on row which is updated by both the transactions.
        - It depends upon who acquires lock first while updating.
        - Sometime (sometime not) we see newly inserted (thread 2) row with id 3 in thread 1 because in read uncommitted we can see uncommitted changes in another transaction.
    - In the example shown, both T1, T2 tries to update row with id = 1, which might cause issues since updating transactions acquires locks.
        - Then it might depend on several factors in another transaction (T2) who is updating same row like ...
            - If that lock is still held by transaction (T1), then T2 won't be able to make the changes.
            - Or when T2 tried to acquire lock, was the lock released by T1, if released T2 can safely update the row.
            - In some cases lock is released by transaction after certain timeout.
    - This is the reason in the main thread we are seeing id 1 with value either 11 or 12.
    - But there is consistency in id 2 value as this is updated by T1 only.

- Read Committed
    - When reading from db, you will only see data that has been committed. ( No dirty reads )
    - When writing to the db, you will only overwrite data that has been committed. ( No dirty writes )
    - This level allows transactions to see only committed changes made by other transactions.
    - In this we notice that thread2 does not get row id 1 result. Why ?
        - Becuase that row is locked by another Transaction T1.
    - When we see row id 3 in T1, it means that T2 has already been committed. To make sure this is happening, we can add a rollback in T2 and check if that still happening.
        - When we rollback in T2, no changes are reflected in T1 and main thread.
- Snapshot Isolation
