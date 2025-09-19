from PyQt6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QLineEdit, 
    QPushButton, 
    QLabel, 
    QMessageBox
)
import database


class ApiKeyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter API Key")
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.label = QLabel("Please enter your API key:")
        layout.addWidget(self.label)

        self.input = QLineEdit()
        # preload existing key if available
        saved_key = database.load_api_key()
        if saved_key:
            self.input.setText("***************")
        layout.addWidget(self.input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_key)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_key(self):
        api_key = self.input.text().strip()
        if api_key:
            database.save_api_key(api_key)
            QMessageBox.information(self, "Success", "API key saved successfully.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "API key cannot be empty.")
