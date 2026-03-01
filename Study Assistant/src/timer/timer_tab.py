import hashlib  # For password hashing
import logging  # For logging events

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)
from src.database.db_manager import DatabaseManager
from src.dialogs.password_change_dialog import PasswordChangeDialog


class TimerTab(QWidget):
    def __init__(self, db_manager: DatabaseManager, app_instance):
        super().__init__()
        self.db_manager = db_manager  # Store the DatabaseManager instance
        self.app = app_instance  # Store the main application instance

        # Default times for Normal mode
        self.normal_pomodoro_time = 25 * 60  # 25 minutes in seconds
        self.normal_short_break_time = 5 * 60  # 5 minutes in seconds
        self.normal_long_break_time = 15 * 60  # 15 minutes in seconds

        # Default time for Kid mode
        self.kid_pomodoro_time = 30 * 60  # 30 minutes in seconds

        self.pomodoro_time = self.normal_pomodoro_time
        self.short_break_time = self.normal_short_break_time
        self.long_break_time = self.normal_long_break_time

        self.current_time = self.pomodoro_time
        self.is_running = False
        self.on_break = False
        self.pomodoro_count = 0
        self.mode = "normal"  # Default mode

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Mode Selection
        mode_layout = QHBoxLayout()
        self.normal_mode_button = QPushButton("Chế Độ Thường")
        self.normal_mode_button.clicked.connect(self.set_normal_mode)
        mode_layout.addWidget(self.normal_mode_button)

        self.kid_mode_button = QPushButton("Chế Độ Trẻ Em")
        self.kid_mode_button.clicked.connect(self.set_kid_mode)
        mode_layout.addWidget(self.kid_mode_button)
        main_layout.addLayout(mode_layout)

        # Timer display
        self.time_display = QLabel(self.format_time(self.current_time))
        self.time_display.setStyleSheet("font-size: 72px; font-weight: bold;")
        main_layout.addWidget(self.time_display, alignment=Qt.AlignmentFlag.AlignCenter)

        # Hiển thị trạng thái
        self.status_display = QLabel("Sẵn sàng học thôi!")
        self.status_display.setStyleSheet("font-size: 24px; color: gray;")
        main_layout.addWidget(
            self.status_display, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Nút điều khiển
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Bắt Đầu")
        self.start_button.clicked.connect(self.start_timer)
        button_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Tạm Dừng")
        self.pause_button.clicked.connect(self.pause_timer)
        self.pause_button.setEnabled(False)
        button_layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("Đặt Lại")
        self.reset_button.clicked.connect(self.reset_timer)
        button_layout.addWidget(self.reset_button)

        self.skip_button = QPushButton("Bỏ Qua")
        self.skip_button.clicked.connect(self.skip_phase)
        self.skip_button.setEnabled(False)
        button_layout.addWidget(self.skip_button)

        main_layout.addLayout(button_layout)

        # Settings
        settings_layout = QHBoxLayout()
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        settings_layout.addWidget(QLabel("Pomodoro (phút):"))
        self.pomodoro_spinbox = QSpinBox()
        self.pomodoro_spinbox.setRange(1, 60)
        self.pomodoro_spinbox.setValue(self.pomodoro_time // 60)
        self.pomodoro_spinbox.valueChanged.connect(self.set_pomodoro_time)
        settings_layout.addWidget(self.pomodoro_spinbox)

        settings_layout.addWidget(QLabel("Nghỉ Ngắn (phút):"))
        self.short_break_spinbox = QSpinBox()
        self.short_break_spinbox.setRange(1, 30)
        self.short_break_spinbox.setValue(self.short_break_time // 60)
        self.short_break_spinbox.valueChanged.connect(self.set_short_break_time)
        settings_layout.addWidget(self.short_break_spinbox)

        settings_layout.addWidget(QLabel("Nghỉ Dài (phút):"))
        self.long_break_spinbox = QSpinBox()
        self.long_break_spinbox.setRange(1, 60)
        self.long_break_spinbox.setValue(self.long_break_time // 60)
        self.long_break_spinbox.valueChanged.connect(self.set_long_break_time)
        settings_layout.addWidget(self.long_break_spinbox)

        # New: Change Password Button
        self.change_password_button = QPushButton("Đổi Mật Khẩu")
        self.change_password_button.clicked.connect(self.change_admin_password)
        settings_layout.addWidget(self.change_password_button)

        main_layout.addLayout(settings_layout)

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def update_timer(self):
        if self.current_time > 0:
            self.current_time -= 1
            self.time_display.setText(self.format_time(self.current_time))
            
            # Debug every 10 seconds
            if self.current_time % 10 == 0:
                print(f"[TIMER] Update - Time: {self.current_time}s, Running: {self.is_running}, On break: {self.on_break}")
        else:
            print(f"[TIMER] Timer reached 0 - Running: {self.is_running}, On break: {self.on_break}")
            self.timer.stop()
            self.is_running = False
            self.toggle_buttons(False)  # Disable pause/skip, enable start/reset

            if not self.on_break:  # Pomodoro time ended
                self.pomodoro_count += 1
                # Automatically log the study session
                print(f"[TIMER] Pomodoro completed. Logging {self.pomodoro_time} seconds for mode: {self.mode}")
                self.db_manager.add_study_session(self.pomodoro_time, self.mode)
                print(f"[TIMER] Study session logged successfully")

                if self.mode == "kid":
                    # In kid mode, no breaks, go straight to next pomodoro
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle("Thời gian học đã hết!")
                    msg_box.setText(
                        "30 phút học của bạn đã hết! Bấm OK để bắt đầu phiên mới."
                    )
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg_box.exec()

                    self.reset_timer()  # Reset to kid pomodoro time
                    self.start_timer()  # Automatically start
                else:
                    # Normal mode: prompt for break
                    QMessageBox.information(self, "Pomodoro", "Đã đến giờ nghỉ!")
                    self.start_break()
            else:  # Break time ended
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Hết Giờ Nghỉ")
                msg_box.setText(
                    "Đã hết giờ nghỉ! Bấm OK để bắt đầu thời gian làm việc."
                )
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()

                # Sau khi người dùng đóng thông báo, tự động bắt đầu thời gian làm việc
                self.on_break = False
                self.current_time = self.pomodoro_time
                self.time_display.setText(self.format_time(self.current_time))
                self.status_display.setText("Thời Gian Tập Trung!")
                self.start_timer()  # Tự động bắt đầu bộ hẹn giờ làm việc

    def start_timer(self):
        if self.current_time <= 0:  # Prevent starting if time is already 0
            self.reset_timer()  # Reset to current mode's pomodoro time

        print(f"[TIMER] Starting timer - Mode: {self.mode}, Time: {self.current_time}s, On break: {self.on_break}")
        self.is_running = True
        self.timer.start(1000)  # Update every second
        self.toggle_buttons(True)
        if not self.on_break:
            self.status_display.setText("Thời Gian Tập Trung!")
        else:
            self.status_display.setText("Thời Gian Nghỉ!")

    def pause_timer(self):
        if self.mode == "kid":
            # In Kid mode, pausing is not allowed
            QMessageBox.warning(
                self, "Không Được Phép", "Chế độ trẻ em không cho phép tạm dừng."
            )
            return

        if self.is_running and not self.on_break:
            # Log elapsed study time if it was a study session and was running
            elapsed_time = self.pomodoro_time - self.current_time
            if elapsed_time > 0:
                print(f"[TIMER] Paused. Logging {elapsed_time} seconds for mode: {self.mode}")
                self.db_manager.add_study_session(elapsed_time, self.mode)
                print(f"[TIMER] Study session logged successfully on pause.")
                logging.info(f"Logged {elapsed_time} seconds study time on pause.")

        self.is_running = False
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.skip_button.setEnabled(True)
        if not self.on_break:
            self.status_display.setText("Pomodoro Tạm Dừng")
        else:
            self.status_display.setText("Nghỉ Tạm Dừng")

    def reset_timer(self):
        # Log elapsed study time if it was a study session and was running
        if self.is_running and not self.on_break:
            elapsed_time = self.pomodoro_time - self.current_time
            if elapsed_time > 0:
                print(f"[TIMER] Reset. Logging {elapsed_time} seconds for mode: {self.mode}")
                self.db_manager.add_study_session(elapsed_time, self.mode)
                print(f"[TIMER] Study session logged successfully on reset.")
                logging.info(f"Logged {elapsed_time} seconds study time on reset.")

        self.timer.stop()
        self.is_running = False
        self.on_break = False
        # Reset current_time based on current mode
        self.current_time = (
            self.pomodoro_time
        )  # This will be set by set_X_mode functions
        self.time_display.setText(self.format_time(self.current_time))
        self.status_display.setText("Sẵn sàng cho Pomodoro!")
        self.toggle_buttons(False)

    def skip_phase(self):
        if self.mode == "kid":
            # In Kid mode, skipping is not allowed
            QMessageBox.warning(
                self, "Không Được Phép", "Chế độ trẻ em không cho phép bỏ qua."
            )
            return

        self.timer.stop()
        self.is_running = False
        if not self.on_break:  # If in Pomodoro, start break
            self.pomodoro_count += 1
            QMessageBox.information(
                self, "Bỏ Qua Pomodoro", "Chuyển sang thời gian nghỉ!"
            )
            self.start_break()
        else:  # If in break time, go back to Pomodoro
            QMessageBox.information(
                self, "Bỏ Qua Thời Gian Nghỉ", "Chuyển lại thời gian tập trung!"
            )
            self.reset_timer()  # Reset to Pomodoro
        self.toggle_buttons(False)

    def start_break(self):
        # Kid mode does not have breaks, so this function should not be called in kid mode.
        # However, adding a check just in case.
        if self.mode == "kid":
            return

        self.on_break = True
        if self.pomodoro_count % 4 == 0 and self.pomodoro_count > 0:
            self.current_time = self.long_break_time
            self.status_display.setText("Thời Gian Nghỉ Dài!")
        else:
            self.current_time = self.short_break_time
            self.status_display.setText("Thời Gian Nghỉ Ngắn!")
        self.time_display.setText(self.format_time(self.current_time))
        self.start_timer()
        

    def set_pomodoro_time(self, minutes):
        if self.mode == "normal":  # Only allow changing in normal mode
            self.pomodoro_time = minutes * 60
            if not self.is_running and not self.on_break:
                self.current_time = self.pomodoro_time
                self.time_display.setText(self.format_time(self.current_time))

    def set_short_break_time(self, minutes):
        if self.mode == "normal":  # Only allow changing in normal mode
            self.short_break_time = minutes * 60
            if (
                not self.is_running
                and self.on_break
                and (self.pomodoro_count % 4 != 0 or self.pomodoro_count == 0)
            ):
                self.current_time = self.short_break_time
                self.time_display.setText(self.format_time(self.current_time))

    def set_long_break_time(self, minutes):
        if self.mode == "normal":  # Only allow changing in normal mode
            self.long_break_time = minutes * 60
            if (
                not self.is_running
                and self.on_break
                and (self.pomodoro_count % 4 == 0 and self.pomodoro_count > 0)
            ):
                self.current_time = self.long_break_time
                self.time_display.setText(self.format_time(self.current_time))

    def toggle_buttons(self, timer_is_running):
        self.start_button.setEnabled(not timer_is_running and not self.on_break)
        self.reset_button.setEnabled(
            self.mode == "normal"
        )  # Allow reset only in normal mode

        if self.mode == "kid":
            self.pause_button.setEnabled(False)
            self.skip_button.setEnabled(False)
            self.pomodoro_spinbox.setEnabled(False)
            self.short_break_spinbox.setEnabled(False)
            self.long_break_spinbox.setEnabled(False)
            self.normal_mode_button.setEnabled(True)  # Can switch back to normal
            self.kid_mode_button.setEnabled(False)  # Already in kid mode
            self.change_password_button.setEnabled(
                False
            )  # Cannot change password in kid mode
        else:  # Normal mode
                self.pause_button.setEnabled(timer_is_running)
                self.skip_button.setEnabled(timer_is_running or self.on_break)

                if self.on_break:
                    self.skip_button.setText("Bỏ Qua Nghỉ")
                else:
                    self.skip_button.setText("Bỏ Qua")

                self.pomodoro_spinbox.setEnabled(True)
                self.short_break_spinbox.setEnabled(True)
                self.long_break_spinbox.setEnabled(True)
                self.normal_mode_button.setEnabled(False)
                self.kid_mode_button.setEnabled(True)
                self.change_password_button.setEnabled(True)

              # Can change password in normal mode

    def set_normal_mode(self):
        # Check if currently in kid mode and require password
        if self.mode == "kid":
            admin_password_hash = self.db_manager.get_admin_password_hash()
            admin_password_set = bool(admin_password_hash)

            dialog = PasswordChangeDialog(self, admin_password_set=admin_password_set)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                input_password, change_password_checked = dialog.get_data()

                if not admin_password_set:
                    # No password set, prompt to set one
                    if input_password:
                        new_password, ok_new = QInputDialog.getText(
                            self,
                            "Đặt Mật Khẩu Admin",
                            "Chưa có mật khẩu Admin. Vui lòng đặt mật khẩu mới:",
                            QLineEdit.EchoMode.Password,
                        )
                        if ok_new and new_password:
                            confirm_password, ok_confirm = QInputDialog.getText(
                                self,
                                "Xác Nhận Mật Khẩu",
                                "Xác nhận mật khẩu Admin mới:",
                                QLineEdit.EchoMode.Password,
                            )
                            if ok_confirm and new_password == confirm_password:
                                self.db_manager.set_admin_password(new_password)
                                QMessageBox.information(
                                    self, "Thành Công", "Mật khẩu Admin đã được đặt."
                                )
                                self._apply_normal_mode_settings()
                            else:
                                QMessageBox.warning(
                                    self,
                                    "Lỗi",
                                    "Mật khẩu xác nhận không khớp hoặc trống.",
                                )
                                self.toggle_buttons(self.is_running)
                        else:
                            QMessageBox.warning(
                                self, "Hủy Bỏ", "Đặt mật khẩu Admin đã bị hủy."
                            )
                            self.toggle_buttons(self.is_running)
                    else:
                        QMessageBox.warning(
                            self, "Lỗi", "Mật khẩu không được để trống khi đặt mới."
                        )
                        self.toggle_buttons(self.is_running)

                else:  # Admin password is set
                    if (
                        self.db_manager.hash_password(input_password)
                        == admin_password_hash
                    ):
                        self._apply_normal_mode_settings()
                        if change_password_checked:
                            self.change_admin_password()
                    else:
                        QMessageBox.warning(
                            self, "Lỗi Mật Khẩu", "Mật khẩu không đúng."
                        )
                        self.toggle_buttons(self.is_running)
            else:
                # User cancelled password entry
                self.toggle_buttons(self.is_running)
        else:
            # If already in normal mode, just ensure UI is updated
            self._apply_normal_mode_settings()

    def _apply_normal_mode_settings(self):
        """Applies the settings for normal mode."""
        self.mode = "normal"
        self.pomodoro_time = self.normal_pomodoro_time
        self.short_break_time = self.normal_short_break_time
        self.long_break_time = self.normal_long_break_time
        self.pomodoro_count = 0  # Reset pomodoro count when changing mode
        self.reset_timer()  # Resets current_time to pomodoro_time based on new mode
        self.status_display.setText("Sẵn sàng cho Pomodoro (Chế Độ Thường)!")
        self.toggle_buttons(False)  # Update button states
        self.app.apply_mode_restrictions("normal")

    def set_kid_mode(self):
        self.mode = "kid"
        self.pomodoro_time = self.kid_pomodoro_time
        # For kid mode, breaks are not allowed, so reset them to 0 or handle logic to skip them
        self.app.apply_mode_restrictions("kid")
        self.short_break_time = 0
        self.long_break_time = 0
        self.pomodoro_count = 0  # Reset pomodoro count when changing mode
        self.reset_timer()  # Resets current_time to pomodoro_time based on new mode
        self.status_display.setText("Sẵn sàng cho Pomodoro (Chế Độ Trẻ Em)!")
        self.toggle_buttons(False)  # Update button states

    def change_admin_password(self):
        admin_password_hash = self.db_manager.get_admin_password_hash()

        if not admin_password_hash:
            # No password set, prompt to set one directly
            new_password, ok = QInputDialog.getText(
                self,
                "Đặt Mật Khẩu Admin",
                "Chưa có mật khẩu Admin. Vui lòng đặt mật khẩu mới:",
                QLineEdit.EchoMode.Password,
            )
            if ok and new_password:
                confirm_password, ok_confirm = QInputDialog.getText(
                    self,
                    "Xác Nhận Mật Khẩu",
                    "Xác nhận mật khẩu Admin mới:",
                    QLineEdit.EchoMode.Password,
                )
                if ok_confirm and new_password == confirm_password:
                    self.db_manager.set_admin_password(new_password)
                    QMessageBox.information(
                        self, "Thành Công", "Mật khẩu Admin đã được đặt."
                    )
                else:
                    QMessageBox.warning(
                        self, "Lỗi", "Mật khẩu xác nhận không khớp hoặc trống."
                    )
            else:
                QMessageBox.warning(self, "Hủy Bỏ", "Đặt mật khẩu Admin đã bị hủy.")
        else:
            # Password exists, prompt for current password
            current_password, ok = QInputDialog.getText(
                self,
                "Đổi Mật Khẩu Admin",
                "Nhập mật khẩu Admin hiện tại:",
                QLineEdit.EchoMode.Password,
            )
            if (
                ok
                and self.db_manager.hash_password(current_password)
                == admin_password_hash
            ):
                new_password, ok_new = QInputDialog.getText(
                    self,
                    "Đổi Mật Khẩu Admin",
                    "Nhập mật khẩu Admin mới:",
                    QLineEdit.EchoMode.Password,
                )
                if ok_new and new_password:
                    confirm_password, ok_confirm = QInputDialog.getText(
                        self,
                        "Xác Nhận Mật Khẩu",
                        "Xác nhận mật khẩu Admin mới:",
                        QLineEdit.EchoMode.Password,
                    )
                    if ok_confirm and new_password == confirm_password:
                        self.db_manager.set_admin_password(new_password)
                        QMessageBox.information(
                            self, "Thành Công", "Mật khẩu Admin đã được đổi."
                        )
                    else:
                        QMessageBox.warning(
                            self, "Lỗi", "Mật khẩu xác nhận không khớp hoặc trống."
                        )
                elif ok_new:  # User entered an empty new password
                    QMessageBox.warning(
                        self, "Lỗi", "Mật khẩu mới không được để trống."
                    )
            elif ok:  # Current password was entered but incorrect
                QMessageBox.warning(
                    self, "Lỗi Mật Khẩu", "Mật khẩu hiện tại không đúng."
                )
            else:  # User cancelled current password entry
                QMessageBox.information(self, "Hủy Bỏ", "Đổi mật khẩu Admin đã bị hủy.")
