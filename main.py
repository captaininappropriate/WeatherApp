from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap, QImage
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QMessageBox
)
import database
from apikeydialog import ApiKeyDialog
import weather
import requests


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        # create widgets
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name...")
        self.query_weather_button = QPushButton("Query Weather")
        self.query_weather_button.clicked.connect(self.query_weather)
        self.weather_condition = QLabel() # image will be placed here
        self.weather_condition.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_label = QLabel("Weather info will appear here.")
        self.weather_label.setWordWrap(True)

        # add widgets to layout
        layout.addWidget(self.city_input)
        layout.addWidget(self.query_weather_button)
        layout.addWidget(self.weather_condition)
        layout.addWidget(self.weather_label)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # create a menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File") # type: ignore

        # API Key action
        api_key_action = QAction("API Key", self)
        api_key_action.triggered.connect(self.open_api_key_dialog)
        file_menu.addAction(api_key_action) # type: ignore

        # close action
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action) # type: ignore

        # Status Bar to display status of API key
        self.statusBar().showMessage(self.get_api_key_status()) # type: ignore

    def get_api_key_status(self) -> str:
        """Check if API key exists and return appropriate status message."""
        api_key = database.load_api_key()
        if api_key:
            return "API key loaded"
        return "API key not set"

    def open_api_key_dialog(self):
        dialog = ApiKeyDialog()
        dialog.exec()

    def query_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return

        try:
            info = weather.get_weather(city)
            # format details on label
            if info:
                msg = (
                    f"Weather in {info['city']}:\n"
                    f"Temperature: {info['temperature']}°C\n"
                    f"Condition: {info['description']}\n"
                    f"Humidity: {info['humidity']}%\n"
                    f"Wind Speed: {info['wind_speed']} m/s"
                )
                self.weather_label.setText(msg)

                # format image url and pass to function
                image_data = info['icon']
                image_url = f"https://openweathermap.org/img/wn/{image_data}@2x.png"
                weather_condition_image = self.get_qpixmap_from_url(image_url)
                self.weather_condition.setPixmap(weather_condition_image)
            else:
                self.weather_label.setText("Could not retrieve weather data.")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def get_qpixmap_from_url(self, url: str) -> QPixmap:
        # Download image data
        response = requests.get(url)
        response.raise_for_status()  # raise an error if download fails
        data = response.content

        # Convert to QImage
        image = QImage.fromData(data)
        if image.isNull():
            raise ValueError("Failed to load image from URL")
        
        # Convert QImage to QPixmap
        return QPixmap.fromImage(image)


if __name__ == "__main__":
    database.init_db()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
