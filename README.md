### SQL Training Module: Industry-Level Concepts

This training module covers key SQL concepts that are essential for working with databases in an industry environment. It includes topics such as data manipulation, optimization, transactions, complex queries, and advanced SQL features. The module will be accompanied by examples, and I'll also recommend a YouTube video for visual learning.

---
#### Create the employees table
```
CREATE TABLE employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Gender VARCHAR(10),
    Department VARCHAR(50),
    JobTitle VARCHAR(50),
    HireDate DATE,
    Salary DECIMAL(10, 2),
    ManagerID INT,
    City VARCHAR(50),
    Country VARCHAR(50)
);
```

#### Insert sample data
```
INSERT INTO employees (EmployeeID, FirstName, LastName, Gender, Department, JobTitle, HireDate, Salary, ManagerID, City, Country)
VALUES
(1, 'John', 'Doe', 'Male', 'IT', 'Software Engineer', '2015-06-01', 80000, 3, 'New York', 'USA'),
(2, 'Jane', 'Smith', 'Female', 'HR', 'HR Manager', '2010-09-15', 90000, NULL, 'Chicago', 'USA'),
(3, 'Alice', 'Johnson', 'Female', 'IT', 'IT Manager', '2008-12-10', 120000, NULL, 'San Francisco', 'USA'),
(4, 'Bob', 'Brown', 'Male', 'Finance', 'Accountant', '2017-04-23', 70000, 5, 'New York', 'USA'),
(5, 'Carol', 'Wilson', 'Female', 'Finance', 'Finance Manager', '2011-03-11', 110000, NULL, 'Chicago', 'USA'),
(6, 'David', 'Lee', 'Male', 'Marketing', 'Marketing Analyst', '2019-11-05', 65000, 7, 'Los Angeles', 'USA'),
(7, 'Eva', 'Davis', 'Female', 'Marketing', 'Marketing Manager', '2014-07-01', 95000, NULL, 'Los Angeles', 'USA'),
(8, 'Frank', 'Thomas', 'Male', 'IT', 'Data Analyst', '2020-02-15', 72000, 3, 'New York', 'USA'),
(9, 'Grace', 'Miller', 'Female', 'HR', 'HR Associate', '2018-08-22', 55000, 2, 'San Francisco', 'USA'),
(10, 'Henry', 'Wilson', 'Male', 'IT', 'Software Engineer', '2021-06-30', 75000, 3, 'New York', 'USA');
```
### **Module Breakdown**

#### **1. Introduction to SQL and Database Basics**

- **SQL Overview**: Structured Query Language (SQL) is the standard language for managing and manipulating databases.
- **Relational Database Concepts**: Learn about tables, columns, rows, and relationships.
- **Data Types**: Numeric, String, Date/Time, Binary, and others.
- **Basic SQL Operations**:
  - `SELECT`
  - `INSERT`
  - `UPDATE`
  - `DELETE`
    
#### **2. Data Querying Techniques**

- **Simple Queries**:
  - Retrieve data from a table with `SELECT`.
    ```sql
    SELECT * FROM employees;
    ```
- **Filtering Data** with `WHERE`:
    ```sql
    SELECT * FROM employees
    WHERE department = 'HR';
    ```
- **Sorting Results** using `ORDER BY`:
    ```sql
    SELECT * FROM employees
    ORDER BY salary DESC;
    ```
- **Limiting Rows** with `LIMIT`:
    ```sql
    SELECT * FROM employees
    LIMIT 5;
    ```

#### **3. Aggregate Functions**

- **Count**:
    ```sql
    SELECT COUNT(*) FROM employees;
    ```
- **Sum**:
    ```sql
    SELECT SUM(salary) FROM employees;
    ```
- **Average**:
    ```sql
    SELECT AVG(salary) FROM employees;
    ```
- **Group By**:
    ```sql
    SELECT department, COUNT(*) AS num_employees
    FROM employees
    GROUP BY department;
    ```

#### **4. Advanced SQL Queries**

- **Joins**: Combining data from multiple tables using `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and `FULL JOIN`.
    - **INNER JOIN**: Retrieves records that have matching values in both tables.
    ```sql
    SELECT employees.name, departments.name
    FROM employees
    INNER JOIN departments ON employees.department_id = departments.id;
    ```
    - **LEFT JOIN**: Retrieves all records from the left table, and matched records from the right table.
    ```sql
    SELECT employees.name, departments.name
    FROM employees
    LEFT JOIN departments ON employees.department_id = departments.id;
    ```
    - **RIGHT JOIN**: Retrieves all records from the right table, and matched records from the left table.
    ```sql
    SELECT employees.name, departments.name
    FROM employees
    RIGHT JOIN departments ON employees.department_id = departments.id;
    ```

#### **5. Subqueries**

- **Subquery Example**:
    ```sql
    SELECT name, salary
    FROM employees
    WHERE department_id = (SELECT id FROM departments WHERE name = 'HR');
    ```
- **Correlated Subquery**:
    ```sql
    SELECT name, salary
    FROM employees e
    WHERE salary > (SELECT AVG(salary) FROM employees WHERE department_id = e.department_id);
    ```

#### **6. Data Modifications**

- **INSERT INTO**: Adding new records.
    ```sql
    INSERT INTO employees (name, department, salary)
    VALUES ('John Doe', 'Finance', 75000);
    ```
- **UPDATE**: Modifying existing records.
    ```sql
    UPDATE employees
    SET salary = salary * 1.05
    WHERE department = 'IT';
    ```
- **DELETE**: Removing records.
    ```sql
    DELETE FROM employees
    WHERE name = 'John Doe';
    ```

#### **7. Transactions and ACID Properties**

- **Begin Transaction**:
    ```sql
    BEGIN TRANSACTION;
    ```
- **COMMIT**: Save changes.
    ```sql
    COMMIT;
    ```
- **ROLLBACK**: Revert changes in case of an error.
    ```sql
    ROLLBACK;
    ```

- **ACID Properties**:
    - **Atomicity**: All or nothing.
    - **Consistency**: Ensuring data integrity.
    - **Isolation**: Transactions don't interfere with each other.
    - **Durability**: Changes are permanent once committed.

#### **8. Indexing and Query Optimization**

- **Index Creation**:
    ```sql
    CREATE INDEX idx_employees_salary ON employees(salary);
    ```
- **Examining Query Plans**: Use `EXPLAIN` to analyze the execution plan.
    ```sql
    EXPLAIN SELECT * FROM employees WHERE salary > 50000;
    ```

#### **9. Complex Data Types and Stored Procedures**

- **Working with Complex Data Types** (e.g., Arrays, JSON, XML):
    ```sql
    SELECT json_column->>'name' FROM employees WHERE json_column IS NOT NULL;
    ```
- **Stored Procedures**:
    - **Creating a Stored Procedure**:
    ```sql
    DELIMITER //
    CREATE PROCEDURE UpdateEmployeeSalary(IN emp_id INT, IN new_salary DECIMAL)
    BEGIN
        UPDATE employees SET salary = new_salary WHERE id = emp_id;
    END //
    DELIMITER ;
    ```
    - **Calling a Stored Procedure**:
    ```sql
    CALL UpdateEmployeeSalary(1, 80000);
    ```

#### **10. Data Security and Permissions**

- **User Creation**:
    ```sql
    CREATE USER 'new_user'@'localhost' IDENTIFIED BY 'password';
    ```
- **Granting Permissions**:
    ```sql
    GRANT SELECT, INSERT ON employees TO 'new_user'@'localhost';
    ```

#### **11. SQL Functions**

- **String Functions**:
    ```sql
    SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees;
    ```
- **Date Functions**:
    ```sql
    SELECT CURDATE(), YEAR(hire_date) FROM employees;
    ```

---

### **Example Database Schema**

Here's a simplified schema for the training examples:

```sql
-- Create table for departments
CREATE TABLE departments (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create table for employees
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INT,
    salary DECIMAL(10, 2),
    hire_date DATE,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

### **YouTube Video Recommendations**

To supplement the theory, here is a **highly recommended YouTube video** for SQL:

- **[SQL Full Course – Learn SQL in 8 Hours | SQL Tutorial | SQL For Beginners | Edureka](https://www.youtube.com/watch?v=HXV3zeQKqGY)**

This video is comprehensive, covering both beginner and intermediate SQL topics, making it suitable for trainees to visualize the concepts they’ve learned.

---

### **Assessment and Practice**

At the end of this module, trainees should complete a project where they:

1. Create a database schema.
2. Populate it with sample data.
3. Perform complex queries, joins, subqueries, and optimizations.
4. Write stored procedures to handle common tasks like salary updates and department changes.
5. Implement data security features like user roles and permissions.

**Example Project Idea**: Create a system to manage an employee database for a company. Implement features such as salary increments, employee department changes, and a report generation tool to analyze employee data by various parameters (e.g., department, hire date, etc.).

---

By following this module, trainees will gain industry-relevant SQL skills that will help them work with databases in real-world scenarios.
