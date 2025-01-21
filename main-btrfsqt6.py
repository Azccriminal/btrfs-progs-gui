import sys
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import os

class MainBtrfsQt6(QMainWindow):
    def __init__(self):
        super().__init__()

        # Apply custom styles
        self.apply_styles()

        # Set up main window
        self.setWindowTitle("Executable Menu Example")
        self.setGeometry(100, 100, 600, 400)

        # Create a layout to hold the buttons
        layout = QVBoxLayout()

        # List of executables and their labels
        executables = [
            ("Device Manager", "devicemanager_btrfsqt6"),
            ("Disk Balance", "diskbalance_btrfsqt6"),
            ("Disk Quota", "diskquota_btrfsqt6"),
            ("Disk Recovery", "diskrecovery_btrfsqt6"),
            ("Disk Scrub", "diskscrub_btrfsqt6"),
            ("Filesystem Property", "filesystem_btrfsqt6"),
            ("Rescue", "rescue_btrfsqt6"),
            ("Subvolume", "subvolume_btrfsqt6")
        ]

        for label, executable_name in executables:
            button = self.create_popup_button(label, executable_name)
            layout.addWidget(button)

        # Create a central widget and set the layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def apply_styles(self):
        """Apply the CSS styles to the window."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2C2F36;
                color: white;
            }

            QLabel {
                font-size: 16px;
                color: #A6A6A6;
                margin-bottom: 5px;
            }

            QPushButton {
                font-size: 20px;
                background-color: #3A3F47;
                border-radius: 10px;
                color: white;
                padding: 10px;
                text-align: center;
                border: none;
                margin-bottom: 10px;
            }

            QPushButton:hover {
                background-color: #4A4F57;
            }

            QPushButton:pressed {
                background-color: #2E353F;
            }

            QTextEdit {
                background-color: #444A53;
                color: white;
                font-family: Consolas, monospace;
                font-size: 14px;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
            }

            QTextEdit:focus {
                border-color: #4A90E2;
            }
        """)

    def create_popup_button(self, label, executable_name):
        """Create a styled button that acts like a popup."""
        button = QPushButton(label, self)
        button.clicked.connect(lambda: self.run_executable(executable_name))
        
        # Set the cursor to a pointing hand when hovering over the button
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        return button

    def run_executable(self, executable_name):
        """Run the executable when menu item is clicked."""
        try:
            # Assuming the executables are in the current working directory or a predefined directory
            executable_path = f"./{executable_name}"  # You can set an absolute path if needed

            # Check if the file exists and is executable
            if os.path.exists(executable_path) and os.access(executable_path, os.X_OK):
                subprocess.run([executable_path], check=True)
            else:
                print(f"Executable '{executable_name}' not found or not executable.")
        except Exception as e:
            print(f"Error running executable: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainBtrfsQt6()
    window.show()
    sys.exit(app.exec())
