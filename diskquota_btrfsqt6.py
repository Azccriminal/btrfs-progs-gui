import sys
import subprocess
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QComboBox

class BtrfsQuotaGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Btrfs Disk Quota Management")
        self.setGeometry(200, 200, 600, 500)
        
        self.initUI()

        # Subprocess setup
        self.process = QProcess(self)

    def initUI(self):
        main_layout = QVBoxLayout(self)
        
        # Title Label
        self.title = QLabel("Btrfs Disk Quota Management", self)
        self.title.setStyleSheet("font-size: 24px; color: white;")
        main_layout.addWidget(self.title)

        # Device Selection ComboBox
        self.device_combo = QComboBox(self)
        self.device_combo.setStyleSheet(self.get_styles())
        self.device_combo.addItem("Select a device")
        self.populate_devices()
        main_layout.addWidget(self.device_combo)

        # Enable Quota Button
        self.enable_quota_button = QPushButton("Enable Quota", self)
        self.enable_quota_button.setStyleSheet(self.get_styles())
        self.enable_quota_button.clicked.connect(self.enable_quota_action)
        main_layout.addWidget(self.enable_quota_button)

        # Disable Quota Button
        self.disable_quota_button = QPushButton("Disable Quota", self)
        self.disable_quota_button.setStyleSheet(self.get_styles())
        self.disable_quota_button.clicked.connect(self.disable_quota_action)
        main_layout.addWidget(self.disable_quota_button)

        # Rescan Quota Button
        self.rescan_quota_button = QPushButton("Rescan Quota", self)
        self.rescan_quota_button.setStyleSheet(self.get_styles())
        self.rescan_quota_button.clicked.connect(self.rescan_quota_action)
        main_layout.addWidget(self.rescan_quota_button)

        # Back Button
        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet(self.get_styles())
        self.back_button.clicked.connect(self.back_action)
        main_layout.addWidget(self.back_button)

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

    def enable_quota_action(self):
        device = self.device_combo.currentText()
        if device != "Select a device":
            self.run_btrfs_command(f"quota enable {device}")
        else:
            self.output_display.setPlainText("Please select a device.")

    def disable_quota_action(self):
        device = self.device_combo.currentText()
        if device != "Select a device":
            self.run_btrfs_command(f"quota disable {device}")
        else:
            self.output_display.setPlainText("Please select a device.")

    def rescan_quota_action(self):
        device = self.device_combo.currentText()
        if device != "Select a device":
            self.run_btrfs_command(f"quota rescan {device}")
        else:
            self.output_display.setPlainText("Please select a device.")

    def back_action(self):
        """Back button action: reset the device selection and clear the output."""
        self.device_combo.setCurrentIndex(0)  # Reset ComboBox to default
        self.output_display.clear()  # Clear the output display

        # Optionally terminate the subprocess if running
        self.process.terminate()
        self.output_display.setPlainText("Subprocess terminated.")

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

    def start_subprocess(self):
        """Start the subprocess."""
        self.process.start("./main-btrfsqt6")

        # Capture output from the subprocess
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_error)

    def read_output(self):
        """Read output from subprocess."""
        output = bytes(self.process.readAllStandardOutput()).decode("utf-8")
        self.output_display.append(output)

    def read_error(self):
        """Read error output from subprocess."""
        error = bytes(self.process.readAllStandardError()).decode("utf-8")
        self.output_display.append(error)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BtrfsQuotaGUI()
    window.show()
    sys.exit(app.exec())
