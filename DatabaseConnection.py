import mysql.connector
from mysql.connector import Error
from flask import Flask

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            database="NCAA transfer portal helper"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

if get_db_connection() is not None:
    print("Database connection successful.")