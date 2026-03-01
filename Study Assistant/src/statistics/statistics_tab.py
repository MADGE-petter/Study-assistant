from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QWidget, QScrollArea, QFrame, QTextEdit,
    QSizePolicy, QSpacerItem, QPushButton, QListWidget, QListWidgetItem,
    QDialog, QSplitter, QGridLayout, QTabWidget
)
from PyQt6.QtGui import QColor, QFont
from datetime import datetime


class SummaryDialog(QDialog):
    def __init__(self, parent=None, title="", content="", created_at=""):
        super().__init__(parent)
        self.setWindowTitle("Chi Tiết Tóm Tắt")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(f"<h3 style='color: #3498db;'>{title}</h3>")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Created at
        date_label = QLabel(f"<p style='color: #7f8c8d; font-size: 12px;'>Ngày tạo: {created_at}</p>")
        layout.addWidget(date_label)
        
        # Content
        content_text = QTextEdit()
        content_text.setPlainText(content)
        content_text.setReadOnly(True)
        content_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                color: #2c3e50;
            }
        """)
        layout.addWidget(content_text)
        
        # Close button
        close_button = QPushButton("Đóng")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)


class NoteDialog(QDialog):
    def __init__(self, parent=None, title="", content="", created_at="", updated_at=""):
        super().__init__(parent)
        self.setWindowTitle("Chi Tiết Ghi Chú")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(f"<h3 style='color: #27ae60;'>{title}</h3>")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Dates
        date_info = f"<p style='color: #7f8c8d; font-size: 12px;'>Ngày tạo: {created_at}"
        if updated_at and updated_at != created_at:
            date_info += f"<br>Cập nhật: {updated_at}"
        date_info += "</p>"
        date_label = QLabel(date_info)
        layout.addWidget(date_label)
        
        # Content
        content_text = QTextEdit()
        content_text.setPlainText(content)
        content_text.setReadOnly(True)
        content_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                color: #2c3e50;
            }
        """)
        layout.addWidget(content_text)
        
        # Close button
        close_button = QPushButton("Đóng")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)


class NoteDialog(QDialog):
    def __init__(self, parent=None, title="", content="", created_at="", updated_at=""):
        super().__init__(parent)
        self.setWindowTitle("Chi Tiết Ghi Chú")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(f"<h3 style='color: #27ae60;'>{title}</h3>")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Dates
        date_info = f"<p style='color: #7f8c8d; font-size: 12px;'>Ngày tạo: {created_at}"
        if updated_at and updated_at != created_at:
            date_info += f"<br>Cập nhật: {updated_at}"
        date_info += "</p>"
        date_label = QLabel(date_info)
        layout.addWidget(date_label)
        
        # Content
        content_text = QTextEdit()
        content_text.setPlainText(content)
        content_text.setReadOnly(True)
        content_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                color: #2c3e50;
            }
        """)
        layout.addWidget(content_text)
        
        # Close button
        close_button = QPushButton("Đóng")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)


class StatisticsTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.load_statistics()

    def init_ui(self):
        # Main layout - vertical split
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # Left column
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setSpacing(10)

        # Title for left column
        left_title = QLabel("📊 Thống Kê Tổng Quan")
        left_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: white;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(52,152,219,0.8), stop:1 rgba(41,128,185,0.8));
            border: none;
            border-radius: 6px;
            margin-bottom: 10px;
        """)
        left_layout.addWidget(left_title)

        # Time widget - positioned below title
        time_widget = self.create_stat_widget("", "Tổng Thời Gian", "00:00:00", "#e74c3c")
        left_layout.addWidget(time_widget)
        
        # Study session history section
        history_widget = self.create_history_widget()
        left_layout.addWidget(history_widget)
        
        # Tasks section with two separate lists
        tasks_widget = QWidget()
        tasks_layout = QVBoxLayout(tasks_widget)
        tasks_layout.setSpacing(10)
        
        # Title for tasks section
        tasks_title = QLabel("📋 Nhiệm Vụ")
        tasks_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: white;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(155,89,182,0.8), stop:1 rgba(142,68,173,0.8));
            border: none;
            border-radius: 6px;
            margin-bottom: 10px;
        """)
        tasks_layout.addWidget(tasks_title)
        
        # Completed tasks section
        completed_label = QLabel("✅ Nhiệm Vụ Đã Hoàn Thành")
        completed_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: white;
            padding: 8px;
            background: #27ae60;
            border: none;
            border-radius: 4px;
            margin-bottom: 5px;
        """)
        tasks_layout.addWidget(completed_label)
        
        self.completed_tasks_list = QListWidget()
        self.completed_tasks_list.setMaximumHeight(150)
        self.completed_tasks_list.setStyleSheet("""
            QListWidget {
                background: rgba(39,174,96,0.1);
                border: 1px solid #27ae60;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                color: white;
                padding: 8px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            QListWidget::item:hover {
                background: rgba(39,174,96,0.3);
            }
            QListWidget::item:selected {
                background: rgba(39,174,96,0.5);
            }
        """)
        tasks_layout.addWidget(self.completed_tasks_list)
        
        # Pending tasks section
        pending_label = QLabel("⏳ Nhiệm Vụ Chưa Hoàn Thành")
        pending_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: white;
            padding: 8px;
            background: #e67e22;
            border: none;
            border-radius: 4px;
            margin-bottom: 5px;
        """)
        tasks_layout.addWidget(pending_label)
        
        self.pending_tasks_list = QListWidget()
        self.pending_tasks_list.setMaximumHeight(150)
        self.pending_tasks_list.setStyleSheet("""
            QListWidget {
                background: rgba(230,126,34,0.1);
                border: 1px solid #e67e22;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                color: white;
                padding: 8px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            QListWidget::item:hover {
                background: rgba(230,126,34,0.3);
            }
            QListWidget::item:selected {
                background: rgba(230,126,34,0.5);
            }
        """)
        tasks_layout.addWidget(self.pending_tasks_list)
        
        left_layout.addWidget(tasks_widget)
        
        # Add stretch to push content to top
        left_layout.addStretch()

        # Right column
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setSpacing(10)

        # Title for right column
        right_title = QLabel("📋 Dữ Liệu Chi Tiết")
        right_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: white;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(155,89,182,0.8), stop:1 rgba(142,68,173,0.8));
            border: none;
            border-radius: 6px;
            margin-bottom: 10px;
        """)
        right_layout.addWidget(right_title)

        # Tab widget for detailed data
        self.detail_tabs = QTabWidget()
        self.detail_tabs.setMinimumHeight(300)  # Ensure minimum height
        self.detail_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #2c3e50;
                border-radius: 5px;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #34495e;
                color: white;
                padding: 6px 12px;
                margin-right: 2px;
                border: none;
                font-size: 12px;
                min-width: 80px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
            }
        """)

        # Summaries Tab
        summaries_tab = QWidget()
        summaries_layout = QVBoxLayout(summaries_tab)
        summaries_layout.setContentsMargins(8, 8, 8, 8)
        
        # Create summaries widget with beautiful style like history
        summaries_widget = QWidget()
        summaries_widget.setStyleSheet("""
            QWidget {
                background-color: #1f2d3a;
                border-radius: 12px;
            }
        """)
        summaries_widget_layout = QVBoxLayout(summaries_widget)
        summaries_widget_layout.setContentsMargins(8, 8, 8, 8)
        summaries_widget_layout.setSpacing(4)

        self.auto_summaries_list = QListWidget()
        self.auto_summaries_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: transparent;
                color: #3498db;
                padding: 8px;
                margin: 2px;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QListWidget::item:hover {
                color: #27ae60;
            }
        """)
        summaries_widget_layout.addWidget(self.auto_summaries_list)
        summaries_layout.addWidget(summaries_widget)

        # Notes Tab
        notes_tab = QWidget()
        notes_layout = QVBoxLayout(notes_tab)
        notes_layout.setContentsMargins(8, 8, 8, 8)
        
        # Create notes widget with beautiful style like history
        notes_widget = QWidget()
        notes_widget.setStyleSheet("""
            QWidget {
                background-color: #1f2d3a;
                border-radius: 12px;
            }
        """)
        notes_widget_layout = QVBoxLayout(notes_widget)
        notes_widget_layout.setContentsMargins(8, 8, 8, 8)
        notes_widget_layout.setSpacing(4)

        self.recent_notes_list = QListWidget()
        print(f"Created recent_notes_list with id: {id(self.recent_notes_list)}")
        self.recent_notes_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: transparent;
                color: #3498db;
                padding: 8px;
                margin: 2px;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QListWidget::item:hover {
                color: #27ae60;
            }
        """)
        notes_widget_layout.addWidget(self.recent_notes_list)
        notes_layout.addWidget(notes_widget)

        # Add tabs
        self.detail_tabs.addTab(summaries_tab, "📝 Tóm Tắt")
        self.detail_tabs.addTab(notes_tab, "📝 Ghi Chú")

        right_layout.addWidget(self.detail_tabs)

        # Refresh button at bottom of right column
        refresh_button = QPushButton("🔄 Làm Mới Dữ Liệu")
        refresh_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2980b9, stop:1 #1abc9c);
            }
            QPushButton:pressed {
                background: #1abc9c;
            }
        """)
        refresh_button.clicked.connect(self.force_refresh_all)
        right_layout.addWidget(refresh_button)

        # Add columns to main layout
        main_layout.addWidget(left_column)
        main_layout.addWidget(right_column)

        # Set column widths (50/50 - equal balance)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 2)

        self.setStyleSheet("""
            StatisticsTab {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
            }
        """)

    def create_stat_widget(self, icon, title, value, color):
        widget = QWidget()
        widget.setMinimumHeight(110)
        widget.setMaximumHeight(140)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        widget.setStyleSheet("""
            QWidget {
                background-color: #1f2d3a;
                border-radius: 12px;
            }
        """)

        # Title - green color
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #27ae60;
            font-size: 18px;
            font-weight: bold;
            background: transparent;
            border: none;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Value - light blue color
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: #3498db;
            font-size: 32px;
            font-weight: bold;
            background: transparent;
            border: none;
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return widget

    def create_history_widget(self):
        widget = QWidget()
        widget.setMinimumHeight(150)
        widget.setMaximumHeight(200)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        widget.setStyleSheet("""
            QWidget {
                background-color: #1f2d3a;
                border-radius: 12px;
            }
        """)

        # History list - like time widget style
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: transparent;
                color: #3498db;
                padding: 8px;
                margin: 2px;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QListWidget::item:hover {
                color: #27ae60;
            }
        """)
        
        layout.addWidget(self.history_list)

        return widget

    def force_refresh_all(self):
        """Force refresh all data including total time"""
        print("Force refreshing all data...")
        
        # Force database commit first
        try:
            self.db_manager.conn.commit()
            print("Database committed")
        except Exception as e:
            print(f"Error committing database: {e}")
        
        # Reload all statistics
        self.load_statistics()
        
        # Force immediate UI update
        self.update()
        self.repaint()
        
        # Process all pending events
        from PyQt6.QtWidgets import QApplication
        QApplication.processEvents()
        
        print("All data refreshed successfully!")

    def load_statistics(self):
        """Load all statistics data"""
        try:
            self.db_manager.conn.commit()
        except Exception as e:
            print(f"Error committing database: {e}")
        
        # Get all data
        try:
            notes = self.db_manager.get_all_notes()
            tasks = self.db_manager.get_all_tasks()
            print(f"Total tasks from database: {len(tasks)}")
            
            # Debug: Print all tasks
            for i, task in enumerate(tasks):
                print(f"Task {i+1}: {task}")
            
            completed_tasks = [task for task in tasks if len(task) > 5 and task[5] == 1]
            pending_tasks = [task for task in tasks if len(task) > 5 and task[5] == 0]
            print(f"Completed tasks found: {len(completed_tasks)}")
            print(f"Pending tasks found: {len(pending_tasks)}")
            
            # Debug: Print completed tasks
            for i, task in enumerate(completed_tasks):
                print(f"Completed Task {i+1}: {task}")
            
            # Debug: Print pending tasks
            for i, task in enumerate(pending_tasks):
                print(f"Pending Task {i+1}: {task}")
            
            summaries = self.db_manager.get_all_note_summaries()
            
            # Get total seconds for status check
            total_seconds = self.db_manager.get_total_study_time()
            print(f"Total study time from database: {total_seconds} seconds")
            
            # Calculate time properly
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            secs = total_seconds % 60
            
            # Format time as single line
            time_text = f"{hours:02d}:{minutes:02d}:{secs:02d}"
            print(f"Formatted time text: {time_text}")
            
            # Update stat widgets - find time widget by searching for specific labels
            all_widgets = self.findChildren(QWidget)
            time_widget = None
            for widget in all_widgets:
                labels = widget.findChildren(QLabel)
                if labels and len(labels) >= 2:
                    # Check if this is our time widget by looking at title
                    title_label = labels[0]
                    if "Tổng Thời Gian" in title_label.text():
                        time_widget = widget
                        print(f"Found time widget: {title_label.text()}")
                        break
            
            if time_widget:
                # Find all labels in widget
                labels = time_widget.findChildren(QLabel)
                if labels and len(labels) >= 2:
                    # First label is title, second is value
                    title_label = labels[0]
                    value_label = labels[1]
                    print(f"Updating time from '{value_label.text()}' to '{time_text}'")
                    value_label.setText(time_text)
                    # Force immediate update
                    value_label.update()
                    time_widget.update()
                    time_widget.repaint()
                    # Force full widget update
                    self.update()
                    self.repaint()
                    print("Time widget updated successfully!")
            else:
                print("Time widget not found!")
            
            # Update history list
            self.history_list.clear()
            
            # Force database commit first
            try:
                self.db_manager.conn.commit()
                print("Database committed before loading sessions")
                
                # Additional: Try to force write
                self.db_manager.conn.execute("PRAGMA synchronous = FULL")
                self.db_manager.conn.commit()
                print("Force sync enabled")
                
            except Exception as e:
                print(f"Error committing database: {e}")
            
            # Get real study sessions from database
            try:
                # Use direct query instead of database method to get proper ordering
                cursor = self.db_manager.conn.cursor()
                cursor.execute("""
                    SELECT session_date, duration_seconds, mode 
                    FROM study_sessions 
                    ORDER BY datetime(session_date) DESC
                    LIMIT 10
                """)
                sessions = cursor.fetchall()
                print(f"Direct query found {len(sessions)} sessions")
                
                # Debug: Print all sessions
                for i, session in enumerate(sessions):
                    print(f"Session {i+1}: {session}")
                
                if sessions:
                    for session in sessions:
                        session_date, duration_seconds, mode = session
                        
                        # Format date
                        try:
                            if isinstance(session_date, str):
                                if len(session_date) == 10:  # YYYY-MM-DD format
                                    session_date_obj = datetime.strptime(session_date, '%Y-%m-%d')
                                else:  # Full datetime format
                                    session_date_obj = datetime.strptime(session_date, '%Y-%m-%d %H:%M:%S')
                            else:
                                session_date_obj = session_date
                            
                            today = datetime.now().date()
                            
                            if session_date_obj.date() == today:
                                date_str = "Hôm nay"
                            elif session_date_obj.date() == today.replace(day=today.day-1):
                                date_str = "Hôm qua"
                            else:
                                days_ago = (today - session_date_obj.date()).days
                                date_str = f"{days_ago} ngày trước"
                        except:
                            date_str = "Gần đây"
                        
                        # Determine icon based on duration and mode
                        if duration_seconds < 300:  # < 5 minutes
                            icon = '⚡'
                        elif duration_seconds < 900:  # < 15 minutes
                            icon = '📖'
                        elif duration_seconds < 1800:  # < 30 minutes
                            icon = '📚'
                        else:
                            icon = '🔥'
                        
                        # Create subject name
                        minutes = duration_seconds // 60
                        seconds = duration_seconds % 60
                        time_str = f"{minutes}p" if seconds == 0 else f"{minutes}p {seconds}s"
                        
                        session_text = f"{icon} Học tập ({mode}) - {time_str} ({date_str})"
                        print(f"Adding session: {session_text}")
                        
                        item = QListWidgetItem(session_text)
                        self.history_list.addItem(item)
                else:
                    # No sessions found
                    no_sessions = QListWidgetItem("📝 Chưa có phiên học nào")
                    self.history_list.addItem(no_sessions)
                    
            except Exception as e:
                print(f"Error loading study sessions: {e}")
                # Show error message
                error_item = QListWidgetItem("❌ Lỗi tải dữ liệu")
                self.history_list.addItem(error_item)
            
            # Update summaries
            self.auto_summaries_list.clear()
            if summaries:
                for summary_id, note_id, note_title, original_content, summary_content, created_at in summaries[:10]:
                    item_text = f"📄 {note_title[:20]}... ({created_at[:10]})"
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.ItemDataRole.UserRole, {
                        'id': summary_id,
                        'title': note_title,
                        'content': summary_content,
                        'created_at': created_at
                    })
                    self.auto_summaries_list.addItem(item)
            
            # Add click event for summaries
            self.auto_summaries_list.itemDoubleClicked.connect(self.on_summary_clicked)
            
            if not summaries:
                no_summaries = QListWidgetItem("Chưa có tóm tắt.")
                no_summaries.setData(Qt.ItemDataRole.UserRole, None)
                self.auto_summaries_list.addItem(no_summaries)
            
            # Update notes
            print(f"Loading {len(notes)} notes...")
            print(f"recent_notes_list id: {id(self.recent_notes_list)}")
            print(f"recent_notes_list count before clear: {self.recent_notes_list.count()}")
            self.recent_notes_list.clear()
            if notes:
                for i, (note_id, title, content, created_at, updated_at) in enumerate(notes[:10]):
                    print(f"Note {i+1}: {title[:20]}...")
                    item_text = f"📝 {title[:20]}... ({created_at[:10]})"
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.ItemDataRole.UserRole, {
                        'id': note_id,
                        'title': title,
                        'content': content,
                        'created_at': created_at,
                        'updated_at': updated_at
                    })
                    self.recent_notes_list.addItem(item)
            print(f"recent_notes_list count after load: {self.recent_notes_list.count()}")
            
            # Add click event for notes
            self.recent_notes_list.itemDoubleClicked.connect(self.on_note_clicked)
            
            if not notes:
                no_notes = QListWidgetItem("Chưa có ghi chú.")
                no_notes.setData(Qt.ItemDataRole.UserRole, None)
                self.recent_notes_list.addItem(no_notes)
            
            # Update completed tasks list
            self.completed_tasks_list.clear()
            if completed_tasks:
                for task in completed_tasks[:5]:  # Show max 5 completed tasks
                    # Handle 8 value task structure
                    task_id, title, description, deadline, priority, completed, created_at, updated_at = task
                    item_text = f"✅ {title[:25]}... ({deadline[:10]})"
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.ItemDataRole.UserRole, {
                        'id': task_id,
                        'title': title,
                        'description': description,
                        'deadline': deadline,
                        'completed': completed,
                        'created_at': created_at
                    })
                    self.completed_tasks_list.addItem(item)
            else:
                no_completed = QListWidgetItem("📝 Chưa có nhiệm vụ hoàn thành")
                no_completed.setData(Qt.ItemDataRole.UserRole, None)
                self.completed_tasks_list.addItem(no_completed)
            
            # Update pending tasks list
            self.pending_tasks_list.clear()
            if pending_tasks:
                for task in pending_tasks[:5]:  # Show max 5 pending tasks
                    # Handle 8 value task structure
                    task_id, title, description, deadline, priority, completed, created_at, updated_at = task
                    item_text = f"⏳ {title[:25]}... ({deadline[:10]})"
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.ItemDataRole.UserRole, {
                        'id': task_id,
                        'title': title,
                        'description': description,
                        'deadline': deadline,
                        'completed': completed,
                        'created_at': created_at
                    })
                    self.pending_tasks_list.addItem(item)
            else:
                no_pending = QListWidgetItem("📝 Chưa có nhiệm vụ chưa hoàn thành")
                no_pending.setData(Qt.ItemDataRole.UserRole, None)
                self.pending_tasks_list.addItem(no_pending)
            
        except Exception as e:
            print(f"Error loading statistics: {e}")
        
        # Force UI update
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, self._force_ui_update)
        
    def _force_ui_update(self):
        """Force UI update after all processing is done"""
        from PyQt6.QtWidgets import QApplication
        self.auto_summaries_list.updateGeometry()
        self.auto_summaries_list.repaint()
        self.recent_notes_list.updateGeometry()
        self.recent_notes_list.repaint()
        
        # Update both task lists
        if hasattr(self, 'completed_tasks_list'):
            self.completed_tasks_list.updateGeometry()
            self.completed_tasks_list.repaint()
            self.completed_tasks_list.update()
        if hasattr(self, 'pending_tasks_list'):
            self.pending_tasks_list.updateGeometry()
            self.pending_tasks_list.repaint()
            self.pending_tasks_list.update()
        
        # Force update history list
        if hasattr(self, 'history_list'):
            self.history_list.updateGeometry()
            self.history_list.repaint()
            self.history_list.update()
        
        self.update()
        QApplication.processEvents()

    def on_summary_clicked(self, item):
        """Handle double click on summary item"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if data:
            dialog = SummaryDialog(
                self,
                title=data['title'],
                content=data['content'],
                created_at=data['created_at']
            )
            dialog.exec()

    def on_note_clicked(self, item):
        """Handle double click on note item"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if data:
            dialog = NoteDialog(
                self,
                title=data['title'],
                content=data['content'],
                created_at=data['created_at'],
                updated_at=data.get('updated_at', data['created_at'])
            )
            dialog.exec()

    def format_duration(self, seconds):
        if seconds >= 3600:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            return f"{hours}h {minutes}m"
        elif seconds >= 60:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}m {secs}s"
        else:
            return f"{seconds}s"

    def apply_mode_restrictions(self, is_kid_mode):
        if is_kid_mode:
            # Apply kid mode restrictions
            pass
        else:
            # Remove kid mode restrictions
            pass

    def get_study_sessions(self):
        """Get study sessions from database"""
        try:
            # Use the existing database method
            sessions = self.db_manager.get_recent_study_sessions(limit=10)
            
            result = []
            for session in sessions:
                session_date, duration_seconds, mode = session
                
                # Format date
                try:
                    if isinstance(session_date, str):
                        if len(session_date) == 10:  # YYYY-MM-DD format
                            session_date_obj = datetime.strptime(session_date, '%Y-%m-%d')
                        else:  # Full datetime format
                            session_date_obj = datetime.strptime(session_date, '%Y-%m-%d %H:%M:%S')
                    else:
                        session_date_obj = session_date
                    
                    today = datetime.now().date()
                    
                    if session_date_obj.date() == today:
                        date_str = "Hôm nay"
                    elif session_date_obj.date() == today.replace(day=today.day-1):
                        date_str = "Hôm qua"
                    else:
                        days_ago = (today - session_date_obj.date()).days
                        date_str = f"{days_ago} ngày trước"
                except:
                    date_str = "Gần đây"
                
                # Determine icon based on duration and mode
                if duration_seconds < 300:  # < 5 minutes
                    icon = '⚡'
                elif duration_seconds < 900:  # < 15 minutes
                    icon = '📖'
                elif duration_seconds < 1800:  # < 30 minutes
                    icon = '📚'
                else:
                    icon = '🔥'
                
                # Create subject name
                minutes = duration_seconds // 60
                seconds = duration_seconds % 60
                time_str = f"{minutes}p" if seconds == 0 else f"{minutes}p {seconds}s"
                
                result.append({
                    'subject': f"Học tập ({mode})",
                    'duration': duration_seconds,
                    'date': date_str,
                    'icon': icon
                })
            
            return result
            
        except Exception as e:
            print(f"Error getting study sessions: {e}")
            return []

    def create_study_sessions_table(self):
        """Create study_sessions table if it doesn't exist"""
        try:
            cursor = self.db_manager.conn.cursor()
            
            # Create table with multiple possible column names for flexibility
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS study_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT,
                    duration INTEGER,
                    created_at TEXT,
                    icon TEXT DEFAULT '📖',
                    -- Alternative column names for compatibility
                    name TEXT,
                    seconds INTEGER,
                    date TEXT,
                    emoji TEXT DEFAULT '📖'
                )
            ''')
            
            self.db_manager.conn.commit()
            
        except Exception as e:
            print(f"Error creating study_sessions table: {e}")

    def save_study_session(self, subject, duration_seconds, icon='📖'):
        """Save a study session to database"""
        try:
            cursor = self.db_manager.conn.cursor()
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                INSERT INTO study_sessions (subject, duration, created_at, icon)
                VALUES (?, ?, ?, ?)
            ''', (subject, duration_seconds, created_at, icon))
            
            self.db_manager.conn.commit()
            print(f"Saved study session: {subject} - {duration_seconds}s")
            
        except Exception as e:
            print(f"Error saving study session: {e}")

    def save_timer_session(self, duration_seconds):
        """Save timer session with automatic naming"""
        try:
            now = datetime.now()
            time_str = now.strftime('%H:%M')
            subject = f"Học tập ({time_str})"
            
            # Auto-determine icon based on duration
            if duration_seconds < 300:  # < 5 minutes
                icon = '⚡'
            elif duration_seconds < 900:  # < 15 minutes
                icon = '📖'
            elif duration_seconds < 1800:  # < 30 minutes
                icon = '📚'
            else:
                icon = '🔥'
            
            self.save_study_session(subject, duration_seconds, icon)
            
        except Exception as e:
            print(f"Error saving timer session: {e}")
