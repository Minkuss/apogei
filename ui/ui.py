import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PySide6.QtCore import Qt
from Apogei_ui import Ui_MainWindow
from datetime import datetime


class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.menu.actions()[0].triggered.connect(self.print_message)

    def print_message(self):
        QMessageBox.information(None, "Сообщение", "Егор - лох")

    def fill_table(self):
        scanner1 = [
            [datetime(2024, 3, 15, 14, 20), 25],
            [datetime(2024, 3, 16, 14, 30), 29],
            [datetime(2024, 3, 12, 14, 45), 29],
            [datetime(2024, 3, 16, 12, 35), 41]
        ]

        # Сортируем данные в порядке возрастания по времени и дате
        scanner1_sorted = sorted(scanner1, key=lambda x: (x[0].time(), x[0]))

        # Создаем словари для хранения данных по времени и дате
        data_by_time = {}
        data_by_date = {}

        for date_time, value in scanner1_sorted:
            date_str = date_time.strftime("%d/%m/%Y")
            time_str = date_time.strftime("%H:%M")

            # Добавляем данные в словарь по времени
            if time_str not in data_by_time:
                data_by_time[time_str] = {}
            data_by_time[time_str][date_str] = value

            # Добавляем данные в словарь по дате
            if date_str not in data_by_date:
                data_by_date[date_str] = {}
            data_by_date[date_str][time_str] = value

        # Получаем список уникальных дат и времен
        unique_dates = sorted(data_by_date.keys())
        unique_times = sorted(data_by_time.keys())

        # Устанавливаем размеры таблицы
        self.ui.tableWidget.setColumnCount(len(unique_times))
        self.ui.tableWidget.setRowCount(len(unique_dates))

        # Устанавливаем заголовки
        self.ui.tableWidget.setHorizontalHeaderLabels(unique_times)
        self.ui.tableWidget.setVerticalHeaderLabels(unique_dates)

        # Заполняем таблицу данными
        for row, date in enumerate(unique_dates):
            for column, time in enumerate(unique_times):
                if date in data_by_time[time]:
                    value = str(data_by_time[time][date])
                else:
                    value = "0"
                item = QTableWidgetItem(value)
                self.ui.tableWidget.setItem(row, column, item)


    def remove_duplicate(self, mylist):
        return sorted(set(mylist), key=lambda x: mylist.index(x))




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = myWindow()
    main_window.fill_table()
    main_window.show()
    sys.exit(app.exec())

