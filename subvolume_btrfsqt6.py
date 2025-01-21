import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QComboBox, QLineEdit
from PyQt6.QtCore import Qt

class BtrfsSubvolumeGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Btrfs Subvolume Management")
        self.setGeometry(200, 200, 600, 500)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Title Label
        self.title = QLabel("Btrfs Subvolume Management", self)
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

        # Subvolume Path Input
        self.subvol_path_input = QLineEdit(self)
        self.subvol_path_input.setStyleSheet(self.get_styles())
        self.subvol_path_input.setPlaceholderText("Enter subvolume path")
        main_layout.addWidget(self.subvol_path_input)

        # Subvolume Name Input
        self.subvol_name_input = QLineEdit(self)
        self.subvol_name_input.setStyleSheet(self.get_styles())
        self.subvol_name_input.setPlaceholderText("Enter subvolume name")
        main_layout.addWidget(self.subvol_name_input)

        # Create Subvolume Button
        self.create_subvol_button = QPushButton("Create Subvolume", self)
        self.create_subvol_button.setStyleSheet(self.get_styles())
        self.create_subvol_button.clicked.connect(self.create_subvolume_action)
        main_layout.addWidget(self.create_subvol_button)

        # Delete Subvolume Button
        self.delete_subvol_button = QPushButton("Delete Subvolume", self)
        self.delete_subvol_button.setStyleSheet(self.get_styles())
        self.delete_subvol_button.clicked.connect(self.delete_subvolume_action)
        main_layout.addWidget(self.delete_subvol_button)

        # List Subvolumes Button
        self.list_subvol_button = QPushButton("List Subvolumes", self)
        self.list_subvol_button.setStyleSheet(self.get_styles())
        self.list_subvol_button.clicked.connect(self.list_subvolumes_action)
        main_layout.addWidget(self.list_subvol_button)

        # Snapshot Subvolume Button
        self.snapshot_subvol_button = QPushButton("Snapshot Subvolume", self)
        self.snapshot_subvol_button.setStyleSheet(self.get_styles())
        self.snapshot_subvol_button.clicked.connect(self.snapshot_subvolume_action)
        main_layout.addWidget(self.snapshot_subvol_button)

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

            QComboBox, QLineEdit {
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

    def execute_back_command(self):
        try:
            result = subprocess.run(["./main-btrfsqt6"], check=True, text=True, capture_output=True)
            self.output_label.setText(f"Back command executed successfully: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.output_label.setText(f"Error executing back command: {e.stderr}")
    
    def create_subvolume_action(self):
        device = self.device_combo.currentText()
        path = self.subvol_path_input.text().strip()
        name = self.subvol_name_input.text().strip()
        if device != "Select a device" and path and name:
            self.run_btrfs_command(f"subvolume create {device}/{path}/{name}")
        else:
            self.output_display.setPlainText("Please fill in all fields and select a device.")

    def delete_subvolume_action(self):
        device = self.device_combo.currentText()
        path = self.subvol_path_input.text().strip()
        if device != "Select a device" and path:
            self.run_btrfs_command(f"subvolume delete {device}/{path}")
        else:
            self.output_display.setPlainText("Please provide a valid subvolume path and select a device.")

    def list_subvolumes_action(self):
        device = self.device_combo.currentText()
        if device != "Select a device":
            self.run_btrfs_command(f"subvolume list {device}")
        else:
            self.output_display.setPlainText("Please select a device.")

    def snapshot_subvolume_action(self):
        device = self.device_combo.currentText()
        path = self.subvol_path_input.text().strip()
        name = self.subvol_name_input.text().strip()
        if device != "Select a device" and path and name:
            self.run_btrfs_command(f"subvolume snapshot {device}/{path} {device}/{path}/{name}")
        else:
            self.output_display.setPlainText("Please provide a valid subvolume path, name, and select a device.")

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
    window = BtrfsSubvolumeGUI()
    window.show()
    sys.exit(app.exec())
