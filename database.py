# import mysql.connector

# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="@1712Shrutidg6",
#     database="energy_db"
# )

# cursor = conn.cursor()

# def save_record(hour, prediction):
#     query = "INSERT INTO history (hour, prediction) VALUES (%s, %s)"
#     cursor.execute(query, (hour, prediction))
#     conn.commit()

# import mysql.connector
# import os

# def get_connection():
#     return mysql.connector.connect(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         database=os.getenv("DB_NAME"),
#         port=int(os.getenv("DB_PORT"))
#     )

# def save_record(hour, prediction):
#     conn = get_connection()
#     cursor = conn.cursor()

#     query = "INSERT INTO history (hour, prediction) VALUES (%s, %s)"
#     cursor.execute(query, (hour, prediction))

#     conn.commit()
#     cursor.close()
#     conn.close()

# import mysql.connector
# import os

# def get_connection():
#     return mysql.connector.connect(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         database=os.getenv("DB_NAME"),
#         port=int(os.getenv("DB_PORT"))
#     )

# def create_table():
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS history (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             hour INT,
#             prediction FLOAT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     """)

#     conn.commit()
#     cursor.close()
#     conn.close()

# def save_record(hour, prediction):
#     conn = get_connection()
#     cursor = conn.cursor()

#     query = "INSERT INTO history (hour, prediction) VALUES (%s, %s)"
#     cursor.execute(query, (hour, prediction))

#     conn.commit()
#     cursor.close()
#     conn.close()

# import os

# print("DB_PORT raw:", os.getenv("DB_PORT"))

'''
import mysql.connector
import os
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env
# ----------------------------
# Utility to safely get DB_PORT
# ----------------------------
def get_db_port():
    # db_port_str = os.getenv("DB_PORT", "3306")  # default to 3306
    # try:
    #     return int(db_port_str)
    # except (TypeError, ValueError):
    #     raise ValueError(f"Invalid DB_PORT: {db_port_str}. Must be a numeric port.")
    db_port_str = os.getenv("DB_PORT", "3306")
    try:
        return int(db_port_str)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid DB_PORT: {db_port_str}. Must be a numeric port.")

# ----------------------------
# Create a new DB connection
# ----------------------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "energy_db"),
        port=get_db_port()
    )

# ----------------------------
# Create table if it doesn't exist
# ----------------------------
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            hour INT,
            prediction FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# ----------------------------
# Save a prediction record
# ----------------------------
def save_record(hour, prediction):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO history (hour, prediction) VALUES (%s, %s)"
    cursor.execute(query, (hour, prediction))
    conn.commit()
    cursor.close()
    conn.close()

# ----------------------------
# Debug: print DB_PORT value
# ----------------------------
print("DB_PORT raw:", os.getenv("DB_PORT"))
print("DB_PORT used:", get_db_port()) '''

import mysql.connector
import os

# Try loading .env locally (will NOT crash on Railway)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# ----------------------------
# Get DB Port safely
# ----------------------------
def get_db_port():
    db_port = os.getenv("DB_PORT")

    # Railway sometimes gives invalid values like "MYSQLPORT"
    if not db_port or not db_port.isdigit():
        return 3306  # safe default

    return int(db_port)

# ----------------------------
# Create DB connection
# ----------------------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=get_db_port()
    )

# ----------------------------
# Create table if not exists
# ----------------------------
def create_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hour INT,
                prediction FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ Table ready")

    except Exception as e:
        print("❌ Error creating table:", e)

# ----------------------------
# Save record
# ----------------------------
def save_record(hour, prediction):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "INSERT INTO history (hour, prediction) VALUES (%s, %s)"
        cursor.execute(query, (hour, prediction))

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ Record saved")

    except Exception as e:
        print("❌ Error saving record:", e)