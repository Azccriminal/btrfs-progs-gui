import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit, QGroupBox
)
from PyQt6.QtCore import Qt


class BtrfsBalanceDebugger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Btrfs Balance Debugger")
        self.resize(800, 600)
        self.setStyleSheet(self.get_styles())

        # Main Layout
        layout = QVBoxLayout()

        # Command Selector
        command_group = QGroupBox("Btrfs Balance Commands")
        command_layout = QVBoxLayout()
        self.command_select = QComboBox()
        self.command_select.addItems(["start", "pause", "cancel", "resume", "status"])
        command_layout.addWidget(QLabel("Select Command:"))
        command_layout.addWidget(self.command_select)
        command_group.setLayout(command_layout)

        # Path Selector
        path_group = QGroupBox("Select Path")
        path_layout = QVBoxLayout()
        self.path_select = QComboBox()
        self.populate_mount_points()
        path_layout.addWidget(QLabel("Available Paths:"))
        path_layout.addWidget(self.path_select)
        path_group.setLayout(path_layout)

        # Debug Console
        self.debug_console = QTextEdit()
        self.debug_console.setReadOnly(True)
        self.debug_console.setPlaceholderText("Debug output will appear here...")

        # Buttons Layout
        buttons_layout = QHBoxLayout()

        # Run Button
        run_button = QPushButton("Run Command")
        run_button.clicked.connect(self.run_command)
        buttons_layout.addWidget(run_button)

        # Back Button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.run_back_process)
        buttons_layout.addWidget(back_button)

        # Layout Setup
        layout.addWidget(command_group)
        layout.addWidget(path_group)
        layout.addWidget(self.debug_console)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def populate_mount_points(self):
        """Populate the combo box with available mount points."""
        try:
            result = subprocess.run(["lsblk", "-o", "MOUNTPOINT"], capture_output=True, text=True)
            if result.returncode == 0:
                mount_points = result.stdout.splitlines()[1:]
                for mount_point in mount_points:
                    if mount_point.strip():  # Ignore empty entries
                        self.path_select.addItem(mount_point.strip())
            else:
                self.debug_console.append("Error fetching mount points!")
        except Exception as e:
            self.debug_console.append(f"Error: {str(e)}")

    def run_command(self):
        """Run the selected btrfs command and display debug output."""
        command = self.command_select.currentText()
        path = self.path_select.currentText()

        if not path:
            self.debug_console.append("Error: No path selected!")
            return

        try:
            full_command = ["btrfs", "balance", command, path]
            self.debug_console.append(f"Running command: {' '.join(full_command)}")
            result = subprocess.run(full_command, capture_output=True, text=True)

            if result.returncode == 0:
                self.debug_console.append(f"Output:\n{result.stdout}")
            else:
                self.debug_console.append(f"Error:\n{result.stderr}")
        except Exception as e:
            self.debug_console.append(f"Exception: {str(e)}")

    def run_back_process(self):
        """Trigger subprocess for 'btrfsqt6-main.elf64' when Back button is pressed."""
        try:
            # Run the subprocess command for btrfsqt6-main.elf64
            self.debug_console.append("Running btrfsqt6-main.elf64 process...")
            result = subprocess.run(["./btrfsqt6-main.elf64"], capture_output=True, text=True)

            if result.returncode == 0:
                self.debug_console.append(f"Process Output:\n{result.stdout}")
            else:
                self.debug_console.append(f"Error:\n{result.stderr}")
        except Exception as e:
            self.debug_console.append(f"Exception: {str(e)}")

    def get_styles(self):
        return """
            QWidget {
                background-color: #2C2F36;
                color: white;
            }

            QLabel {
                font-size: 16px;
                color: #A6A6A6;
            }

            QPushButton {
                font-size: 20px;
                background-color: #3A3F47;
                border-radius: 10px;
                color: white;
                padding: 10px;
                text-align: center;
                border: none;
            }

            QPushButton:hover {
                background-color: #4A4F57;
            }

            QPushButton:pressed {
                background-color: #2E353F;
            }

            QComboBox {
                background-color: #444A53;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }

            QTextEdit {
                background-color: #444A53;
                color: white;
                font-family: Consolas, monospace;
                font-size: 14px;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 10px;
            }

            QGroupBox {
                border: 1px solid #555;
                border-radius: 10px;
                margin-top: 20px;
                padding: 15px;
            }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BtrfsBalanceDebugger()
    window.show()
    sys.exit(app.exec())
