from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,  # Added for better layout
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class PasswordChangeDialog(QDialog):
    def __init__(self, parent=None, admin_password_set=False):
        super().__init__(parent)
        self.setWindowTitle("Xác Nhận Mật Khẩu Admin")
        self.setModal(True)
        # Set a fixed size for the dialog for better appearance
        self.setFixedSize(350, 150)

        self.admin_password_set = admin_password_set

        self.input_password = ""
        self.change_password_checked = False

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 10)  # Add margins
        main_layout.setSpacing(15)  # Add spacing between widgets

        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(10)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow(QLabel("Mật khẩu Admin:"), self.password_input)

        # Checkbox for changing password
        self.change_password_checkbox = QCheckBox("Đổi mật khẩu Admin")
        # Only show and enable if a password is already set
        self.change_password_checkbox.setVisible(self.admin_password_set)
        self.change_password_checkbox.setEnabled(self.admin_password_set)
        form_layout.addRow(self.change_password_checkbox)  # Add checkbox to form layout

        main_layout.addLayout(form_layout)  # Add the form layout to the main layout
        main_layout.addStretch()  # Push buttons to the bottom

        # OK and Cancel buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # Spacing between buttons

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Hủy")
        cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    def accept(self):
        self.input_password = self.password_input.text()
        self.change_password_checked = self.change_password_checkbox.isChecked()
        super().accept()

    def get_data(self):
        return self.input_password, self.change_password_checked
