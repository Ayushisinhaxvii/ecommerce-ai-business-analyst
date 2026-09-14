# Import SQLite so we can query our business database
import sqlite3

# Import pandas so we can work with SQL results
import pandas as pd

# Import regular expressions for extracting years
import re

# Import the database path from our configuration
from src.config import DATABASE_PATH


# Define the SQL queries used by our business analyst
SQL_QUERIES = {

    # Count all orders
    "total_orders": """
        SELECT COUNT(*) AS total_orders
        FROM orders;
    """,

    # Count unique customers
    "total_customers": """
        SELECT COUNT(DISTINCT customer_unique_id) AS total_customers
        FROM customers;
    """,

    # Calculate total product sales for delivered orders
    "total_sales": """
        SELECT
            ROUND(SUM(oi.price), 2) AS total_sales
        FROM order_items AS oi
        INNER JOIN orders AS o
            ON oi.order_id = o.order_id
        WHERE o.order_status = 'delivered';
    """,

    # Calculate average order value for delivered orders
    "average_order_value": """
        SELECT
            ROUND(
                SUM(oi.price) / COUNT(DISTINCT oi.order_id),
                2
            ) AS average_order_value
        FROM order_items AS oi
        INNER JOIN orders AS o
            ON oi.order_id = o.order_id
        WHERE o.order_status = 'delivered';
    """,

    # Calculate average delivery time
    "average_delivery_days": """
        SELECT
            ROUND(
                AVG(
                    julianday(order_delivered_customer_date)
                    - julianday(order_purchase_timestamp)
                ),
                2
            ) AS average_delivery_days
        FROM orders
        WHERE order_status = 'delivered'
          AND order_delivered_customer_date IS NOT NULL;
    """,

    # Calculate late delivery rate
    "late_delivery_rate": """
        SELECT
            ROUND(
                100.0 * SUM(
                    CASE
                        WHEN order_delivered_customer_date
                             > order_estimated_delivery_date
                        THEN 1
                        ELSE 0
                    END
                ) / COUNT(*),
                2
            ) AS late_delivery_rate
        FROM orders
        WHERE order_status = 'delivered'
          AND order_delivered_customer_date IS NOT NULL;
    """,

    # Calculate average review score
    "average_review_score": """
        SELECT
            ROUND(AVG(review_score), 2) AS average_review_score
        FROM reviews
        WHERE review_score IS NOT NULL;
    """,

    # Calculate cancellation rate
    "cancellation_rate": """
        SELECT
            ROUND(
                100.0 * SUM(
                    CASE
                        WHEN order_status = 'canceled'
                        THEN 1
                        ELSE 0
                    END
                ) / COUNT(*),
                2
            ) AS cancellation_rate
        FROM orders;
    """
}


# Define phrases that identify each SQL business question
SQL_INTENTS = {

    # Identify total-order questions
    "total_orders": [
        "total orders",
        "number of orders",
        "how many orders",
        "order count"
    ],

    # Identify customer-count questions
    "total_customers": [
        "total customers",
        "number of customers",
        "how many customers",
        "customer count"
    ],

    # Identify sales questions
    "total_sales": [
        "total sales",
        "sales",
        "product sales",
        "sales amount"
    ],

    # Identify AOV questions
    "average_order_value": [
        "average order value",
        "aov",
        "average order"
    ],

    # Identify delivery-time questions
    "average_delivery_days": [
        "average delivery time",
        "average delivery days",
        "how long does delivery take"
    ],

    # Identify late-delivery questions
    "late_delivery_rate": [
        "late delivery rate",
        "percentage of late orders",
        "late orders percentage"
    ],

    # Identify review-score questions
    "average_review_score": [
        "average review score",
        "average rating",
        "customer rating"
    ],

    # Identify cancellation questions
    "cancellation_rate": [
        "cancellation rate",
        "cancelled orders percentage",
        "canceled orders percentage"
    ]
}


# Detect which SQL business metric the user is asking about
def detect_sql_intent(question):

    # Convert the question to lowercase
    question_lower = question.lower()

    # Check every business intent
    for intent, phrases in SQL_INTENTS.items():

        # Check every phrase belonging to that intent
        for phrase in phrases:

            # Return the intent when a phrase matches
            if phrase in question_lower:
                return intent

    # Return None when no SQL intent matches
    return None


# Extract a year such as 2018 from the user's question
def extract_year(question):

    # Search for a four-digit year beginning with 20
    match = re.search(r"\b(20\d{2})\b", question)

    # Return the year if one was found
    if match:
        return int(match.group(1))

    # Return None when no year was found
    return None


# Add a year filter to a SQL query when needed
def add_year_filter(query, year):

    # Do nothing if the user did not specify a year
    if year is None:
        return query

    # Add the year condition before the final semicolon
    query = query.rstrip().rstrip(";")

    # Add a purchase-year filter
    query += f"""
        AND strftime('%Y', order_purchase_timestamp)
            = '{year}'
    """

    # Return the modified query
    return query


# Build the correct SQL query for an intent
def build_sql_query(intent, year=None):

    # Get the base query
    query = SQL_QUERIES[intent]

    # Handle year-specific sales
    if intent == "total_sales" and year is not None:

        query = """
            SELECT
                ROUND(SUM(oi.price), 2) AS total_sales
            FROM order_items AS oi
            INNER JOIN orders AS o
                ON oi.order_id = o.order_id
            WHERE o.order_status = 'delivered'
              AND strftime('%Y', o.order_purchase_timestamp)
                  = ?
        """

        return query, (str(year),)


    # Handle year-specific AOV
    if intent == "average_order_value" and year is not None:

        query = """
            SELECT
                ROUND(
                    SUM(oi.price) /
                    COUNT(DISTINCT oi.order_id),
                    2
                ) AS average_order_value
            FROM order_items AS oi
            INNER JOIN orders AS o
                ON oi.order_id = o.order_id
            WHERE o.order_status = 'delivered'
              AND strftime('%Y', o.order_purchase_timestamp)
                  = ?
        """

        return query, (str(year),)


    # Handle year-specific total orders
    if intent == "total_orders" and year is not None:

        query = """
            SELECT COUNT(*) AS total_orders
            FROM orders
            WHERE strftime('%Y', order_purchase_timestamp) = ?
        """

        return query, (str(year),)


    # Handle year-specific customer count
    if intent == "total_customers" and year is not None:

        query = """
            SELECT COUNT(DISTINCT c.customer_unique_id)
                AS total_customers
            FROM customers AS c
            INNER JOIN orders AS o
                ON c.customer_id = o.customer_id
            WHERE strftime('%Y', o.order_purchase_timestamp) = ?
        """

        return query, (str(year),)


    # Handle year-specific average delivery time
    if intent == "average_delivery_days" and year is not None:

        query = """
            SELECT
                ROUND(
                    AVG(
                        julianday(order_delivered_customer_date)
                        - julianday(order_purchase_timestamp)
                    ),
                    2
                ) AS average_delivery_days
            FROM orders
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NOT NULL
              AND strftime('%Y', order_purchase_timestamp) = ?
        """

        return query, (str(year),)


    # Handle year-specific late delivery rate
    if intent == "late_delivery_rate" and year is not None:

        query = """
            SELECT
                ROUND(
                    100.0 * SUM(
                        CASE
                            WHEN order_delivered_customer_date
                                 > order_estimated_delivery_date
                            THEN 1
                            ELSE 0
                        END
                    ) / COUNT(*),
                    2
                ) AS late_delivery_rate
            FROM orders
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NOT NULL
              AND strftime('%Y', order_purchase_timestamp) = ?
        """

        return query, (str(year),)


    # Handle year-specific average review score
    if intent == "average_review_score" and year is not None:

        query = """
            SELECT
                ROUND(AVG(r.review_score), 2)
                    AS average_review_score
            FROM reviews AS r
            INNER JOIN orders AS o
                ON r.order_id = o.order_id
            WHERE r.review_score IS NOT NULL
              AND strftime('%Y', o.order_purchase_timestamp) = ?
        """

        return query, (str(year),)


    # Handle year-specific cancellation rate
    if intent == "cancellation_rate" and year is not None:

        query = """
            SELECT
                ROUND(
                    100.0 * SUM(
                        CASE
                            WHEN order_status = 'canceled'
                            THEN 1
                            ELSE 0
                        END
                    ) / COUNT(*),
                    2
                ) AS cancellation_rate
            FROM orders
            WHERE strftime('%Y', order_purchase_timestamp) = ?
        """

        return query, (str(year),)


    # Return the normal query when no year is specified
    return query, ()


# Execute a SQL query against our SQLite database
def run_sql_query(sql_query, parameters=()):

    # Open a database connection
    connection = sqlite3.connect(DATABASE_PATH)

    try:

        # Execute the query and return the result
        result = pd.read_sql_query(
            sql_query,
            connection,
            params=parameters
        )

        return result

    finally:

        # Always close the database connection
        connection.close()


# Answer a business question using our approved SQL queries
def answer_sql_question(question):

    # Detect the business intent
    intent = detect_sql_intent(question)

    # Stop if no SQL intent was found
    if intent is None:
        return {
            "intent": None,
            "year": None,
            "sql": None,
            "result": pd.DataFrame()
        }

    # Extract a year if the user mentioned one
    year = extract_year(question)

    # Build the appropriate SQL query
    sql_query, parameters = build_sql_query(
        intent,
        year
    )

    # Execute the query
    result = run_sql_query(
        sql_query,
        parameters
    )

    # Return all useful information
    return {
        "intent": intent,
        "year": year,
        "sql": sql_query,
        "result": result
    }