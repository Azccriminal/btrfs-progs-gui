import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QHBoxLayout
from PyQt6.QtCore import Qt

class DiskOperationsGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Btrfs Disk Operations")
        self.setGeometry(200, 200, 600, 500)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Başlık Label
        self.title = QLabel("Btrfs Disk Operations", self)
        self.title.setStyleSheet("font-size: 24px; color: white;")
        main_layout.addWidget(self.title)

        # Disk İşlemleri Butonları
        button_layout = QVBoxLayout()

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.execute_back_command)
        main_layout.addWidget(self.back_button)

        # Show space usage
        self.df_button = QPushButton("Show Space Usage (df)", self)
        self.df_button.clicked.connect(lambda: self.run_disk_operation("df"))
        button_layout.addWidget(self.df_button)

        # Summarize disk usage
        self.du_button = QPushButton("Summarize Disk Usage (du)", self)
        self.du_button.clicked.connect(lambda: self.run_disk_operation("du"))
        button_layout.addWidget(self.du_button)

        # Show filesystem structure
        self.show_button = QPushButton("Show Filesystem Structure (show)", self)
        self.show_button.clicked.connect(lambda: self.run_disk_operation("show"))
        button_layout.addWidget(self.show_button)

        # Force sync filesystem
        self.sync_button = QPushButton("Force Sync Filesystem (sync)", self)
        self.sync_button.clicked.connect(lambda: self.run_disk_operation("sync"))
        button_layout.addWidget(self.sync_button)

        # Defragment filesystem
        self.defrag_button = QPushButton("Defragment Filesystem (defragment)", self)
        self.defrag_button.clicked.connect(lambda: self.run_disk_operation("defragment"))
        button_layout.addWidget(self.defrag_button)

        # Resize filesystem
        self.resize_button = QPushButton("Resize Filesystem (resize)", self)
        self.resize_button.clicked.connect(lambda: self.run_disk_operation("resize"))
        button_layout.addWidget(self.resize_button)

        # Create swapfile
        self.mkswap_button = QPushButton("Create Swap File (mkswapfile)", self)
        self.mkswap_button.clicked.connect(lambda: self.run_disk_operation("mkswapfile"))
        button_layout.addWidget(self.mkswap_button)

        # Set the layout for buttons
        main_layout.addLayout(button_layout)

        # Çıktı Gösterim Alanı
        self.output_display = QTextEdit(self)
        self.output_display.setStyleSheet(self.get_styles())
        self.output_display.setReadOnly(True)
        main_layout.addWidget(self.output_display)

        # Layout Ayarları
        self.setLayout(main_layout)
    def execute_back_command(self):
        try:
            result = subprocess.run(["./main-btrfsqt6"], check=True, text=True, capture_output=True)
            self.output_label.setText(f"Back command executed successfully: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.output_label.setText(f"Error executing back command: {e.stderr}")
 
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

    def run_disk_operation(self, operation):
        """Run the selected disk operation and display the output."""
        try:
            if operation == "df":
                result = subprocess.run(['sudo', 'btrfs', 'filesystem', 'df', '/'], capture_output=True, text=True)
            elif operation == "du":
                result = subprocess.run(['sudo', 'btrfs', 'filesystem', 'du', '/'], capture_output=True, text=True)
            elif operation == "show":
                result = subprocess.run(['sudo', 'btrfs', 'filesystem', 'show', '/'], capture_output=True, text=True)
            elif operation == "sync":
                result = subprocess.run(['sudo', 'btrfs', 'filesystem', 'sync', '/'], capture_output=True, text=True)
            elif operation == "defragment":
                result = subprocess.run(['sudo', 'btrfs', 'filesystem', 'defragment', '/'], capture_output=True, text=True)
            elif operation == "resize":
                # Prompt for a new size or use a default value
                new_size = "10G"  # Example size
                result = subprocess.run(['sudo', 'btrfs', 'filesystem', 'resize', new_size, '/'], capture_output=True, text=True)
            elif operation == "mkswapfile":
                # Prompt for swap file path
                swap_file = "/mnt/swapfile"  # Example path
                result = subprocess.run(['sudo', 'btrfs', 'filesystem', 'mkswapfile', swap_file], capture_output=True, text=True)

            # Display output
            if result.returncode == 0:
                self.output_display.setPlainText(result.stdout)
            else:
                self.output_display.setPlainText(f"Error: {result.stderr}")

        except Exception as e:
            self.output_display.setPlainText(f"Error executing command: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiskOperationsGUI()
    window.show()
    sys.exit(app.exec())
