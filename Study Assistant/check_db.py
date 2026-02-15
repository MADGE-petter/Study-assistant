import sqlite3
from datetime import datetime

DATABASE_NAME = "study_assistant.db"


def check_reminders_in_db():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Connecting to database: {DATABASE_NAME}"
        )

        cursor.execute(
            "SELECT id, title, description, reminder_time, is_active, created_at FROM reminders ORDER BY reminder_time ASC"
        )
        reminders = cursor.fetchall()

        if not reminders:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] No reminders found in the database."
            )
            return

        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Found {len(reminders)} reminder(s) in the database:"
        )
        for r_id, title, desc, r_time, is_active, created_at in reminders:
            status = "Active" if is_active else "Inactive"
            print(
                f"  ID: {r_id}, Title: {title}, Time: {r_time}, Status: {status}, Created: {created_at}"
            )

    except sqlite3.Error as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Database error: {e}")
    finally:
        if conn:
            conn.close()
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Database connection closed."
            )


if __name__ == "__main__":
    check_reminders_in_db()
