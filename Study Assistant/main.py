import sys

from PyQt6.QtCore import QDate, Qt, QTimer  # For alignment, dates, and timers
from PyQt6.QtGui import QFont  # For font
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMessageBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from src.database.db_manager import DatabaseManager
from src.notes.notes_tab import NotesTab
from src.reminders.reminders_tab import RemindersTab
from src.statistics.statistics_tab import StatisticsTab
from src.tasks.tasks_tab import TasksTab
from src.timer.timer_tab import TimerTab
from src.utils.styles import get_qss_styles


class StudyAssistantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trợ Lý Học Tập")
        self.setGeometry(100, 100, 800, 600)

        self.db_manager = DatabaseManager()

        # Automated task check timer (every 1 hour)
        self.task_check_timer = QTimer(self)
        self.task_check_timer.setInterval(3600000)  # 1 hour
        self.task_check_timer.timeout.connect(self.check_task_deadlines)
        self.task_check_timer.start()

        # Initial check on startup after a short delay
        QTimer.singleShot(3000, self.check_task_deadlines)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        self.setup_tabs()

    def setup_tabs(self):
        # Home Tab
        home_tab = QWidget()
        home_layout = QVBoxLayout(home_tab)

        # Create the welcome label
        welcome_label = QLabel("Chào mừng bạn đến với Ứng dụng Trợ Lý Học Tập!")

        # Set font to Times New Roman, size 36
        font = QFont("Times New Roman", 40)
        welcome_label.setFont(font)

        # Center the text
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        home_layout.addWidget(welcome_label)
        self.tab_widget.addTab(home_tab, "Trang Chủ")
        self.home_tab_index = self.tab_widget.indexOf(home_tab)

        # Timer Tab
        self.timer_tab_widget = TimerTab(
            self.db_manager, self
        )  # Pass self (StudyAssistantApp)
        self.timer_tab_index = self.tab_widget.addTab(self.timer_tab_widget, "Hẹn Giờ")

        # Notes Tab
        self.notes_tab_widget = NotesTab(self.db_manager)
        self.notes_tab_index = self.tab_widget.addTab(self.notes_tab_widget, "Ghi Chú")

        # Tasks Tab
        self.tasks_tab_widget = TasksTab(self.db_manager)
        self.tasks_tab_index = self.tab_widget.addTab(self.tasks_tab_widget, "Nhiệm Vụ")

        # Reminders Tab
        self.reminders_tab_widget = RemindersTab(self.db_manager)
        self.reminders_tab_index = self.tab_widget.addTab(
            self.reminders_tab_widget, "Nhắc Nhở"
        )

        # Statistics Tab
        self.stats_tab_widget = StatisticsTab(self.db_manager)
        self.stats_tab_index = self.tab_widget.addTab(self.stats_tab_widget, "Báo Cáo")

        self.apply_mode_restrictions("normal")  # Initialize with normal mode

    def apply_mode_restrictions(self, mode):
        # Apply restrictions based on the mode
        if mode == "kid":
            # Go full screen to cover taskbar and prevent easy access to other apps
            self.showFullScreen()

            # Call restriction methods on individual tabs
            self.notes_tab_widget.apply_mode_restrictions(True)
            self.tasks_tab_widget.apply_mode_restrictions(True)
            self.reminders_tab_widget.apply_mode_restrictions(True)
            self.stats_tab_widget.apply_mode_restrictions(True)
        elif mode == "normal":
            # Restore normal window
            self.showNormal()

            # Remove restrictions on individual tabs
            self.notes_tab_widget.apply_mode_restrictions(False)
            self.tasks_tab_widget.apply_mode_restrictions(False)
            self.reminders_tab_widget.apply_mode_restrictions(False)
            self.stats_tab_widget.apply_mode_restrictions(False)

        QApplication.processEvents()  # Force UI to update immediately

    def check_task_deadlines(self):
        """Automatically checks for tasks that are due today or overdue."""
        current_date = QDate.currentDate().toString("yyyy-MM-dd")
        upcoming_tasks = self.db_manager.get_upcoming_uncompleted_tasks(current_date)

        due_today = []
        for task in upcoming_tasks:
            if task[3] == current_date:
                due_today.append(task[1])  # title

        if due_today:
            titles = "\n- ".join(due_today)
            QMessageBox.information(
                self,
                "Tự động nhắc nhở nhiệm vụ",
                f"Bạn có các nhiệm vụ sau cần hoàn thành trong hôm nay:\n- {titles}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(get_qss_styles())  # Apply global styles
    window = StudyAssistantApp()
    window.show()
    sys.exit(app.exec())
