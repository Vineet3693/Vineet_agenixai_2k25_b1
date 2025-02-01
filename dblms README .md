# Library Management System: SQL Database Summary 

## 1. Schema Design and Explanation

### 1.1 Schema Overview
The schema consists of four tables: **Author**, **Books**, **Customer**, and **Transactions**, with the following relationships:
- **Author**: Stores information about book authors, including their `Name` and their `Genre` expertise.
- **Books**: Contains details of the books, including `Title`, `Genre`, `Publication_Date`, and a foreign key `AUTHORID` referencing the `Author` table.
- **Customer**: Stores customer information such as `Name`, `Contact_No`, and `Email`.
- **Transactions**: Tracks borrowing transactions, with references to `BOOKID` and `CUSTOMERID`, as well as `IssueDate` and optional `ReturnDate`.

### 1.2 Schema Relationship Design
The schema was designed using a relational database model to ensure normalization:
- **1-to-Many Relationships**: An author can write multiple books (`Author → Books`), and each book can be issued multiple times to different customers (`Books → Transactions`).
- **Normalization**: Data redundancy is minimized by separating entities into distinct tables, e.g., customers are linked to transactions rather than being directly associated with books.

### 1.3 Key Features of the Schema
- **Primary Keys**: Each table has a unique identifier (e.g., `AUTHORID` for Author).
- **Foreign Keys**: Relationships between tables are enforced via foreign keys (e.g., `AUTHORID` in Books references Author).
- **Data Types**: Appropriate data types are used, such as `VARCHAR` for textual data, `DATE` for dates, and `INT` for numeric identifiers.

---

## 2. SQL Queries and Execution Plans

### Query 1: Retrieve the top 5 most-issued books with their issue count.
```sql
SELECT 
    b.Title, COUNT(t.TRANSACTIONID) AS IssueCount
FROM 
    Transactions t
JOIN 
    Books b ON t.BOOKID = b.BOOKID
GROUP BY 
    b.Title
ORDER BY 
    IssueCount DESC
LIMIT 5;
```
#### Execution Plan Analysis:
- **Join Operation**: Combines `Transactions` and `Books` tables on `BOOKID`.
- **Group By and Aggregate**: Groups by `Title` and calculates the count of transactions.
- **Order By**: Sorts results in descending order of issue count.
- **Limit**: Restricts output to the top 5 entries.

---

### Query 2: List books along with their authors that belong to the "Fantasy" genre, sorted by publication year in descending order.
```sql
SELECT 
    b.Title, a.Name AS AuthorName, b.Publication_Date
FROM 
    Books b
JOIN 
    Author a ON b.AUTHORID = a.AUTHORID
WHERE 
    b.Genre = 'Fantasy'
ORDER BY 
    b.Publication_Date DESC;
```
#### Execution Plan Analysis:
- **Join Operation**: Combines `Books` and `Author` tables on `AUTHORID`.
- **Filter**: Restricts results to rows where `Genre` is "Fantasy".
- **Sort Operation**: Orders results by `Publication_Date` in descending order.

---

### Query 3: Identify the top 3 customers who have borrowed the most books.
```sql
SELECT 
    c.Name, COUNT(t.TRANSACTIONID) AS BorrowCount
FROM 
    Transactions t
JOIN 
    Customer c ON t.CUSTOMERID = c.CUSTOMERID
GROUP BY 
    c.Name
ORDER BY 
    BorrowCount DESC
LIMIT 3;
```
#### Execution Plan Analysis:
- **Join Operation**: Links `Transactions` and `Customer` tables on `CUSTOMERID`.
- **Group By and Aggregate**: Counts transactions grouped by customer name.
- **Order By**: Sorts results by the count of borrowed books in descending order.
- **Limit**: Restricts output to the top 3 customers.

---

### Query 4: List all customers who have overdue books (assume overdue if `ReturnDate` is null and `IssueDate` is older than 30 days).
```sql
SELECT 
    c.Name, c.Email, t.IssueDate
FROM 
    Transactions t
JOIN 
    Customer c ON t.CUSTOMERID = c.CUSTOMERID
WHERE 
    t.ReturnDate IS NULL AND t.IssueDate < CURRENT_DATE - INTERVAL '30 days';
```
#### Execution Plan Analysis:
- **Join Operation**: Links `Transactions` and `Customer` tables on `CUSTOMERID`.
- **Filter**: Selects rows where `ReturnDate` is null and `IssueDate` is older than 30 days.

---

### Query 5: Find authors who have written more than 3 books.
```sql
SELECT 
    a.Name, COUNT(b.BOOKID) AS BookCount
FROM 
    Author a
JOIN 
    Books b ON a.AUTHORID = b.AUTHORID
GROUP BY 
    a.Name
HAVING 
    COUNT(b.BOOKID) > 3;
```
#### Execution Plan Analysis:
- **Join Operation**: Links `Author` and `Books` tables on `AUTHORID`.
- **Group By and Aggregate**: Counts books grouped by author name.
- **Having Clause**: Filters results to include only authors with more than 3 books.

---

### Query 6: Retrieve a list of authors who have books issued in the last 6 months.
```sql
SELECT DISTINCT 
    a.Name
FROM 
    Transactions t
JOIN 
    Books b ON t.BOOKID = b.BOOKID
JOIN 
    Author a ON b.AUTHORID = a.AUTHORID
WHERE 
    t.IssueDate >= CURRENT_DATE - INTERVAL '6 months';
```
#### Execution Plan Analysis:
- **Join Operations**: Links `Transactions`, `Books`, and `Author` tables.
- **Filter**: Selects rows where `IssueDate` is within the last 6 months.
- **Distinct**: Eliminates duplicate author names.

---

### Query 7: Calculate the total number of books currently issued and the percentage of books issued compared to the total available.
```sql
SELECT 
    COUNT(t.TRANSACTIONID) AS TotalIssued, 
    ROUND(COUNT(t.TRANSACTIONID) * 100.0 / COUNT(b.BOOKID), 2) AS PercentageIssued
FROM 
    Books b
LEFT JOIN 
    Transactions t ON b.BOOKID = t.BOOKID AND t.ReturnDate IS NULL;
```
#### Execution Plan Analysis:
- **Join Operation**: Links `Books` and `Transactions` with a condition to include only currently issued books.
- **Aggregate**: Calculates the total count and percentage.

---

### Query 8: Generate a monthly report of issued books for the past year, showing month, book count, and unique customer count.
```sql
SELECT 
    DATE_TRUNC('month', t.IssueDate) AS Month, 
    COUNT(t.TRANSACTIONID) AS BookCount, 
    COUNT(DISTINCT t.CUSTOMERID) AS UniqueCustomers
FROM 
    Transactions t
WHERE 
    t.IssueDate >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY 
    DATE_TRUNC('month', t.IssueDate)
ORDER BY 
    Month;
```
#### Execution Plan Analysis:
- **Filter**: Restricts rows to those issued within the past year.
- **Group By and Aggregate**: Groups transactions by month and calculates book count and unique customer count.
- **Sort Operation**: Orders results by month.

---

### Query 9: Add appropriate indexes to optimize queries.
```sql
CREATE INDEX idx_books_genre ON Books(Genre);
CREATE INDEX idx_transactions_issue_date ON Transactions(IssueDate);
CREATE INDEX idx_transactions_return_date ON Transactions(ReturnDate);
CREATE INDEX idx_transactions_customer_book ON Transactions(CUSTOMERID, BOOKID);
```
#### Explanation:
- **Books(Genre)**: Optimizes queries filtering by genre.
- **Transactions(IssueDate)**: Speeds up date range queries.
- **Transactions(ReturnDate)**: Improves performance for overdue book queries.
- **Transactions(CUSTOMERID, BOOKID)**: Optimizes joins and queries involving these columns.

---

### Query 10: Analyze query execution plans for Query 1 and Query 4 using `EXPLAIN`.
#### Query 1 Execution Plan:
- **Seq Scan on Transactions**: Reads all rows in the `Transactions` table.
- **Hash Join**: Combines data from `Books` and `Transactions` using a hash-based join strategy.
- **GroupAggregate**: Aggregates rows by book title to calculate issue count.

#### Query 4 Execution Plan:
- **Index Scan on Transactions**: Uses an index on `IssueDate` to locate overdue books efficiently.
- **Nested Loop Join**: Matches `Customer` and `Transactions` data using a nested loop strategy.

#### Understanding:
- Query 1's execution involves reading all transactions and grouping them, which could benefit from indexing on `BOOKID`.
- Query 4 leverages indexed filtering, making it efficient for large datasets.
