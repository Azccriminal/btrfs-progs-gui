import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QComboBox
from PyQt6.QtCore import Qt

class BtrfsGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Btrfs Device Management")
        self.setGeometry(200, 200, 600, 500)
        
        self.initUI()
    
    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title label
        self.title = QLabel("Btrfs Device Management", self)
        self.title.setStyleSheet("font-size: 24px; color: white;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title)

        # Device selection combo box
        self.device_combo = QComboBox(self)
        self.device_combo.setStyleSheet(self.get_styles())
        self.device_combo.setPlaceholderText("Select or enter a device")
        self.update_device_list()
        main_layout.addWidget(self.device_combo)

        # Manual device input field
        self.device_ready_input = QLineEdit(self)
        self.device_ready_input.setStyleSheet(self.get_styles())
        self.device_ready_input.setPlaceholderText("Or enter device manually")
        main_layout.addWidget(self.device_ready_input)

        # Add device button
        self.add_device_button = QPushButton("Add Device", self)
        self.add_device_button.setStyleSheet(self.get_styles())
        self.add_device_button.clicked.connect(self.add_device_action)
        main_layout.addWidget(self.add_device_button)

        # Remove device button
        self.remove_device_button = QPushButton("Remove Device", self)
        self.remove_device_button.setStyleSheet(self.get_styles())
        self.remove_device_button.clicked.connect(self.remove_device_action)
        main_layout.addWidget(self.remove_device_button)

        # Replace device button
        self.replace_device_button = QPushButton("Replace Device", self)
        self.replace_device_button.setStyleSheet(self.get_styles())
        self.replace_device_button.clicked.connect(self.replace_device_action)
        main_layout.addWidget(self.replace_device_button)

        # Scan devices button
        self.scan_device_button = QPushButton("Scan Devices", self)
        self.scan_device_button.setStyleSheet(self.get_styles())
        self.scan_device_button.clicked.connect(self.scan_device_action)
        main_layout.addWidget(self.scan_device_button)

        # Device stats button
        self.device_stats_button = QPushButton("Device IO Stats", self)
        self.device_stats_button.setStyleSheet(self.get_styles())
        self.device_stats_button.clicked.connect(self.device_stats_action)
        main_layout.addWidget(self.device_stats_button)

        # Device usage button
        self.device_usage_button = QPushButton("Device Usage", self)
        self.device_usage_button.setStyleSheet(self.get_styles())
        self.device_usage_button.clicked.connect(self.device_usage_action)
        main_layout.addWidget(self.device_usage_button)

        # Output display area
        self.output_display = QTextEdit(self)
        self.output_display.setStyleSheet(self.get_styles())
        self.output_display.setReadOnly(True)
        main_layout.addWidget(self.output_display)

        # Back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
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
        """)
        self.back_button.clicked.connect(self.go_back)
        main_layout.addWidget(self.back_button)

        # Set layout
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

            QLineEdit {
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

            QComboBox {
                background-color: #444A53;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
        """

    def update_device_list(self):
        devices = self.get_devices_from_lsblk()
        self.device_combo.clear()
        self.device_combo.addItems(devices)

    def get_devices_from_lsblk(self):
        try:
            result = subprocess.run(['lsblk', '-o', 'NAME,SIZE'], capture_output=True, text=True)
            devices = result.stdout.splitlines()
            return [line.split()[0] for line in devices if line.startswith('sd')]
        except Exception as e:
            self.output_display.setPlainText(f"Error fetching devices: {e}")
            return []

    def add_device_action(self):
        device = self.get_selected_device()
        if device:
            self.run_btrfs_command(f"device add {device} /mnt")
        else:
            self.output_display.setPlainText("Please select or enter a device.")

    def remove_device_action(self):
        device = self.get_selected_device()
        if device:
            self.run_btrfs_command(f"device remove {device} /mnt")
        else:
            self.output_display.setPlainText("Please select or enter a device.")

    def replace_device_action(self):
        device = self.get_selected_device()
        if device:
            self.run_btrfs_command(f"device replace {device} /mnt")
        else:
            self.output_display.setPlainText("Please select or enter a device.")

    def scan_device_action(self):
        self.run_btrfs_command("device scan")

    def device_stats_action(self):
        device = self.get_selected_device()
        if device:
            self.run_btrfs_command(f"device stats {device}")
        else:
            self.output_display.setPlainText("Please select or enter a device.")

    def device_usage_action(self):
        device = self.get_selected_device()
        if device:
            self.run_btrfs_command(f"device usage {device}")
        else:
            self.output_display.setPlainText("Please select or enter a device.")

    def go_back(self):
        try:
            subprocess.run(["./main-btrfsqt6"], check=True)
        except FileNotFoundError:
            print("main-btrfsqt6.elf64 not found!")
        except subprocess.CalledProcessError as e:
            print(f"main-btrfsqt6.elf64 failed to execute: {e}")

    def run_btrfs_command(self, command):
        try:
            result = subprocess.run(['sudo', 'btrfs'] + command.split(), capture_output=True, text=True)
            if result.returncode == 0:
                self.output_display.setPlainText(result.stdout)
            else:
                self.output_display.setPlainText(f"Error: {result.stderr}")
        except Exception as e:
            self.output_display.setPlainText(f"Error executing command: {e}")

    def get_selected_device(self):
        device = self.device_combo.currentText()
        return device if device else self.device_ready_input.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BtrfsGUI()
    window.show()
    sys.exit(app.exec())
