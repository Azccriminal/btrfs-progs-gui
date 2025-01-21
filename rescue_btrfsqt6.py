import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QComboBox

class BtrfsRescueGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Btrfs Rescue Operations")
        self.setGeometry(200, 200, 600, 500)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Başlık
        self.title = QLabel("Btrfs Rescue Operations", self)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 20px;")
        main_layout.addWidget(self.title)

        # Cihaz Seçimi
        self.device_select_label = QLabel("Select Device:", self)
        self.device_select_label.setStyleSheet("font-size: 16px; color: #A6A6A6;")
        main_layout.addWidget(self.device_select_label)

        
        self.device_combo = QComboBox(self)
        self.device_combo.addItems(self.get_devices())
        main_layout.addWidget(self.device_combo)

        
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.execute_back_command)

        main_layout.addWidget(self.back_button)
       
        self.chunk_recover_button = QPushButton("Chunk Recover", self)
        self.chunk_recover_button.clicked.connect(lambda: self.run_rescue_operation("chunk-recover"))
        main_layout.addWidget(self.chunk_recover_button)

        self.super_recover_button = QPushButton("Superblock Recover", self)
        self.super_recover_button.clicked.connect(lambda: self.run_rescue_operation("super-recover"))
        main_layout.addWidget(self.super_recover_button)

        self.zero_log_button = QPushButton("Zero Log", self)
        self.zero_log_button.clicked.connect(lambda: self.run_rescue_operation("zero-log"))
        main_layout.addWidget(self.zero_log_button)

        self.fix_device_size_button = QPushButton("Fix Device Size", self)
        self.fix_device_size_button.clicked.connect(lambda: self.run_rescue_operation("fix-device-size"))
        main_layout.addWidget(self.fix_device_size_button)

        self.create_control_device_button = QPushButton("Create Control Device", self)
        self.create_control_device_button.clicked.connect(lambda: self.run_rescue_operation("create-control-device"))
        main_layout.addWidget(self.create_control_device_button)

        self.clear_ino_cache_button = QPushButton("Clear Inode Cache", self)
        self.clear_ino_cache_button.clicked.connect(lambda: self.run_rescue_operation("clear-ino-cache"))
        main_layout.addWidget(self.clear_ino_cache_button)

        self.clear_space_cache_button = QPushButton("Clear Space Cache", self)
        self.clear_space_cache_button.clicked.connect(lambda: self.run_rescue_operation("clear-space-cache"))
        main_layout.addWidget(self.clear_space_cache_button)

        self.clear_uuid_tree_button = QPushButton("Clear UUID Tree", self)
        self.clear_uuid_tree_button.clicked.connect(lambda: self.run_rescue_operation("clear-uuid-tree"))
        main_layout.addWidget(self.clear_uuid_tree_button)

        # Çıktı Alanı
        self.output_display = QTextEdit(self)
        self.output_display.setReadOnly(True)
        main_layout.addWidget(self.output_display)

        self.setLayout(main_layout)

        # CSS stillerini uygula
        self.apply_styles()
    def execute_back_command(self):
        try:
            # Running the main-btrfsqt6.elf64 executable
            result = subprocess.run(["./main-btrfsqt6.elf64"], check=True, text=True, capture_output=True)
            self.output_label.setText(f"Back command executed successfully: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.output_label.setText(f"Error executing back command: {e.stderr}")

    def apply_styles(self):
        """CSS stillerini uygulama."""
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

    def get_devices(self):
        """`lsblk` komutunu çalıştırarak mevcut cihazları al."""
        try:
            result = subprocess.run(['lsblk', '-d', '-o', 'NAME'], capture_output=True, text=True)
            devices = result.stdout.splitlines()
            # İlk satır başlık olduğu için onu atlıyoruz
            devices = devices[1:]
            return [f"/dev/{device.strip()}" for device in devices]
        except Exception as e:
            self.output_display.setPlainText(f"Error retrieving devices: {e}")
            return []

    def run_rescue_operation(self, operation):
        """Btrfs rescue komutlarını çalıştır ve sonucu göster."""
        device = self.device_combo.currentText()
        if not device:
            self.output_display.setPlainText("Please select a device.")
            return

        try:
            if operation == "chunk-recover":
                result = subprocess.run(['sudo', 'btrfs', 'rescue', 'chunk-recover', device], capture_output=True, text=True)
            elif operation == "super-recover":
                result = subprocess.run(['sudo', 'btrfs', 'rescue', 'super-recover', device], capture_output=True, text=True)
            elif operation == "zero-log":
                result = subprocess.run(['sudo', 'btrfs', 'rescue', 'zero-log', device], capture_output=True, text=True)
            elif operation == "fix-device-size":
                result = subprocess.run(['sudo', 'btrfs', 'rescue', 'fix-device-size', device], capture_output=True, text=True)
            elif operation == "create-control-device":
                result = subprocess.run(['sudo', 'btrfs', 'rescue', 'create-control-device'], capture_output=True, text=True)
            elif operation == "clear-ino-cache":
                result = subprocess.run(['sudo', 'btrfs', 'rescue', 'clear-ino-cache', device], capture_output=True, text=True)
            elif operation == "clear-space-cache":
                result = subprocess.run(['sudo', 'btrfs', 'rescue', 'clear-space-cache', device], capture_output=True, text=True)
            elif operation == "clear-uuid-tree":
                result = subprocess.run(['sudo', 'btrfs', 'rescue', 'clear-uuid-tree'], capture_output=True, text=True)
            else:
                self.output_display.setPlainText("Invalid Operation")
                return

            # Çıktıyı göster
            if result.returncode == 0:
                self.output_display.setPlainText(result.stdout)
            else:
                self.output_display.setPlainText(f"Error: {result.stderr}")

        except Exception as e:
            self.output_display.setPlainText(f"Error executing command: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BtrfsRescueGUI()
    window.show()
    sys.exit(app.exec())
