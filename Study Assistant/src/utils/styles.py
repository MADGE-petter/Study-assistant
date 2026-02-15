def get_qss_styles():
    return """
    QMainWindow {
        background-color: #000000; /* Black background */
        font-family: "Segoe UI", "Times New Roman", sans-serif;
        color: #ecf0f1; /* Light text color for general window content */
    }

    QTabWidget::pane {
        border: 1px solid #34495e; /* Darker border for tab pane */
        background: #000000; /* Dark background for tab pane */
    }

    QTabBar::tab {
        background: #3f556d; /* Darker gray for inactive tabs */
        border: 1px solid #34495e;
        border-bottom-color: #3f556d; /* Make it blend with the tab background */
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        min-width: 100px;
        padding: 8px;
        font-size: 14px;
        color: #ecf0f1; /* Light text for inactive tabs */
    }

    QTabBar::tab:selected {
        background: #34495e; /* Background matching the pane for selected tab */
        border-color: #34495e;
        border-bottom-color: #34495e; /* Make the selected tab look like it's connected to the pane */
        color: #2ecc71; /* Green for selected tab text */
        font-weight: bold;
    }

    QTabBar::tab:hover:!selected {
        background: #4a627d; /* Slightly lighter dark gray on hover for unselected tabs */
    }

    QPushButton {
        background-color: #2ecc71; /* Green */
        color: white;
        border: 1px solid #2ecc71;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #27ae60; /* Darker green on hover */
        border-color: #27ae60;
    }

    QPushButton:pressed {
        background-color: #219d54; /* Even darker green on pressed */
        border-color: #219d54;
    }

    QPushButton:disabled {
        background-color: #7f8c8d; /* Gray for disabled buttons */
        border-color: #7f8c8d;
        color: #bdc3c7; /* Lighter gray for disabled text */
    }

    QLabel {
        color: #ecf0f1; /* Light text color */
        font-size: 14px;
    }

    QLineEdit, QTextEdit, QComboBox, QDateEdit, QDateTimeEdit {
        border: 1px solid #34495e; /* Darker border */
        border-radius: 4px;
        padding: 6px;
        font-size: 14px;
        background-color: #4a627d; /* Slightly lighter dark background for inputs */
        color: #ecf0f1; /* Light text for inputs */
    }

    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus, QDateTimeEdit:focus {
        border-color: #2ecc71; /* Green border on focus */
    }

    QComboBox::drop-down {
        border: 0px; /* No border for the arrow button */
    }

    QCheckBox::indicator {
        width: 16px;
        height: 16px;
    }

    QDialog {
        background-color: #000000; /* Black background for dialogs */
        border: 1px solid #34495e;
        border-radius: 8px;
        color: #ecf0f1; /* Light text color for dialogs */
    }

    """
