import sys
import os

from PyQt6.QtCore import QDate, Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMessageBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.database.db_manager import DatabaseManager, DATABASE_NAME
from src.notes.notes_tab import NotesTab
from src.statistics.statistics_tab import StatisticsTab
from src.summary.summary_tab import SummaryTab
from src.tasks.tasks_tab import TasksTab
from src.timer.timer_tab import TimerTab
from src.utils.styles import get_qss_styles

# Fix database path to use absolute path
ABSOLUTE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATABASE_NAME)


# ===== Widget Trang Chủ Vẽ Ảnh Chuẩn =====
class HomeWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.pixmap = QPixmap(image_path)

        self.label = QLabel(
            "Chào mừng bạn đến với Ứng dụng Trợ Lý Học Tập!", self
        )
        font = QFont("Times New Roman", 40)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            color: white;
            background-color: rgba(0, 0, 0, 150);
            padding: 25px;
            border-radius: 15px;
        """)

    def resizeEvent(self, event):
        self.label.adjustSize()
        self.label.move(
            (self.width() - self.label.width()) // 2,
            (self.height() - self.label.height()) // 2,
        )
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)

        if not self.pixmap.isNull():
            scaled = self.pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )

            x = (scaled.width() - self.width()) // 2
            y = (scaled.height() - self.height()) // 2

            painter.drawPixmap(0, 0, scaled, x, y, self.width(), self.height())


class StudyAssistantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trợ Lý Học Tập")
        self.setGeometry(100, 100, 1000, 650)

        self.db_manager = DatabaseManager(ABSOLUTE_DB_PATH)

        self.task_check_timer = QTimer(self)
        self.task_check_timer.setInterval(3600000)
        self.task_check_timer.timeout.connect(self.check_task_deadlines)
        self.task_check_timer.start()

        QTimer.singleShot(3000, self.check_task_deadlines)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        self.setup_tabs()

    def apply_mode_restrictions(self, mode):
        try:
            if mode == "kid":
                self.showFullScreen()

                if hasattr(self, "notes_tab_widget"):
                    self.notes_tab_widget.apply_mode_restrictions(True)
                if hasattr(self, "tasks_tab_widget"):
                    self.tasks_tab_widget.apply_mode_restrictions(True)
                if hasattr(self, "stats_tab_widget"):
                    self.stats_tab_widget.apply_mode_restrictions(True)
                if hasattr(self, "summary_tab_widget"):
                    self.summary_tab_widget.apply_mode_restrictions(True)

            elif mode == "normal":
                self.showNormal()

                if hasattr(self, "notes_tab_widget"):
                    self.notes_tab_widget.apply_mode_restrictions(False)
                if hasattr(self, "tasks_tab_widget"):
                    self.tasks_tab_widget.apply_mode_restrictions(False)
                if hasattr(self, "stats_tab_widget"):
                    self.stats_tab_widget.apply_mode_restrictions(False)
                if hasattr(self, "summary_tab_widget"):
                    self.summary_tab_widget.apply_mode_restrictions(False)
        except Exception as e:
            print(f"ERROR in apply_mode_restrictions: {e}")
            import traceback
            traceback.print_exc()

    def setup_tabs(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_path, "src", "TC.jpg")

            home_widget = HomeWidget(image_path)
            self.tab_widget.addTab(home_widget, "Trang Chủ")

            # LƯU CÁC TAB VÀO BIẾN (QUAN TRỌNG)
            self.timer_tab_widget = TimerTab(self.db_manager, self)
            self.tab_widget.addTab(self.timer_tab_widget, "Hẹn Giờ")

            self.notes_tab_widget = NotesTab(self.db_manager)
            self.tab_widget.addTab(self.notes_tab_widget, "Ghi Chú")

            self.tasks_tab_widget = TasksTab(self.db_manager)
            self.tab_widget.addTab(self.tasks_tab_widget, "Nhiệm Vụ")

            self.stats_tab_widget = StatisticsTab(self.db_manager)
            self.tab_widget.addTab(self.stats_tab_widget, "Thống kê")

            self.summary_tab_widget = SummaryTab(self.db_manager)
            self.tab_widget.addTab(self.summary_tab_widget, "Tóm Tắt")
        except Exception as e:
            print(f"ERROR in setup_tabs: {e}")
            import traceback
            traceback.print_exc()

    def check_task_deadlines(self):
        current_date = QDate.currentDate().toString("yyyy-MM-dd")
        upcoming_tasks = self.db_manager.get_upcoming_uncompleted_tasks(current_date)

        due_today = [task[1] for task in upcoming_tasks if task[3] == current_date]

        if due_today:
            titles = "\n- ".join(due_today)
            QMessageBox.information(
                self,
                "Tự động nhắc nhở nhiệm vụ",
                f"Bạn có các nhiệm vụ sau cần hoàn thành hôm nay:\n- {titles}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(get_qss_styles())
    window = StudyAssistantApp()
    window.show()
    sys.exit(app.exec())