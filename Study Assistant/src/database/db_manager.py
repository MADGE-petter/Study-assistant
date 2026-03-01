import hashlib  # For password hashing
import sqlite3
from datetime import datetime

DATABASE_NAME = "study_assistant.db"


class DatabaseManager:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        if self.conn:
            self.create_tables()
        else:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DBManager: Connection failed, tables not created."
            )

    def connect(self):
        self.conn = None  # Reset connection on each attempt
        self.cursor = None  # Reset cursor on each attempt
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error connecting to database {self.db_name}: {e}"
            )
            self.conn = None
            self.cursor = None

    def close(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Create database tables"""
        if not self.cursor:
            print("DBManager: Cursor not available, cannot create tables.")
            return

        # Create settings table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

        # Create notes table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Create tasks table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                priority INTEGER DEFAULT 0,
                is_completed INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                completed_at TEXT
            )
        """)

        # Create reminders table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                reminder_time TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)

        # Create note_summaries table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS note_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                note_title TEXT NOT NULL,
                original_content TEXT NOT NULL,
                summary_content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (note_id) REFERENCES notes (id)
            )
        """)
        if self.conn:
            self.conn.commit()

    # --- Settings operations (for password and other configurations) ---
    def set_setting(self, key, value):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot set setting.")
            return
        self.cursor.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value),
        )
        if self.conn:
            self.conn.commit()

    def get_setting(self, key):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot get setting.")
            return None
        self.cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def set_admin_password(self, password):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot set admin password.")
            return
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.set_setting("admin_password_hash", hashed_password)

    def get_admin_password_hash(self):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot get admin password hash.")
            return None
        return self.get_setting("admin_password_hash")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # --- Notes CRUD operations ---
    def add_note(self, title, content, created_at, updated_at):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot add note.")
            return None
        self.cursor.execute(
            "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, content, created_at, updated_at),
        )
        if self.conn:
            self.conn.commit()
        return self.cursor.lastrowid

    def get_all_notes(self):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot get notes.")
            return []
        self.cursor.execute(
            "SELECT id, title, content, created_at, updated_at FROM notes ORDER BY updated_at DESC"
        )
        return self.cursor.fetchall()

    def get_note_by_id(self, note_id):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot get note.")
            return None
        self.cursor.execute(
            "SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?",
            (note_id,),
        )
        return self.cursor.fetchone()

    def update_note(self, note_id, title, content, updated_at):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot update note.")
            return
        self.cursor.execute(
            "UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?",
            (title, content, updated_at, note_id),
        )
        if self.conn:
            self.conn.commit()

    def delete_note(self, note_id):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot delete note.")
            return
        self.cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        if self.conn:
            self.conn.commit()

    # --- Tasks CRUD operations ---
    def add_task(
        self,
        title,
        description,
        due_date,
        priority,
        is_completed,
        created_at,
        completed_at,
    ):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot add task.")
            return None
        self.cursor.execute(
            "INSERT INTO tasks (title, description, due_date, priority, is_completed, created_at, completed_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                title,
                description,
                due_date,
                priority,
                is_completed,
                created_at,
                completed_at,
            ),
        )
        if self.conn:
            self.conn.commit()
        return self.cursor.lastrowid

    def get_all_tasks(self):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot get tasks.")
            return []
        self.cursor.execute(
            "SELECT id, title, description, due_date, priority, is_completed, created_at, completed_at FROM tasks ORDER BY due_date ASC, priority DESC"
        )
        return self.cursor.fetchall()

    def get_task_by_id(self, task_id):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot get task.")
            return None
        self.cursor.execute(
            "SELECT id, title, description, due_date, priority, is_completed, created_at, completed_at FROM tasks WHERE id = ?",
            (task_id,),
        )
        return self.cursor.fetchone()

    def update_task(
        self,
        task_id,
        title,
        description,
        due_date,
        priority,
        is_completed,
        completed_at,
    ):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot update task.")
            return
        self.cursor.execute(
            "UPDATE tasks SET title = ?, description = ?, due_date = ?, priority = ?, is_completed = ?, completed_at = ? WHERE id = ?",
            (
                title,
                description,
                due_date,
                priority,
                is_completed,
                completed_at,
                task_id,
            ),
        )
        if self.conn:
            self.conn.commit()

    def delete_task(self, task_id):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot delete task.")
            return
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if self.conn:
            self.conn.commit()

    def get_upcoming_uncompleted_tasks(self, current_date_str):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot get upcoming tasks.")
            return []
        self.cursor.execute(
            "SELECT id, title, description, due_date, priority, is_completed, created_at, completed_at FROM tasks WHERE is_completed = 0 AND due_date >= ? ORDER BY due_date ASC, priority DESC",
            (current_date_str,),
        )
        return self.cursor.fetchall()

    # --- Study Sessions (Automated Tracking) ---
    def add_study_session(self, duration_seconds, mode="normal"):
        if not self.cursor:
            print("DBManager: Cursor not available, cannot add study session.")
            return
        session_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO study_sessions (session_date, duration_seconds, mode) VALUES (?, ?, ?)",
            (session_date, duration_seconds, mode),
        )
        if self.conn:
            self.conn.commit()

    def get_total_study_time(self):
        if not self.cursor:
            return 0
        self.cursor.execute("SELECT SUM(duration_seconds) FROM study_sessions")
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0

    def get_recent_study_sessions(self, limit=7):
        if not self.cursor:
            return []
        self.cursor.execute(
            "SELECT session_date, duration_seconds, mode FROM study_sessions ORDER BY session_date DESC LIMIT ?",
            (limit,)
        )
        return self.cursor.fetchall()

    def get_recent_notes(self, limit=5):
        if not self.cursor:
            return []
        self.cursor.execute(
            "SELECT id, title, content, created_at, updated_at FROM notes ORDER BY updated_at DESC LIMIT ?",
            (limit,)
        )
        return self.cursor.fetchall()

    def get_total_notes_count(self):
        if not self.cursor:
            return 0
        self.cursor.execute("SELECT COUNT(*) FROM notes")
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_total_tasks_count(self):
        if not self.cursor:
            return 0
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_completed_tasks_count(self):
        if not self.cursor:
            return 0
        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE is_completed = 1")
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_completed_tasks_by_date(self, date_str):
        if not self.cursor:
            return []
        self.cursor.execute(
            "SELECT id, title, description, due_date, is_completed, created_at, completed_at FROM tasks WHERE is_completed = 1 AND DATE(completed_at) = ?",
            (date_str,)
        )
        return self.cursor.fetchall()

    def get_tasks_by_date(self, date_str):
        """Get all tasks for a specific date"""
        if not self.cursor:
            return []
        self.cursor.execute(
            "SELECT id, title, description, due_date, is_completed, created_at, completed_at FROM tasks WHERE DATE(due_date) = ?",
            (date_str,)
        )
        return self.cursor.fetchall()

    def get_timer_statistics(self):
        if not self.cursor:
            return {}
        self.cursor.execute("SELECT COUNT(*) FROM study_sessions")
        count_result = self.cursor.fetchone()
        total_sessions = count_result[0] if count_result else 0
        
        self.cursor.execute("SELECT SUM(duration_seconds) FROM study_sessions")
        sum_result = self.cursor.fetchone()
        total_seconds = sum_result[0] if sum_result and sum_result[0] else 0
        total_minutes = total_seconds // 60 if total_seconds else 0
        
        return {
            'total_sessions': total_sessions,
            'total_minutes': total_minutes
        }

    def save_note_summary(self, note_id, note_title, original_content, summary_content, created_at):
        """Save a note summary to the database"""
        if not self.cursor:
            return None
        self.cursor.execute(
            "INSERT INTO note_summaries (note_id, note_title, original_content, summary_content, created_at) VALUES (?, ?, ?, ?, ?)",
            (note_id, note_title, original_content, summary_content, created_at)
        )
        if self.conn:
            self.conn.commit()
        return self.cursor.lastrowid

    def get_all_note_summaries(self):
        """Get all note summaries"""
        if not self.cursor:
            return []
        self.cursor.execute(
            "SELECT id, note_id, note_title, original_content, summary_content, created_at FROM note_summaries ORDER BY created_at DESC"
        )
        return self.cursor.fetchall()

    def get_note_summaries_by_note_id(self, note_id):
        """Get all summaries for a specific note"""
        if not self.cursor:
            return []
        self.cursor.execute(
            "SELECT id, note_id, note_title, original_content, summary_content, created_at FROM note_summaries WHERE note_id = ? ORDER BY created_at DESC",
            (note_id,)
        )
        return self.cursor.fetchall()

    def get_total_note_summaries_count(self):
        """Get total count of note summaries"""
        if not self.cursor:
            return 0
        self.cursor.execute("SELECT COUNT(*) FROM note_summaries")
        result = self.cursor.fetchone()
        return result[0] if result else 0


# Example usage (for testing)
if __name__ == "__main__":
    db_manager = DatabaseManager()
    print("Database and tables created successfully!")
    db_manager.close()
