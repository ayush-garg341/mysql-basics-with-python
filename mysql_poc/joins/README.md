### Various join types in MySql

#### INNER JOIN
- Retrieves only the rows that have matching values in both tables.
- Use cases of inner join
    - Retrieving Related Data from two tables.
    - Data Validation
    - Combining Information
    - Filtering Based on Multiple Criteria in where clause
    - Calculating Aggregates
- but which part is executed first,  join clause or where clause ?
    - JOIN clause is executed first to combine rows from the specified tables based on the join condition, and then the WHERE clause is applied to filter the rows from the joined result set.

#### LEFT JOIN ( LEFT OUTER JOIN )
-  To retrieve all rows from the left table (the table mentioned before the LEFT JOIN) and the matching rows from the right table (the table mentioned after the LEFT JOIN)
-  If there's no match in the right table, NULL values are returned.
- How does where clause works in left join ?
    - Filtering conditions on the Left table :- Conditions specified in the WHERE clause are applied to the rows of the left table before the join operation occurs.
        - This means that the WHERE clause filters the rows in the left table based on the specified conditions.
    - Filtering Conditions on the Result Set :- Conditions applied to columns from the right table in the WHERE clause can affect the result set. However, if you use conditions on columns from the right table in the WHERE clause, it essentially turns the LEFT JOIN into an INNER JOIN.
- customers table on left and orders table on right.

#### RIGHT JOIN ( RIGHT OUTER JOIN )
- Retrieves all rows from the right table and the matched rows from the left table. If there's no match in the left table, NULL values are returned.
- How does where clause works in left join ?
    - Filtering conditions on the right table :- Conditions specified in the WHERE clause are applied to the rows of the right table before the join operation occurs.
        -  This means that the WHERE clause filters the rows in the right table based on the specified conditions.
    - Filtering Conditions on the Result Set :- Conditions applied to columns from the left table in the WHERE clause can affect the result set. It turns Right join into Inner join.
- customers table on left and orders table on right.

#### FULL JOIN ( FULL OUTER JOIN )
- Retrieves all rows when there is a match in either the left or right table. If there's no match, NULL values are returned.
- Combines the result sets of both a LEFT JOIN and a RIGHT JOIN.
- It returns all rows from both tables, matching them where possible and filling in NULL values for columns where there are no matches in either the left or right table.
- Use case of Full outer join
    - Finding Missing Data
        - For example, suppose we have two tables, "employees" and "assignments." We can use a FULL JOIN to find employees who are not assigned to any task and tasks that are not assigned to any employee or if we have two tables, 'orders' and 'customers' we can use FULL JOIN to find the customers who have not placed any orders and orders that do not belong to any customer.
    - Comparing two data sets
        - A FULL JOIN can be used to compare two data sets, identifying matching and non-matching rows in both sets.
- NOTE :- MySQL does not support FULL JOIN yet, but we can achieve the functionality with left join + union + right join

#### CROSS JOIN ( CARTESIAN JOIN )
- Combines every row from one table with every row from another table, resulting in a Cartesian product of the two tables.
- It's a powerful operation but should be used with caution because it can generate very large result sets.
- It does not operate on a common key in both tables, as we saw previously.

#### SELF JOIN
- Useful when you have hierarchical data or relationships within a single table.
- Let's say you have a table called "employees" with a hierarchical structure, where each employee has a manager who is also an employee.

#### NATURAL JOIN
- Combines two tables based on columns with the same name and data type.
- Less commonly used as compared to left, right, inner join.
- Data type and column name must be consistent among tables.

#### STRAIGHT JOIN
- Used to force the optimizer to execute the SELECT query in the order in which the tables are listed in the FROM clause.
- This means that the tables are joined in the order ( enforces the join sequence ) they appear in the query, rather than the optimizer determining the join order based on its own optimization algorithms.
- Usecase of this is relatively rare and should be considered carefully.

#### How Multiple INNER JOINs execute ?
- When we perform multiple INNER JOINs, they are executed in sequence from left to right.
- The result of multiple INNER JOINs is a single result set that includes columns from all the joined tables.
- The rows in the result set satisfy all the join conditions specified in the JOIN clauses.
