from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
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
from src.ai.summarizer import TextSummarizer


class NotesTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.summarizer = TextSummarizer("english")  # Initialize summarizer
        self.current_note_id = None
        self.init_ui()
        self.load_notes()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Left panel for note list
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Tất Cả Ghi Chú:"))

        self.note_list_widget = QListWidget()
        self.note_list_widget.itemClicked.connect(self.display_note)
        left_panel.addWidget(self.note_list_widget)

        self.add_note_button = QPushButton("Thêm Ghi Chú Mới")
        self.add_note_button.clicked.connect(self.add_new_note)
        left_panel.addWidget(self.add_note_button)

        main_layout.addLayout(left_panel, 1)

        # Right panel for note content and summarization
        right_panel = QVBoxLayout()

        # Note editing section
        note_edit_group = QVBoxLayout()
        note_edit_group.addWidget(QLabel("Nội Dung Ghi Chú:"))

        self.note_title_input = QLineEdit()
        self.note_title_input.setPlaceholderText("Tiêu Đề Ghi Chú")
        note_edit_group.addWidget(self.note_title_input)

        self.note_content_input = QTextEdit()
        self.note_content_input.setPlaceholderText("Nội Dung Ghi Chú")
        note_edit_group.addWidget(self.note_content_input)

        button_layout = QHBoxLayout()
        self.save_note_button = QPushButton("Lưu Ghi Chú")
        self.save_note_button.clicked.connect(self.save_note)
        self.save_note_button.setEnabled(False)
        button_layout.addWidget(self.save_note_button)

        self.delete_note_button = QPushButton("Xóa Ghi Chú")
        self.delete_note_button.clicked.connect(self.delete_note)
        self.delete_note_button.setEnabled(False)
        button_layout.addWidget(self.delete_note_button)
        note_edit_group.addLayout(button_layout)

        # Summarization section
        summary_group = QVBoxLayout()
        summary_group.addWidget(QLabel("Bản Tóm Tắt:"))

        self.summary_output = QTextEdit()
        self.summary_output.setReadOnly(True)
        self.summary_output.setPlaceholderText("Bản tóm tắt sẽ xuất hiện ở đây.")
        summary_group.addWidget(self.summary_output)

        self.summarize_button = QPushButton("Tóm Tắt Ghi Chú")
        self.summarize_button.clicked.connect(self.summarize_note)
        self.summarize_button.setEnabled(False)  # Disable until content is loaded
        summary_group.addWidget(self.summarize_button)

        right_panel.addLayout(note_edit_group)
        right_panel.addStretch()  # Push summarization section down a bit
        right_panel.addLayout(summary_group)
        main_layout.addLayout(right_panel, 3)

        self.clear_note_fields()

    def load_notes(self):
        self.note_list_widget.clear()
        notes = (
            self.db_manager.get_all_notes()
        )  # This function needs to be implemented in db_manager
        for note in notes:
            item = QListWidgetItem(note[1])  # note[1] is the title
            item.setData(Qt.ItemDataRole.UserRole, note[0])  # note[0] is the id
            self.note_list_widget.addItem(item)
        self.clear_note_fields()

    def display_note(self, item):
        note_id = item.data(Qt.ItemDataRole.UserRole)
        note = self.db_manager.get_note_by_id(
            note_id
        )  # This function needs to be implemented
        if note:
            self.current_note_id = note[0]
            self.note_title_input.setText(note[1])
            self.note_content_input.setText(note[2])
            self.save_note_button.setEnabled(True)
            self.delete_note_button.setEnabled(True)
            self.summarize_button.setEnabled(
                True
            )  # Enable summarize button when a note is displayed
            self.summary_output.clear()  # Clear previous summary
        else:
            self.clear_note_fields()

    def add_new_note(self):
        self.clear_note_fields()
        self.current_note_id = None
        self.save_note_button.setEnabled(True)
        self.delete_note_button.setEnabled(False)
        self.summarize_button.setEnabled(False)  # Disable summarize for new empty note
        self.note_title_input.setFocus()

    def save_note(self):
        title = self.note_title_input.text().strip()
        content = self.note_content_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(
                self, "Lỗi Nhập Liệu", "Tiêu đề ghi chú không được để trống."
            )
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.current_note_id is None:
            # Add new note
            self.db_manager.add_note(
                title, content, current_time, current_time
            )  # This needs to be implemented
            QMessageBox.information(
                self, "Thành Công", "Ghi chú đã được thêm thành công!"
            )
        else:
            # Update existing note
            self.db_manager.update_note(
                self.current_note_id, title, content, current_time
            )  # This needs to be implemented
            QMessageBox.information(
                self, "Thành Công", "Ghi chú đã được cập nhật thành công!"
            )

        self.load_notes()
        self.clear_note_fields()  # This will disable summarize button too

    def delete_note(self):
        if self.current_note_id is None:
            return

        reply = QMessageBox.question(
            self,
            "Xác Nhận Xóa",
            "Bạn có chắc chắn muốn xóa ghi chú này không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_note(
                self.current_note_id
            )  # This needs to be implemented
            QMessageBox.information(
                self, "Thành Công", "Ghi chú đã được xóa thành công!"
            )
            self.load_notes()
            self.clear_note_fields()

    def summarize_note(self):
        content = self.note_content_input.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, "Lỗi Tóm Tắt", "Không có nội dung để tóm tắt.")
            self.summary_output.clear()
            return
        
        try:
            summary = self.summarizer.summarize_text(content, sentences_count=5)
            self.summary_output.setText(summary)
            
            # Auto-save to database for both summary tab and statistics
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            note_title = self.note_title_input.text().strip() or "Không có tiêu đề"
            
            if self.current_note_id is not None:
                # Save summary with note_id
                result = self.db_manager.save_note_summary(
                    self.current_note_id, 
                    note_title, 
                    content, 
                    summary, 
                    current_time
                )
                if result:
                    QMessageBox.information(
                        self, 
                        "Thành Công", 
                        "Tóm tắt đã được lưu vào thống kê học tập!"
                    )
                    # Explicit database commit before refresh
                    self.db_manager.conn.commit()
                    # Refresh summary and statistics tabs
                    self.refresh_other_tabs()
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể lưu tóm tắt!")
            else:
                # For new notes, ask to save note first
                reply = QMessageBox.question(
                    self,
                    "Lưu Tóm Tắt",
                    "Bạn có muốn lưu ghi chú này trước khi lưu tóm tắt không?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.save_note()  # Save note first
                    # Now save summary with new note_id
                    if self.current_note_id is not None:
                        result = self.db_manager.save_note_summary(
                            self.current_note_id, 
                            note_title, 
                            content, 
                            summary, 
                            current_time
                        )
                        if result:
                            QMessageBox.information(
                                self, 
                                "Thành Công", 
                                "Ghi chú và tóm tắt đã được lưu vào thống kê học tập!"
                            )
                            # Explicit database commit before refresh
                            self.db_manager.conn.commit()
                            # Refresh summary and statistics tabs
                            self.refresh_other_tabs()
                        else:
                            QMessageBox.warning(self, "Lỗi", "Không thể lưu tóm tắt!")
                        
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Tóm Tắt AI", f"Đã xảy ra lỗi khi tóm tắt: {e}")
            self.summary_output.clear()

    def refresh_other_tabs(self):
        """Refresh summary and statistics tabs to show new data"""
        try:
            # Force database commit first
            self.db_manager.conn.commit()
            
            # Get the main application instance through tab widget
            parent = self.parent()
            while parent and not hasattr(parent, 'tab_widget'):
                parent = parent.parent()
            
            if parent and hasattr(parent, 'tab_widget'):
                # Find the summary and statistics tabs
                for i in range(parent.tab_widget.count()):
                    tab = parent.tab_widget.widget(i)
                    if hasattr(tab, 'load_summaries'):
                        # Force database commit for this tab
                        try:
                            tab.db_manager.conn.commit()
                        except:
                            pass
                        tab.load_summaries()
                    elif hasattr(tab, 'load_statistics'):
                        # Force database commit for this tab
                        try:
                            tab.db_manager.conn.commit()
                        except:
                            pass
                        tab.load_statistics()
        except Exception as e:
            print(f"Error refreshing tabs: {e}")

    def clear_note_fields(self):
        self.current_note_id = None
        self.note_title_input.clear()
        self.note_content_input.clear()
        self.save_note_button.setEnabled(False)
        self.delete_note_button.setEnabled(False)
        self.summarize_button.setEnabled(False)  # Disable summarize button
        self.summary_output.clear()  # Clear summary output

    def apply_mode_restrictions(self, restricted):
        """Disables editing and summarization features in Kid Mode."""
        self.add_note_button.setEnabled(not restricted)
        self.note_title_input.setReadOnly(restricted)
        self.note_content_input.setReadOnly(restricted)
        self.summary_output.setReadOnly(True)  # Always read-only for summary output

        if restricted:
            self.save_note_button.setEnabled(False)
            self.delete_note_button.setEnabled(False)
            self.summarize_button.setEnabled(False)
        else:
            # Restore button states based on selection
            if self.current_note_id is not None:
                self.save_note_button.setEnabled(True)
                self.delete_note_button.setEnabled(True)
                self.summarize_button.setEnabled(True)
            else:
                self.summarize_button.setEnabled(False)  # For new/empty note
