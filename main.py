from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
)
import database
from apikeydialog import ApiKeyDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        city_name = QLineEdit()
        current_temperature = QLabel()
        low_temperature = QLabel()
        high_temperature = QLabel()
        weather_condition = QLabel()
        query_button = QPushButton("Submit")

        layout.addWidget(city_name)
        layout.addWidget(query_button)
        layout.addWidget(current_temperature)
        layout.addWidget(low_temperature)
        layout.addWidget(high_temperature)
        layout.addWidget(weather_condition)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File") # type: ignore

        # API Key action
        api_key_action = QAction("API Key", self)
        api_key_action.triggered.connect(self.open_api_key_dialog)
        file_menu.addAction(api_key_action) # type: ignore

        # Close action
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action) # type: ignore

    def open_api_key_dialog(self):
        dialog = ApiKeyDialog()
        dialog.exec()


if __name__ == "__main__":
    database.init_db()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
