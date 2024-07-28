
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QListWidget
from main_window_ui import Ui_MainWindow  # импорт  сгенерированного файла
from parsing_avito import ParsingAvito  # Импортируйте  класс парсера
import sys




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Добавляем элементы в список городов
        self.ui.cityList.addItem(QListWidgetItem("Невинномысск"))
        self.ui.cityList.addItem(QListWidgetItem("Карачаево-Черкесская республика"))

        # Подключите сигналы к слотам
        self.ui.cityList.itemClicked.connect(self.on_city_selected)
        self.ui.parseButton.clicked.connect(self.start_parsing)

    def on_city_selected(self, item):
        selected_city = item.text()
        if selected_city == "Невинномысск":
            self.ui.cityList.clear()
            self.ui.cityList.addItem(QListWidgetItem("ПРП-ЗИП"))
            self.ui.cityList.addItem(QListWidgetItem("Центр"))
            self.ui.cityList.addItem(QListWidgetItem("Фабрика"))
            self.ui.cityList.addItem(QListWidgetItem("Головное"))

    def start_parsing(self):
        selected_item = self.ui.cityList.currentItem()
        if selected_item is None:
            return

        selected_rayon = selected_item.text()
        url = ""

        match selected_rayon:
            case "ПРП-ЗИП":
                url = "https://www.avito.ru/nevinnomyssk/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?context=&district=314-316-319-321"
            case "Центр":
                url = "https://www.avito.ru/nevinnomyssk/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?context=&district=323-325"
            case "Фабрика":
                url ='https://www.avito.ru/nevinnomyssk/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?context=&district=322-324'
            case "Головное":
                url = 'https://www.avito.ru/nevinnomyssk/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?context=&district=312-320'

        if url:
            print(f"Начинается парсинг для района: {selected_rayon}")
            parser = ParsingAvito(url=url, count=1, debug_mode=1, rayon=selected_rayon)
            parser.parse()
            self.output_results(parser.data)


        # if selected_item:
        #     if selected_item.text() == "ПРП-ЗИП":
        #         print("Я работаю")
        #         url = "https://www.avito.ru/nevinnomyssk/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?context=&district=314-316-319-321"
        #         parser = ParsingAvito(url=url, count=1, debug_mode=1)
        #         parser.parse()
        #         self.output_results(parser.data)

    def output_results(self, data):
        for item in data:
            self.ui.outputField.append(f"Название: {item['name']}")
            self.ui.outputField.append(f"Описание: {item['description']}")
            self.ui.outputField.append(f"Цена: {item['price']}")
            self.ui.outputField.append(f"Ссылка: {item['url']}")
            self.ui.outputField.append(f"Адрес: {item['address']}")
            self.ui.outputField.append(f"Дата публикации: {item['date_public']}")
            self.ui.outputField.append("-" * 50)
if __name__ == "__main__":
    app = QApplication(sys.argv) # базовый класс для всех GUI-приложений на PySide6
    # Он управляет приложением, а также обрабатывает события
    """"sys.argv содержит список аргументов командной строки, 
    переданных при запуске скрипта. Это полезно для настройки приложения с использованием 
    командной строки (например, для передачи параметров конфигурации)."""
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

