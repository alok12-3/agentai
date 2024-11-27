import sqlite3
import os
import random
from datetime import datetime, timedelta

# Set database path in the current folder
current_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_dir, "datafile.db")

# Connect to the SQLite database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        transaction_date TEXT,
        amount REAL,
        product_category TEXT
    )
""")

# Generate random data for the table
def generate_random_data(num_records=1000):
    product_categories = ["Electronics", "Clothing", "Home Goods", "Books", "Sports", "Toys"]
    
    # Loop to create random records
    for _ in range(num_records):
        customer_id = random.randint(1, 100)  # Random customer ID between 1 and 100
        transaction_date = datetime.now() - timedelta(days=random.randint(0, 365))  # Random date within the last year
        amount = round(random.uniform(5.0, 500.0), 2)  # Random amount between $5 and $500
        product_category = random.choice(product_categories)  # Random category

        # Insert data into the table
        cursor.execute("""
            INSERT INTO transactions (customer_id, transaction_date, amount, product_category)
            VALUES (?, ?, ?, ?)
        """, (customer_id, transaction_date.strftime('%Y-%m-%d %H:%M:%S'), amount, product_category))

    # Commit the transactions
    conn.commit()
    print(f"{num_records} records inserted into the 'transactions' table.")

# Generate 1000 records
generate_random_data(1000)

# Close the database connection
conn.close()
print(f"Sample dataset created in '{database_path}'.")
