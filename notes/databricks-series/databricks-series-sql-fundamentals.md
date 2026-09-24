---
title: "DataBricks Series - SQL Fundamentals"
date: 2025-11-18
source: https://www.musfirajamil.com/blog/databricks-series-sql-fundamentals
---

# DataBricks Series - SQL Fundamentals

_The core SQL patterns worth mastering first, filtering, aggregation, joins, CTEs, window functions, and indexing, with runnable examples against a students table._

SQL (Structured Query Language) is a standardized programming language used to manage, query, and manipulate relational databases. It allows users to retrieve, update, insert, and delete data efficiently.

If you're learning SQL, I'd recommend focusing on the following topics:

* SELECT + WHERE + JOIN (most used)
* GROUP BY + HAVING (summarizing data)
* ORDER BY + LIMIT (controlling results)
* CTEs + Subqueries (for complex logic)
* Window Functions (advanced analytics)
* Indexes (for performance tuning)

We will focus on the most-used concepts, which upon mastery will allow you to accomplish 80% of typical query tasks.

1. **Basic Querying (SELECT, FROM, WHERE)**

Let's assume we are tasked with loading data from a students table for students who have achieved grades > 85.

```
SELECT *
FROM students
WHERE grade >= 85;
```

In this query, `SELECT *` tells the SQL engine to load all available columns in the table students and apply the filter to the grade column.

2. **Filtering Data (WHERE, AND, OR, IN, LIKE, BETWEEN)**

```
SELECT * FROM students
WHERE grade BETWEEN 80 AND 90
AND department IN ('Computer Science', 'Math');
```

3. **Sorting and Limiting Results (ORDER BY, LIMIT)**

```
SELECT * FROM students
ORDER BY grade DESC
LIMIT 10;
```

4. **Aggregation (COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING)**

```
SELECT department, AVG(grade) AS avg_grade
FROM students
GROUP BY department
HAVING AVG(grade) > 80;
```

Here we can replace AVG with any of the following:

* COUNT (count rows)
* SUM (total sum of values)
* AVG (average value)
* MIN/MAX (smallest/largest value)
* GROUP BY (aggregates by category)
* HAVING (filters aggregated results)

### 5. Joins (INNER, LEFT, RIGHT, FULL)

```
SELECT s.first_name, s.last_name, c.course_name
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id;
```

6. **Subqueries (Nested Queries)**

```
SELECT first_name, last_name
FROM students
WHERE student_id IN (
 SELECT student_id FROM enrollments WHERE course_id = 101
);
```

7. **Common Table Expressions (CTEs)**

```
WITH top_students AS (
 SELECT student_id, grade FROM students WHERE grade > 90
)
SELECT s.first_name, s.last_name, t.grade
FROM top_students t
JOIN students s ON s.student_id = t.student_id;
```

`WITH` defines temporary query results.

8. **Window Functions (OVER, PARTITION BY)**

```
SELECT student_id, grade,
 RANK() OVER (PARTITION BY course_id ORDER BY grade DESC) AS rank
FROM enrollments;
```

Concepts to know:

* OVER (defines how results are computed)
* PARTITION BY (grouping for window calculations)
* RANK(), DENSE\_RANK(), ROW\_NUMBER() (ranking functions)

9. **Updating Data (INSERT, UPDATE, DELETE)**

```
UPDATE students
SET grade = 95
WHERE student_id = 101;

INSERT INTO students (first_name, last_name, grade)
VALUES ('John', 'Doe', 88);

DELETE FROM students WHERE grade < 50;
```

Extensions that are super important to know:

* INSERT INTO (adds new records)
* UPDATE (modifies existing records)
* DELETE (removes records)

Note: Always use WHERE with **UPDATE** and **DELETE** to prevent accidental changes!

10. **Indexing for Performance (INDEX, EXPLAIN)**

```
CREATE INDEX idx_students ON students (last_name);
```

**Concepts to know:**

* CREATE INDEX (speeds up searches)
* EXPLAIN (analyzes query execution plan)
