import os
import sqlite3


def connect_to_db(database_name='upwork_jobs.db'):
    # Get the full path to the database file
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    parent_dir = os.path.dirname(current_dir)  # Get the parent directory
    database_path = os.path.join(parent_dir, database_name)
    # Connect to database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    return conn, cursor


def create_db(conn, cursor):
    # Create the `jobs` table (if it doesn't exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            job_url TEXT,
            job_title TEXT NOT NULL,
            posted_date DATETIME,
            job_description TEXT NOT NULL,
            job_tags TEXT,
            job_proposals TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()


def get_all_jobs(cursor):
    """Fetch all jobs from the database"""
    cursor.execute('SELECT * FROM jobs')
    return cursor.fetchall()


def get_job_by_id(cursor, job_id):
    """Fetch a specific job by its job_id"""
    cursor.execute('SELECT * FROM jobs WHERE job_id = ?', (job_id,))
    return cursor.fetchone()


def search_jobs_by_title(cursor, keyword):
    """Search jobs by title containing a keyword"""
    cursor.execute('SELECT * FROM jobs WHERE job_title LIKE ?', (f'%{keyword}%',))
    return cursor.fetchall()


def get_recent_jobs(cursor, limit=10):
    """Get the most recent jobs based on posted_date"""
    cursor.execute('SELECT * FROM jobs ORDER BY posted_date DESC LIMIT ?', (limit,))
    return cursor.fetchall()


def clear_database(conn, cursor):
    """Clear all records from the jobs table"""
    try:
        cursor.execute('DELETE FROM jobs')
        conn.commit()
        return True
    except Exception as e:
        print(f"Error clearing database: {e}")
        return False

