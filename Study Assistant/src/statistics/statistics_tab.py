from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class StatisticsTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.load_statistics()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # Header Title
        self.header_label = QLabel("Báo Cáo Tiến Độ Học Tập")
        header_font = self.header_label.font()
        header_font.setPointSize(24)
        header_font.setBold(True)
        self.header_label.setFont(header_font)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.header_label)

        # Total Time Card
        self.total_time_frame = QFrame()
        self.total_time_frame.setObjectName("totalTimeCard")
        self.total_time_frame.setStyleSheet("""
            #totalTimeCard {
                background-color: #34495e;
                border-radius: 15px;
                border: 2px solid #2ecc71;
            }
        """)
        total_layout = QVBoxLayout(self.total_time_frame)
        total_layout.setContentsMargins(30, 30, 30, 30)

        self.total_title = QLabel("TỔNG THỜI GIAN ĐÃ HỌC")
        self.total_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_title.setStyleSheet("font-weight: bold; color: #bdc3c7;")

        self.total_time_display = QLabel("00:00:00")
        self.total_time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_font = self.total_time_display.font()
        time_font.setPointSize(48)
        time_font.setBold(True)
        self.total_time_display.setFont(time_font)
        self.total_time_display.setStyleSheet("color: #2ecc71; margin-top: 10px;")

        total_layout.addWidget(self.total_title)
        total_layout.addWidget(self.total_time_display)
        self.main_layout.addWidget(self.total_time_frame)

        # Daily History Label
        self.history_title = QLabel("Hoạt động trong 7 ngày gần nhất:")
        self.history_title.setStyleSheet(
            "font-weight: bold; font-size: 16px; margin-top: 20px;"
        )
        self.main_layout.addWidget(self.history_title)

        # History Container
        self.history_container = QVBoxLayout()
        self.main_layout.addLayout(self.history_container)

        self.main_layout.addStretch()

        # Refresh Button
        self.refresh_button = QPushButton("Làm Mới Báo Cáo")
        self.refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_button.clicked.connect(self.load_statistics)
        self.main_layout.addWidget(self.refresh_button)

    def format_duration(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours} giờ {minutes} phút {secs} giây"
        elif minutes > 0:
            return f"{minutes} phút {secs} giây"
        else:
            return f"{secs} giây"

    def load_statistics(self):
        # 1. Update Total Study Time
        total_seconds = self.db_manager.get_total_study_time()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        self.total_time_display.setText(f"{hours:02d}:{minutes:02d}:{secs:02d}")

        # 2. Update Daily Breakdown
        # Clear current history display
        while self.history_container.count():
            item = self.history_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        recent_sessions = self.db_manager.get_recent_study_sessions(7)

        if not recent_sessions:
            no_data = QLabel("Chưa có dữ liệu học tập tự động được ghi nhận.")
            no_data.setStyleSheet("color: #7f8c8d; font-style: italic;")
            self.history_container.addWidget(no_data)
        else:
            for date_str, duration in recent_sessions:
                h_layout = QHBoxLayout()

                date_label = QLabel(date_str)
                date_label.setStyleSheet("font-weight: bold;")

                duration_label = QLabel(self.format_duration(duration))
                duration_label.setStyleSheet("color: #2ecc71;")

                h_layout.addWidget(date_label)
                h_layout.addStretch()
                h_layout.addWidget(duration_label)

                row_frame = QFrame()
                row_frame.setLayout(h_layout)
                row_frame.setStyleSheet(
                    "border-bottom: 1px solid #34495e; padding: 5px;"
                )
                self.history_container.addWidget(row_frame)

    def apply_mode_restrictions(self, restricted):
        """Kid mode restrictions for statistics."""
        # In kid mode, we disable the refresh button to avoid distraction
        self.refresh_button.setEnabled(not restricted)
        if restricted:
            self.header_label.setText("Tiến Độ Học Của Bé")
        else:
            self.header_label.setText("Báo Cáo Tiến Độ Học Tập")

        # Reload to update labels if needed
        self.load_statistics()
