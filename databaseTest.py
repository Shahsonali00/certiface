import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "pass",
    "database": "face_recognition"
}



try:
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass",
    database="face_recognition",
    port=3306,  # Add this line if your MySQL is running on a different port
    connection_timeout=10
)
    print("Connection attempted...")

    if connection.is_connected():
        print("Connected to MySQL database successfully!")
    else:
        print("Failed to connect to MySQL database.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
except Exception as ex:
    print(f"Unexpected error: {ex}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("MySQL connection is closed.")