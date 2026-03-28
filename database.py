import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@1712Shrutidg6",
        database="energy_db",
        port=3306
    )

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

def save_record(hour, prediction):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO history (hour, prediction) VALUES (%s, %s)"
    cursor.execute(query, (hour, prediction))

    conn.commit()
    cursor.close()
    conn.close()