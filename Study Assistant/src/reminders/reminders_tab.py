from datetime import datetime

from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (
    QCheckBox,
    QDateTimeEdit,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from src.database.db_manager import DatabaseManager


class RemindersTab(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.current_reminder_id = None
        self.init_ui()
        self.load_reminders()

        # Timer to check for reminders every minute
        self.reminder_check_timer = QTimer(self)
        self.reminder_check_timer.setInterval(
            60000
        )  # Check every minute (60,000 milliseconds)
        self.reminder_check_timer.timeout.connect(self.check_for_reminders)
        self.reminder_check_timer.start()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Left panel: List of reminders
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Tất Cả Nhắc Nhở:"))

        self.reminder_list_widget = QListWidget()
        self.reminder_list_widget.itemClicked.connect(self.display_reminder)
        left_panel.addWidget(self.reminder_list_widget)

        self.add_reminder_button = QPushButton("Thêm Nhắc Nhở Mới")
        self.add_reminder_button.clicked.connect(self.add_new_reminder)
        left_panel.addWidget(self.add_reminder_button)

        main_layout.addLayout(left_panel, 1)

        # Right panel: Reminder editor
        right_panel = QVBoxLayout()

        self.reminder_title_input = QLineEdit()
        self.reminder_title_input.setPlaceholderText("Tiêu Đề Nhắc Nhở")
        right_panel.addWidget(self.reminder_title_input)

        self.reminder_description_input = QTextEdit()
        self.reminder_description_input.setPlaceholderText("Mô Tả Nhắc Nhở")
        right_panel.addWidget(self.reminder_description_input)

        # Reminder Time
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Đặt Thời Gian:"))
        self.reminder_datetime_input = QDateTimeEdit()
        self.reminder_datetime_input.setCalendarPopup(True)
        self.reminder_datetime_input.setDateTime(QDateTime.currentDateTime())
        self.reminder_datetime_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        time_layout.addWidget(self.reminder_datetime_input)
        right_panel.addLayout(time_layout)

        # Is Active checkbox
        self.reminder_active_checkbox = QCheckBox("Hoạt Động")
        self.reminder_active_checkbox.setChecked(True)
        right_panel.addWidget(self.reminder_active_checkbox)

        # Action buttons for reminders
        button_layout = QHBoxLayout()
        self.save_reminder_button = QPushButton("Lưu Nhắc Nhở")
        self.save_reminder_button.clicked.connect(self.save_reminder)
        self.save_reminder_button.setEnabled(False)
        button_layout.addWidget(self.save_reminder_button)

        self.delete_reminder_button = QPushButton("Xóa Nhắc Nhở")
        self.delete_reminder_button.clicked.connect(self.delete_reminder)
        self.delete_reminder_button.setEnabled(
            False
        )  # Disable delete until a reminder is selected
        button_layout.addWidget(self.delete_reminder_button)

        right_panel.addLayout(button_layout)

        main_layout.addLayout(right_panel, 3)
        self.clear_reminder_fields()

    def load_reminders(self):
        self.reminder_list_widget.clear()
        reminders = self.db_manager.get_all_reminders()  # Needs to be implemented
        for reminder in reminders:
            item_text = f"{reminder[1]} ({reminder[3]})"  # tiêu đề (thời gian nhắc nhở)
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, reminder[0])  # reminder[0] is id
            if not reminder[4]:  # is_active
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(Qt.GlobalColor.darkGray)
            self.reminder_list_widget.addItem(item)
        self.clear_reminder_fields()

    def display_reminder(self, item):
        reminder_id = item.data(Qt.ItemDataRole.UserRole)
        reminder = self.db_manager.get_reminder_by_id(
            reminder_id
        )  # Needs to be implemented
        if reminder:
            self.current_reminder_id = reminder[0]
            self.reminder_title_input.setText(reminder[1])
            self.reminder_description_input.setText(reminder[2])
            self.reminder_datetime_input.setDateTime(
                QDateTime.fromString(reminder[3], "yyyy-MM-dd HH:mm:ss")
            )
            self.reminder_active_checkbox.setChecked(bool(reminder[4]))
            self.save_reminder_button.setEnabled(True)
            self.delete_reminder_button.setEnabled(True)
        else:
            self.clear_reminder_fields()

    def add_new_reminder(self):
        self.clear_reminder_fields()
        self.current_reminder_id = None
        self.save_reminder_button.setEnabled(True)
        self.delete_reminder_button.setEnabled(False)
        self.reminder_title_input.setFocus()

    def save_reminder(self):
        title = self.reminder_title_input.text().strip()
        description = self.reminder_description_input.toPlainText().strip()
        reminder_time_str = self.reminder_datetime_input.dateTime().toString(
            "yyyy-MM-dd HH:mm:ss"
        )
        is_active = 1 if self.reminder_active_checkbox.isChecked() else 0
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not title:
            QMessageBox.warning(
                self, "Lỗi Nhập Liệu", "Tiêu đề nhắc nhở không được để trống."
            )
            return

        if self.current_reminder_id is None:
            # Add new reminder
            self.db_manager.add_reminder(
                title, description, reminder_time_str, is_active, current_time
            )  # Needs to be implemented
            QMessageBox.information(self, "Success", "Reminder added successfully!")
        else:
            # Update existing reminder
            self.db_manager.update_reminder(
                self.current_reminder_id,
                title,
                description,
                reminder_time_str,
                is_active,
            )  # Cần triển khai
            QMessageBox.information(
                self, "Thành Công", "Nhắc nhở đã được cập nhật thành công!"
            )

        self.load_reminders()
        self.clear_reminder_fields()

    def delete_reminder(self):
        if self.current_reminder_id is None:
            return

        reply = QMessageBox.question(
            self,
            "Xác Nhận Xóa",
            "Bạn có chắc chắn muốn xóa nhắc nhở này không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_reminder(self.current_reminder_id)  # Cần triển khai
            QMessageBox.information(
                self, "Thành Công", "Nhắc nhở đã được xóa thành công!"
            )
            self.load_reminders()
            self.clear_reminder_fields()

    def clear_reminder_fields(self):
        self.current_reminder_id = None
        self.reminder_title_input.clear()
        self.reminder_description_input.clear()
        self.reminder_datetime_input.setDateTime(QDateTime.currentDateTime())
        self.reminder_active_checkbox.setChecked(True)
        self.save_reminder_button.setEnabled(False)
        self.delete_reminder_button.setEnabled(False)

    def check_for_reminders(self):
        current_datetime = QDateTime.currentDateTime()
        # Format to match database storage, but only up to minute for comparison
        current_datetime_str = current_datetime.toString("yyyy-MM-dd HH:mm:ss")

        reminders = self.db_manager.get_active_reminders_due_now(
            current_datetime_str
        )  # Cần triển khai
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for reminders..."
        )
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Current time for comparison: {current_datetime_str}"
        )

        reminders = self.db_manager.get_active_reminders_due_now(
            current_datetime_str
        )  # Cần triển khai
        if reminders:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Found {len(reminders)} active reminders due now."
            )
        else:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] No active reminders due now."
            )

        for reminder in reminders:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Triggering reminder: {reminder[1]} at {reminder[3]}"
            )
            QMessageBox.information(
                self, "Nhắc Nhở!", f"Đã đến giờ cho: {reminder[1]} - {reminder[2]}"
            )
            # Deactivate the reminder after showing it
            self.db_manager.deactivate_reminder(reminder[0])
            self.load_reminders()

    def apply_mode_restrictions(self, restricted):
        """Disables editing features in Kid Mode."""
        self.add_reminder_button.setEnabled(not restricted)
        self.reminder_title_input.setReadOnly(restricted)
        self.reminder_description_input.setReadOnly(restricted)
        self.reminder_datetime_input.setReadOnly(restricted)
        self.reminder_active_checkbox.setEnabled(not restricted)

        if restricted:
            self.save_reminder_button.setEnabled(False)
            self.delete_reminder_button.setEnabled(False)
        else:
            # Restore button states based on selection
            if self.current_reminder_id is not None:
                self.save_reminder_button.setEnabled(True)
                self.delete_reminder_button.setEnabled(True)
