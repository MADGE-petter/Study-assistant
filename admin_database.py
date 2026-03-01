#!/usr/bin/env python3
"""
Admin Database Manager
Separate database for admin operations
"""

import sqlite3
import os
from datetime import datetime


class AdminDatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), 'admin_data.db')
        self.init_database()
    
    def init_database(self):
        """Initialize admin database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Admin users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                role VARCHAR(20) DEFAULT 'admin',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Admin logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER,
                action VARCHAR(100) NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(45),
                FOREIGN KEY (admin_id) REFERENCES admin_users (id)
            )
        ''')
        
        # System settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_by INTEGER,
                FOREIGN KEY (updated_by) REFERENCES admin_users (id)
            )
        ''')
        
        # Data backups table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                backup_name VARCHAR(255) NOT NULL,
                backup_path VARCHAR(500),
                backup_size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER,
                backup_type VARCHAR(50) DEFAULT 'manual',
                FOREIGN KEY (created_by) REFERENCES admin_users (id)
            )
        ''')
        
        # User activity monitoring
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id VARCHAR(100),
                activity_type VARCHAR(50),
                activity_details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_duration INTEGER
            )
        ''')
        
        # System performance metrics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name VARCHAR(100),
                metric_value REAL,
                metric_unit VARCHAR(20),
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def log_admin_action(self, admin_id, action, details=None, ip_address=None):
        """Log admin action"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO admin_logs (admin_id, action, details, ip_address)
            VALUES (?, ?, ?, ?)
        ''', (admin_id, action, details, ip_address))
        conn.commit()
        conn.close()
    
    def get_admin_logs(self, limit=100):
        """Get admin logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT al.id, au.username, al.action, al.details, al.timestamp, al.ip_address
            FROM admin_logs al
            LEFT JOIN admin_users au ON al.admin_id = au.id
            ORDER BY al.timestamp DESC
            LIMIT ?
        ''', (limit,))
        logs = cursor.fetchall()
        conn.close()
        return logs
    
    def get_system_stats(self):
        """Get system statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total admin users
        cursor.execute("SELECT COUNT(*) FROM admin_users WHERE is_active = 1")
        stats['admin_users'] = cursor.fetchone()[0]
        
        # Total logs today
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) FROM admin_logs WHERE DATE(timestamp) = ?", (today,))
        stats['logs_today'] = cursor.fetchone()[0]
        
        # Total backups
        cursor.execute("SELECT COUNT(*) FROM data_backups")
        stats['total_backups'] = cursor.fetchone()[0]
        
        # Recent user activities
        cursor.execute("SELECT COUNT(*) FROM user_activity WHERE DATE(timestamp) = ?", (today,))
        stats['user_activities_today'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def create_default_admin(self):
        """Create default admin user if not exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM admin_users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            # Default password: admin123
            cursor.execute('''
                INSERT INTO admin_users (username, password_hash, email, role)
                VALUES (?, ?, ?, ?)
            ''', ('admin', 'pbkdf2:sha256:260000$salt$hash', 'admin@studyassistant.com', 'super_admin'))
            conn.commit()
        
        conn.close()
    
    def get_user_activity_summary(self):
        """Get user activity summary"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Last 7 days activity
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as activities
            FROM user_activity
            WHERE timestamp >= datetime('now', '-7 days')
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''')
        activity_data = cursor.fetchall()
        
        conn.close()
        return activity_data
    
    def backup_main_database(self, main_db_path):
        """Backup the main study assistant database"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"study_assistant_backup_{timestamp}.db"
            backup_path = os.path.join(os.path.dirname(self.db_path), backup_name)
            
            # Copy the database
            main_conn = sqlite3.connect(main_db_path)
            backup_conn = sqlite3.connect(backup_path)
            main_conn.backup(backup_conn)
            main_conn.close()
            backup_conn.close()
            
            # Log the backup
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO data_backups (backup_name, backup_path, backup_size, created_by)
                VALUES (?, ?, ?, ?)
            ''', (backup_name, backup_path, os.path.getsize(backup_path), 1))
            conn.commit()
            conn.close()
            
            return backup_path
        except Exception as e:
            print(f"Backup failed: {e}")
            return None


# Initialize admin database
if __name__ == "__main__":
    admin_db = AdminDatabaseManager()
    admin_db.create_default_admin()
    print("Admin database initialized successfully!")
