import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit

class BtrfsPropertyGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Btrfs Property Operations")
        self.setGeometry(200, 200, 600, 500)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Başlık
        self.title = QLabel("Btrfs Property Operations", self)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 20px;")
        main_layout.addWidget(self.title)

        # Property İşlemleri Butonları
        self.get_button = QPushButton("Get Property", self)
        self.get_button.clicked.connect(lambda: self.run_property_operation("get"))
        main_layout.addWidget(self.get_button)
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.execute_back_command)
        main_layout.addWidget(self.back_button)

        self.set_button = QPushButton("Set Property", self)
        self.set_button.clicked.connect(lambda: self.run_property_operation("set"))
        main_layout.addWidget(self.set_button)

        self.list_button = QPushButton("List Properties", self)
        self.list_button.clicked.connect(lambda: self.run_property_operation("list"))
        main_layout.addWidget(self.list_button)

        # Object Input
        self.object_input_label = QLabel("Enter Object (e.g., /mnt):", self)
        main_layout.addWidget(self.object_input_label)

        self.object_input = QLineEdit(self)
        main_layout.addWidget(self.object_input)

        # Property Name Input
        self.property_name_input_label = QLabel("Enter Property Name:", self)
        main_layout.addWidget(self.property_name_input_label)

        self.property_name_input = QLineEdit(self)
        main_layout.addWidget(self.property_name_input)

        # Property Value Input
        self.property_value_input_label = QLabel("Enter Property Value (for Set):", self)
        main_layout.addWidget(self.property_value_input_label)

        self.property_value_input = QLineEdit(self)
        main_layout.addWidget(self.property_value_input)

        # Çıktı Alanı
        self.output_display = QTextEdit(self)
        self.output_display.setReadOnly(True)
        main_layout.addWidget(self.output_display)

        self.setLayout(main_layout)

        # CSS stillerini uygula
        self.apply_styles()

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

            QLineEdit {
                background-color: #3A3F47;
                color: white;
                font-size: 16px;
                border-radius: 8px;
                padding: 8px;
                border: 1px solid #555;
                margin-bottom: 10px;
            }

            QLineEdit:focus {
                border-color: #4A90E2;
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
    def execute_back_command(self):
        try:
            result = subprocess.run(["./main-btrfsqt6"], check=True, text=True, capture_output=True)
            self.output_label.setText(f"Back command executed successfully: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.output_label.setText(f"Error executing back command: {e.stderr}")

    def run_property_operation(self, operation):
        """Btrfs property komutlarını çalıştır ve sonucu göster."""
        object_path = self.object_input.text().strip()
        property_name = self.property_name_input.text().strip()
        property_value = self.property_value_input.text().strip()

        try:
            if operation == "get":
                result = subprocess.run(['sudo', 'btrfs', 'property', 'get', object_path, property_name], capture_output=True, text=True)
            elif operation == "set" and property_value:
                result = subprocess.run(['sudo', 'btrfs', 'property', 'set', object_path, property_name, property_value], capture_output=True, text=True)
            elif operation == "list":
                result = subprocess.run(['sudo', 'btrfs', 'property', 'list', object_path], capture_output=True, text=True)
            else:
                self.output_display.setPlainText("Please provide the necessary input.")
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
    window = BtrfsPropertyGUI()
    window.show()
    sys.exit(app.exec())
