import sys
import time
from datetime import datetime
import socket

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QMessageBox, QVBoxLayout, QWidget
from pandas import DataFrame, to_datetime, read_excel
import pyqtgraph as pg

import styleSheet
from Apogei_ui import Ui_MainWindow
from Ip_Port_change_code import ChangeConnectionData
from connection.client.client import get_data_from_server


class MyWindow(QMainWindow):
    """Class for ui."""

    def __init__(self) -> None:
        """Initialize class and edit ui parameters."""
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Апогей')
        self.theme = styleSheet.Theme.Dark
        self.ui.menu.addAction('Смена IP и порта')
        self.ui.menu.actions()[0].triggered.connect(self.change_style)
        self.ui.menu.actions()[1].triggered.connect(self.show_change_connection_data_window)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.pushButton.clicked.connect(self.search)
        self.get_action_style_sheet(styleSheet.Theme.Dark)
        self.set_btn_style_sheet(styleSheet.Theme.Dark)
        self.set_table_widget_style_sheet(styleSheet.Theme.Dark)
        self.set_combo_box_style_sheet(styleSheet.Theme.Dark)
        self.set_date_picker_style_sheet(styleSheet.Theme.Dark)
        self.set_main_window_style_sheet(styleSheet.Theme.Dark)
        self.ui.comboBox.addItem('Температура')
        self.ui.comboBox.addItem('Влажность')
        self.ui.comboBox.addItem('Давление')
        self.ui.comboBox.addItem('Полный спектр')
        self.ui.comboBox.addItem('Инфракрасный спектр')
        self.ui.comboBox.addItem('Видимый спектр')
        self.ui.comboBox.adjustSize()
        self.ui.comboBox.currentTextChanged.connect(self.fill_table)
        self.ui.pushButton_3.clicked.connect(self.fill_table)
        self.ui.pushButton_2.clicked.connect(self.update_data)
        self.ui.dateEdit_2.setDate(datetime.now())
        self.ui.dateEdit.setDate(self.ui.dateEdit_2.date().addDays(-7))
        self.ui.dates.currentIndexChanged.connect(self.update_graph)
        self.ui.graphic_type.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBox.currentIndexChanged.connect(self.update_graph)
        self.setMaximumWidth(466)
        self.setMaximumHeight(666)
        self.setMinimumWidth(466)
        self.setMinimumHeight(666)
        self.ip = '127.0.0.1'
        self.port = 30033
        self.data: DataFrame = DataFrame()
        self.ui.dates.clear()
        self.plot_widget = pg.PlotWidget()
        self.plot_layout = QVBoxLayout(self.ui.graphic)
        self.plot_layout.addWidget(self.plot_widget)
        self.connection_window = None

    def show_change_connection_data_window(self):
        """Open connection data window."""
        self.connection_window = ChangeConnectionData()
        self.connection_window.ReturnChange.connect(self.set_new_connection_data)
        self.connection_window.setTheme(self.theme)
        self.connection_window.show()

    def set_new_connection_data(self, ip, port):
        """Set new connection data."""
        self.ip, self.port = ip, port
        del self.connection_window
        self.connection_window = None

    def export_excel(self):
        """Export excel."""
        self.data.to_excel('..\\output.xlsx', index=False)

    def load_data(self) -> None:
        """Load data from database."""
        data: dict = get_data_from_server(self.ip, self.port)
        self.data = DataFrame(data)
        self.data['timestamp'] = to_datetime(self.data['timestamp'])

    def load_from_excel_data(self):
        try:
            self.data = read_excel('..\\output.xlsx')
            self.data['timestamp'] = to_datetime(self.data['timestamp'])
            self.fill_table()
        except Exception as ex:
            print(ex)
            print('Ошибка получения данных с excel.')

    def change_style(self) -> None:
        """Set new stylesheet."""
        if self.theme == styleSheet.Theme.Dark:
            self.theme = styleSheet.Theme.Light
        else:
            self.theme = styleSheet.Theme.Dark
        self.update_styles(self.theme)

    def update_styles(self, theme: styleSheet.Theme) -> None:
        """Update widgets style."""
        self.set_btn_style_sheet(theme)
        self.set_table_widget_style_sheet(theme)
        self.set_combo_box_style_sheet(theme)
        self.set_date_picker_style_sheet(theme)
        self.set_main_window_style_sheet(theme)
        self.get_action_style_sheet(theme)

    def fill_table(self) -> None:
        """Fill table with data."""
        cases = {
            'Температура': 'temperature',
            'Влажность': 'humidity',
            'Давление': 'pressure',
            'Полный спектр': 'full_spectrum',
            'Инфракрасный спектр': 'infrared_spectrum',
            'Видимый спектр': 'visible_spectrum',
        }
        scanner = list(zip(self.data['timestamp'], self.data[cases[self.ui.comboBox.currentText()]]))
        self.ui.tableWidget.clear()

        # Сортируем данные в порядке возрастания по времени и дате
        scanner_sorted = sorted(scanner, key=lambda x: (x[0].time(), x[0]))

        # Создаем словари для хранения данных по времени и дате
        data_by_time = {}
        data_by_date = {}

        for date_time, value in scanner_sorted:
            date_str = date_time.strftime('%d/%m/%Y')
            time_str = date_time.strftime('%H:%M:%S')

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
            for column, data_time in enumerate(unique_times):
                if date in data_by_time[data_time]:
                    value = str(data_by_time[data_time][date])
                else:
                    value = '0'
                item = QTableWidgetItem(value)
                self.ui.tableWidget.setItem(row, column, item)
        self.set_table_widget_column_width()

        # Fill combobox with unique dates
        self.fill_combobox_with_dates()

    def fill_combobox_with_dates(self):
        """Fill combobox with unique dates from the data."""
        unique_dates = sorted({dt.strftime('%d/%m/%Y') for dt in self.data['timestamp']})
        self.ui.dates.clear()
        self.ui.dates.addItems(unique_dates)
        self.update_graph()

    def update_graph(self):

        cases = {
            'Температура': 'temperature',
            'Влажность': 'humidity',
            'Давление': 'pressure',
            'Полный спектр': 'full_spectrum',
            'Инфракрасный спектр': 'infrared_spectrum',
            'Видимый спектр': 'visible_spectrum',
        }

        selected_case = self.ui.comboBox.currentText()
        if selected_case not in cases:
            return

        if self.ui.graphic_type.currentText() == "График по дню":
            self.ui.dates.show()
            selected_date = self.ui.dates.currentText()
            if not selected_date:
                return



            # Фильтруем данные по выбранной дате
            filtered_data = self.data[self.data['timestamp'].dt.strftime('%d/%m/%Y') == selected_date]

            if filtered_data.empty:
                return

            # Получаем данные для графика
            times_datetime = filtered_data['timestamp'].dt.to_pydatetime()

            # Извлечение времени из объектов datetime
            times = [dt.timestamp() for dt in times_datetime]  # Преобразование времени в datetime
            values = filtered_data[cases[selected_case]].tolist()  # Извлечение численных значений
            axis = pg.DateAxisItem()
            self.plot_widget.setBackground('w')
            self.plot_widget.setAxisItems({'bottom': axis})
            self.plot_widget.clear()
            self.plot_widget.plot(times, values, pen='b')
        else:
            self.ui.dates.hide()
            times_datetime = self.data['timestamp'].dt.to_pydatetime()
            # Извлечение времени из объектов datetime
            times = [dt.timestamp() for dt in times_datetime]  # Преобразование времени в datetime
            values = self.data[cases[selected_case]].tolist()  # Извлечение численных значений
            axis = pg.DateAxisItem()
            self.plot_widget.setBackground('w')
            self.plot_widget.setAxisItems({'bottom': axis})
            self.plot_widget.clear()
            self.plot_widget.plot(times, values, pen='b')


    @staticmethod
    def remove_duplicate(mylist: list) -> list:
        """Remove duplicates from sensors list."""
        return sorted(set(mylist), key=lambda x: mylist.index(x))

    def search(self) -> None:
        """Search data by datetimes."""
        start_date = self.ui.dateEdit.date()
        start_date_datetime = datetime(start_date.year(), start_date.month(), start_date.day())
        end_date = self.ui.dateEdit_2.date()
        end_date_datetime = datetime(end_date.year(), end_date.month(), end_date.day())
        date_format = '%d/%m/%Y'

        row_index = 0
        while row_index < self.ui.tableWidget.rowCount():
            date = self.ui.tableWidget.verticalHeaderItem(row_index).text()
            date_datetime = datetime.strptime(date, date_format)
            if (date_datetime < start_date_datetime) or (date_datetime > end_date_datetime):
                self.ui.tableWidget.removeRow(row_index)
            else:
                row_index += 1

    def update_data(self) -> None:
        """Update data."""
        while True:
            try:
                self.load_data()
                break
            except ValueError as ex:
                print(ex)
                time.sleep(1)
            except socket.gaierror as ex:
                print(ex)
                QMessageBox.critical(self, 'Ошибка', 'Ошибка подключения к серверу,'
                                                     'проверьте правильно ли у вас выставлены Ip и порт')
                break

        self.fill_table()
        self.export_excel()



    def set_btn_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set button style sheet."""
        self.ui.pushButton.setStyleSheet(styleSheet.get_btn_style_sheet(theme))
        self.ui.pushButton_2.setStyleSheet(styleSheet.get_btn_style_sheet(theme))
        self.ui.pushButton_3.setStyleSheet(styleSheet.get_btn_style_sheet(theme))

    def set_table_widget_column_width(self) -> None:
        """Set table width."""
        num_columns = self.ui.tableWidget.columnCount()
        column_width = 113
        for i in range(num_columns):
            self.ui.tableWidget.setColumnWidth(i, column_width)

    def set_table_widget_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set table style sheet."""
        self.ui.tableWidget.setStyleSheet(styleSheet.get_table_widget_style_sheet(theme))

    def set_combo_box_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set combo box style sheet."""
        self.ui.comboBox.setStyleSheet(styleSheet.get_combo_box_style_sheet(theme))

    def set_date_picker_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set date picker style sheet."""
        self.ui.dateEdit.setStyleSheet(styleSheet.get_date_picker_style_sheet(theme))
        self.ui.dateEdit_2.setStyleSheet(styleSheet.get_date_picker_style_sheet(theme))

    def set_main_window_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set main window style sheet."""
        self.setStyleSheet(styleSheet.get_main_window_style_sheet(theme))

    def get_action_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Get action style sheet."""
        self.ui.menubar.setStyleSheet(styleSheet.get_action_style_sheet(theme))
        self.ui.menu.setStyleSheet(styleSheet.get_action_style_sheet(theme))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyWindow()
    main_window.load_from_excel_data()
    main_window.show()
    sys.exit(app.exec())
