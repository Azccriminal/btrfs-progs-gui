import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QComboBox
from PyQt6.QtCore import Qt

class BtrfsScrubGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Btrfs Scrub Management")
        self.setGeometry(200, 200, 600, 500)
        
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        
        # Title Label
        self.title = QLabel("Btrfs Scrub Management", self)
        self.title.setStyleSheet("font-size: 24px; color: white;")
        main_layout.addWidget(self.title)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.execute_back_command)
        main_layout.addWidget(self.back_button)

        # Device Selection ComboBox
        self.device_combo = QComboBox(self)
        self.device_combo.setStyleSheet(self.get_styles())
        self.device_combo.addItem("Select a device")
        self.populate_devices()
        main_layout.addWidget(self.device_combo)

        # Start Scrub Button
        self.start_scrub_button = QPushButton("Start Scrub", self)
        self.start_scrub_button.setStyleSheet(self.get_styles())
        self.start_scrub_button.clicked.connect(self.start_scrub_action)
        main_layout.addWidget(self.start_scrub_button)

        # Cancel Scrub Button
        self.cancel_scrub_button = QPushButton("Cancel Scrub", self)
        self.cancel_scrub_button.setStyleSheet(self.get_styles())
        self.cancel_scrub_button.clicked.connect(self.cancel_scrub_action)
        main_layout.addWidget(self.cancel_scrub_button)

        # Resume Scrub Button
        self.resume_scrub_button = QPushButton("Resume Scrub", self)
        self.resume_scrub_button.setStyleSheet(self.get_styles())
        self.resume_scrub_button.clicked.connect(self.resume_scrub_action)
        main_layout.addWidget(self.resume_scrub_button)

        # Status Scrub Button
        self.status_scrub_button = QPushButton("Scrub Status", self)
        self.status_scrub_button.setStyleSheet(self.get_styles())
        self.status_scrub_button.clicked.connect(self.scrub_status_action)
        main_layout.addWidget(self.status_scrub_button)

        # Output Display Area
        self.output_display = QTextEdit(self)
        self.output_display.setStyleSheet(self.get_styles())
        self.output_display.setReadOnly(True)
        main_layout.addWidget(self.output_display)

        # Set Layout
        self.setLayout(main_layout)

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
        """

    def populate_devices(self):
        """Populate the ComboBox with block devices from lsblk."""
        try:
            result = subprocess.run(['lsblk', '--output', 'NAME,MOUNTPOINT'], capture_output=True, text=True)
            if result.returncode == 0:
                # Parse the output to get the list of devices with mount points
                devices = []
                for line in result.stdout.splitlines()[1:]:  # Skip the header line
                    parts = line.split()
                    if len(parts) > 1 and parts[1]:  # Ensure it has a mount point
                        devices.append(parts[1])  # Add the mount point to the list
                for device in devices:
                    self.device_combo.addItem(device)
            else:
                self.output_display.setPlainText(f"Error: {result.stderr}")
        except Exception as e:
            self.output_display.setPlainText(f"Error fetching devices: {e}")

    def start_scrub_action(self):
        device = self.device_combo.currentText()
        if device != "Select a device":
            self.run_btrfs_command(f"scrub start {device}")
        else:
            self.output_display.setPlainText("Please select a device.")

    def cancel_scrub_action(self):
        device = self.device_combo.currentText()
        if device != "Select a device":
            self.run_btrfs_command(f"scrub cancel {device}")
        else:
            self.output_display.setPlainText("Please select a device.")

    def resume_scrub_action(self):
        device = self.device_combo.currentText()
        if device != "Select a device":
            self.run_btrfs_command(f"scrub resume {device}")
        else:
            self.output_display.setPlainText("Please select a device.")

    def scrub_status_action(self):
        device = self.device_combo.currentText()
        if device != "Select a device":
            self.run_btrfs_command(f"scrub status {device}")
        else:
            self.output_display.setPlainText("Please select a device.")
    def execute_back_command(self):
        try:
            result = subprocess.run(["./main-btrfsqt6"], check=True, text=True, capture_output=True)
            self.output_label.setText(f"Back command executed successfully: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.output_label.setText(f"Error executing back command: {e.stderr}")
    
    def run_btrfs_command(self, command):
        """Run the btrfs command and display the output."""
        try:
            result = subprocess.run(['sudo', 'btrfs'] + command.split(), capture_output=True, text=True)
            if result.returncode == 0:
                self.output_display.setPlainText(result.stdout)
            else:
                self.output_display.setPlainText(f"Error: {result.stderr}")
        except Exception as e:
            self.output_display.setPlainText(f"Error executing command: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BtrfsScrubGUI()
    window.show()
    sys.exit(app.exec())
