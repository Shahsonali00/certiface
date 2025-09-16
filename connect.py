import mysql.connector

conn = mysql.connector.connect(
    user='root',
    password='pass',         # use the correct password
    host='localhost',
    database='face_recognition',
    port=3306
)

if conn.is_connected():
    print("✅ Connected to database successfully!")
else:
    print("❌ Connection failed.")