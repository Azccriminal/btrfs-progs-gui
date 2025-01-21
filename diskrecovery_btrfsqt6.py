import sys
import re
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QCheckBox, QGroupBox, QFormLayout, QFileDialog, QComboBox, QHBoxLayout, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class BtrfsRestoreUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Btrfs Restore")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet(self.get_styles())
        self.create_main_menu()

    def get_styles(self):
        return """
            QWidget {
                background-color: #2C2F36;
                color: white;
            }

            QLineEdit {
                font-size: 16px;
                background-color: #444A53;
                color: white;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 20px;
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
                padding: 20px;
                text-align: left;
                border: none;
                margin: 10px;
            }

            QPushButton:hover {
                background-color: #4A4F57;
            }

            QPushButton:pressed {
                background-color: #2E353F;
            }

            QPushButton#warningButton {
                background-color: #D9534F;
                color: white;
                font-size: 12px;
                padding: 5px;
                margin-top: 5px;
            }

            QCheckBox {
                font-size: 16px;
                color: #A6A6A6;
            }

            QGroupBox {
                border: 1px solid #555;
                border-radius: 10px;
                margin-top: 20px;
                padding: 10px;
            }

            QComboBox {
                background-color: #444A53;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }

            QLabel#warningLabel {
                color: #D9534F;
                font-size: 12px;
            }

            QScrollArea {
                background-color: #2C2F36;
            }
        """

    def create_main_menu(self):
        """ Create the main menu with dynamic clickable options """
        menu_layout = QVBoxLayout()

        # Device Selection using lsblk
        self.device_select = QComboBox(self)
        self.device_select.addItem("Select a disk...")
        self.populate_device_list()
        menu_layout.addWidget(self.device_select)

        # Button to open file manager for selecting restore path
        self.select_restore_path_button = QPushButton("Select Restore Path", self)
        self.select_restore_path_button.clicked.connect(self.open_file_dialog)
        menu_layout.addWidget(self.select_restore_path_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.execute_back_command)
        menu_layout.addWidget(self.back_button)
        # Options for Btrfs Restore
        options_group = QGroupBox("Restore Options", self)
        options_layout = QFormLayout()

        self.dry_run_checkbox = QCheckBox("Dry run (list files to be recovered)", self)
        options_layout.addRow(self.dry_run_checkbox)

        self.ignore_errors_checkbox = QCheckBox("Ignore errors", self)
        options_layout.addRow(self.ignore_errors_checkbox)

        self.overwrite_checkbox = QCheckBox("Overwrite existing files", self)
        options_layout.addRow(self.overwrite_checkbox)

        self.metadata_checkbox = QCheckBox("Restore metadata (owner, mode, times)", self)
        options_layout.addRow(self.metadata_checkbox)

        self.symlink_checkbox = QCheckBox("Restore symbolic links", self)
        options_layout.addRow(self.symlink_checkbox)

        self.subvolume_checkbox = QCheckBox("Recover using Btrfs subvolume", self)
        options_layout.addRow(self.subvolume_checkbox)

        options_group.setLayout(options_layout)
        menu_layout.addWidget(options_group)

        # File Restore Button
        self.restore_data_button = QPushButton("Restore Data", self)
        self.restore_data_button.clicked.connect(self.start_restore)
        menu_layout.addWidget(self.restore_data_button)

        # Warning Message next to the "Restore Data" button
        self.warning_label = QLabel("WARNING: FILE BRICK! BACKUP FILE AND DISK STRUCTURE", self)
        self.warning_label.setObjectName("warningLabel")
        menu_layout.addWidget(self.warning_label)

        # Button for Btrfs Subvolume creation
        self.create_subvolume_button = QPushButton("Create Btrfs Subvolume", self)
        self.create_subvolume_button.clicked.connect(self.create_btrfs_subvolume)
        menu_layout.addWidget(self.create_subvolume_button)

        # Button to list subvolumes
        self.list_subvolumes_button = QPushButton("List Subvolumes", self)
        self.list_subvolumes_button.clicked.connect(self.list_subvolumes)
        menu_layout.addWidget(self.list_subvolumes_button)

        # Output label for status messages
        self.output_label = QLabel("", self)
        menu_layout.addWidget(self.output_label)

        self.setLayout(menu_layout)
    
    def populate_device_list(self):
        """ Populate the combo box with devices from lsblk """
        try:
            result = subprocess.run(["lsblk", "-o", "NAME,SIZE"], capture_output=True, text=True)
            if result.returncode == 0:
                devices = result.stdout.splitlines()[1:]
                for device in devices:
                    device_name = device.split()[0]
                    self.device_select.addItem(f"/dev/{device_name}")
        except Exception as e:
            self.output_label.setText(f"Error fetching devices: {str(e)}")
            
    def open_file_dialog(self):
        """ Open a file dialog for selecting the restore path """
        restore_path = QFileDialog.getExistingDirectory(self, "Select Restore Path")
        if restore_path:
            self.output_label.setText(f"Restore path: {restore_path}")

    def start_restore(self):
        """ Trigger btrfs restore process """
        device = self.device_select.currentText()
        restore_path = self.output_label.text().replace("Restore path: ", "")

        if not device or device == "Select a disk...":
            self.output_label.setText("Please select a valid device.")
            return

        if not restore_path:
            self.output_label.setText("Please select a restore path.")
            return

        # Constructing the restore command
        command = f"btrfs restore {device} {restore_path}"

        # Add selected options to the command
        if self.dry_run_checkbox.isChecked():
            command += " -D"
        if self.ignore_errors_checkbox.isChecked():
            command += " -i"
        if self.overwrite_checkbox.isChecked():
            command += " -o"
        if self.metadata_checkbox.isChecked():
            command += " -m"
        if self.symlink_checkbox.isChecked():
            command += " -S"
        if self.subvolume_checkbox.isChecked():
            command += " -s"

        try:
            # Run the btrfs restore command
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            self.output_label.setText(f"Restore successful: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.output_label.setText(f"Error: {e.stderr}")

    def create_btrfs_subvolume(self):
        """ Create a new Btrfs subvolume """
        device = self.device_select.currentText()
        if not device or device == "Select a disk...":
            self.output_label.setText("Please select a valid device.")
            return

        try:
            result = subprocess.run(f"sudo btrfs subvolume create {device}/subvolume_name", shell=True, check=True, text=True, capture_output=True)
            self.output_label.setText(f"Subvolume created: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.output_label.setText(f"Error creating subvolume: {e.stderr}")

    def list_subvolumes(self):
        """ List all Btrfs subvolumes for the selected device """
        device = self.device_select.currentText()
        if not device or device == "Select a disk...":
            self.output_label.setText("Please select a valid device.")
            return

        try:
            # List all subvolumes for the selected device
            result = subprocess.run(f"sudo btrfs subvolume list {device}", shell=True, check=True, text=True, capture_output=True)
            subvolumes = result.stdout.strip()
            if subvolumes:
                self.output_label.setText(f"Subvolumes:\n{subvolumes}")
            else:
                self.output_label.setText("No subvolumes found.")
        except subprocess.CalledProcessError as e:
            self.output_label.setText(f"Error listing subvolumes: {e.stderr}")
    def execute_back_command(self):
        try:
            result = subprocess.run(["./main-btrfsqt6"], check=True, text=True, capture_output=True)
            self.output_label.setText(f"Back command executed successfully: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.output_label.setText(f"Error executing back command: {e.stderr}")

    def contextMenuEvent(self, event):
       context_menu = QMenu(self)
       copy_action = context_menu.addAction("Copy")
       action = context_menu.exec(event.globalPos())

       if action == copy_action:
            clipboard = QApplication.clipboard()
            if self.output_label.hasFocus():
                clipboard.setText(self.output_label.text())
            elif self.device_select.hasFocus():
                clipboard.setText(self.device_select.currentText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BtrfsRestoreUI()
    window.show()
    sys.exit(app.exec())
