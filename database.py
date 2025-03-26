import psycopg2 
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def save_to_database(session_id, dependencies, selected_dependencies, beliefs, desires, intentions):
    """Save session data to PostgreSQL."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history (session_id, dependencies, selected_dependencies, beliefs, desires, intentions)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (session_id, json.dumps(dependencies), json.dumps(selected_dependencies), 
         json.dumps(beliefs), json.dumps(desires), json.dumps(intentions))
    )

    conn.commit()
    cursor.close()
    conn.close()

def load_from_database(limit=5):
    """Load chat history from PostgreSQL."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT %s", (limit,))
    history = cursor.fetchall()

    cursor.close()
    conn.close()
    return history
