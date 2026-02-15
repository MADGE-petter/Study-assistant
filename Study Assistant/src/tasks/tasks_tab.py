from datetime import datetime

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
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


class TasksTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.current_task_id = None
        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Left panel for task list
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Tất Cả Nhiệm Vụ:"))

        self.task_list_widget = QListWidget()
        self.task_list_widget.itemClicked.connect(self.display_task)
        left_panel.addWidget(self.task_list_widget)

        self.add_task_button = QPushButton("Thêm Nhiệm Vụ Mới")
        self.add_task_button.clicked.connect(self.add_new_task)
        left_panel.addWidget(self.add_task_button)

        main_layout.addLayout(left_panel, 1)

        # Right panel for task details
        right_panel = QVBoxLayout()

        self.task_title_input = QLineEdit()
        self.task_title_input.setPlaceholderText("Tiêu Đề Nhiệm Vụ")
        right_panel.addWidget(self.task_title_input)

        self.task_description_input = QTextEdit()
        self.task_description_input.setPlaceholderText("Mô Tả Nhiệm Vụ")
        right_panel.addWidget(self.task_description_input)

        # Due Date
        due_date_layout = QHBoxLayout()
        due_date_layout.addWidget(QLabel("Ngày Đến Hạn:"))
        self.task_due_date_input = QDateEdit()
        self.task_due_date_input.setCalendarPopup(True)
        self.task_due_date_input.setDate(QDate.currentDate())
        due_date_layout.addWidget(self.task_due_date_input)
        right_panel.addLayout(due_date_layout)

        # Priority
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(QLabel("Ưu Tiên:"))
        self.task_priority_combo = QComboBox()
        self.task_priority_combo.addItems(["Thấp", "Trung Bình", "Cao"])
        self.task_priority_combo.setCurrentIndex(0)  # Mặc định là Thấp
        priority_layout.addWidget(self.task_priority_combo)
        right_panel.addLayout(priority_layout)

        # Is Completed
        self.task_completed_checkbox = QCheckBox("Hoàn Thành")
        right_panel.addWidget(self.task_completed_checkbox)

        button_layout = QHBoxLayout()
        self.save_task_button = QPushButton("Lưu Nhiệm Vụ")
        self.save_task_button.clicked.connect(self.save_task)
        self.save_task_button.setEnabled(False)
        button_layout.addWidget(self.save_task_button)

        self.delete_task_button = QPushButton("Xóa Nhiệm Vụ")
        self.delete_task_button.clicked.connect(self.delete_task)
        self.delete_task_button.setEnabled(False)
        button_layout.addWidget(self.delete_task_button)

        right_panel.addLayout(button_layout)
        main_layout.addLayout(right_panel, 3)

        self.clear_task_fields()

    def load_tasks(self):
        self.task_list_widget.clear()
        tasks = (
            self.db_manager.get_all_tasks()
        )  # This function needs to be implemented in db_manager
        for task in tasks:
            item_text = f"{task[1]} (Due: {task[3] if task[3] else 'N/A'})"
            item = QListWidgetItem(item_text)  # task[1] is the title
            item.setData(Qt.ItemDataRole.UserRole, task[0])  # task[0] is the id

            if task[5]:  # task[5] is is_completed
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Checked)
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(Qt.GlobalColor.darkGray)
            else:
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)

            self.task_list_widget.addItem(item)
        self.clear_task_fields()

    def display_task(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        task = self.db_manager.get_task_by_id(
            task_id
        )  # This function needs to be implemented
        if task:
            self.current_task_id = task[0]
            self.task_title_input.setText(task[1])
            self.task_description_input.setText(task[2])

            if task[3]:  # Due Date
                self.task_due_date_input.setDate(
                    QDate.fromString(task[3], "yyyy-MM-dd")
                )
            else:
                self.task_due_date_input.setDate(QDate.currentDate())

            self.task_priority_combo.setCurrentIndex(task[4])  # Priority
            self.task_completed_checkbox.setChecked(bool(task[5]))  # Is Completed

            self.save_task_button.setEnabled(True)
            self.delete_task_button.setEnabled(True)
        else:
            self.clear_task_fields()

    def add_new_task(self):
        self.clear_task_fields()
        self.current_task_id = None
        self.save_task_button.setEnabled(True)
        self.delete_task_button.setEnabled(False)
        self.task_title_input.setFocus()

    def save_task(self):
        title = self.task_title_input.text().strip()
        description = self.task_description_input.toPlainText().strip()
        due_date = self.task_due_date_input.date().toString("yyyy-MM-dd")
        priority = self.task_priority_combo.currentIndex()
        is_completed = 1 if self.task_completed_checkbox.isChecked() else 0

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        completed_at = current_time if is_completed else None

        if not title:
            QMessageBox.warning(
                self, "Lỗi Nhập Liệu", "Tiêu đề nhiệm vụ không được để trống."
            )
            return

        if self.current_task_id is None:
            # Add new task
            self.db_manager.add_task(
                title,
                description,
                due_date,
                priority,
                is_completed,
                current_time,
                completed_at,
            )  # This needs to be implemented
            QMessageBox.information(self, "Success", "Task added successfully!")
        else:
            # Update existing task
            self.db_manager.update_task(
                self.current_task_id,
                title,
                description,
                due_date,
                priority,
                is_completed,
                completed_at,
            )  # This needs to be implemented
            QMessageBox.information(self, "Success", "Task updated successfully!")

        self.load_tasks()
        self.clear_task_fields()

    def delete_task(self):
        if self.current_task_id is None:
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_task(
                self.current_task_id
            )  # This needs to be implemented
            QMessageBox.information(self, "Success", "Task deleted successfully!")
            self.load_tasks()
            self.clear_task_fields()

    def clear_task_fields(self):
        self.current_task_id = None
        self.task_title_input.clear()
        self.task_description_input.clear()
        self.task_due_date_input.setDate(QDate.currentDate())
        self.task_priority_combo.setCurrentIndex(0)
        self.task_completed_checkbox.setChecked(False)
        self.save_task_button.setEnabled(False)
        self.delete_task_button.setEnabled(False)

    def apply_mode_restrictions(self, restricted):
        """Disables editing features in Kid Mode."""
        self.add_task_button.setEnabled(not restricted)
        self.task_title_input.setReadOnly(restricted)
        self.task_description_input.setReadOnly(restricted)
        self.task_due_date_input.setReadOnly(restricted)
        self.task_priority_combo.setEnabled(not restricted)
        self.task_completed_checkbox.setEnabled(not restricted)

        if restricted:
            self.save_task_button.setEnabled(False)
            self.delete_task_button.setEnabled(False)
        else:
            # Restore button states based on selection
            if self.current_task_id is not None:
                self.save_task_button.setEnabled(True)
                self.delete_task_button.setEnabled(True)
