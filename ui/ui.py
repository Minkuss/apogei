import sys
import time
from datetime import datetime
import socket

from PySide6.QtGui import QColor, QIcon, QPen, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QMessageBox, QVBoxLayout\
    , QFileDialog
from pandas import DataFrame, to_datetime, read_excel, ExcelWriter
import pyqtgraph as pg
import pyqtgraph.exporters
from openpyxl import Workbook
from openpyxl.drawing.image import Image

import styleSheet
from apogei_ui import Ui_MainWindow
from change_ip_port_code import ChangeConnectionData
from connection.client.client import get_data_from_server
import json


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
        self.ui.pushButton_4.clicked.connect(self.show_analysis)
        self.ip = '127.0.0.1'
        self.port = 30033
        self.data: DataFrame = DataFrame()
        self.ui.dates.clear()
        self.plot_widget = pg.PlotWidget()
        self.plot_layout = QVBoxLayout(self.ui.graphic)
        self.plot_layout.addWidget(self.plot_widget)
        self.set_graphic_widget_style_sheet(styleSheet.Theme.Dark)
        self.connection_window = None
        self.json_data = None
        self.current_user = None
        self.current_password = None

    def show_change_connection_data_window(self):
        """Open connection data window."""
        self.connection_window = ChangeConnectionData()
        self.connection_window.ReturnChange.connect(self.set_new_connection_data)
        self.connection_window.set_theme(self.theme)
        self.connection_window.show()

    def set_new_connection_data(self, ip, port):
        """Set new connection data."""
        self.ip, self.port = ip, port
        del self.connection_window
        self.connection_window = None
        file_path = '..\\users.json'
        for user in self.json_data:
            if user["username"] == self.current_user and user['password'] == self.current_password:
                user['ip'] = ip
                user['port'] = port
                break
        with open(file_path, 'w') as file:
            json.dump(self.json_data, file, indent=4)

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
        self.set_graphic_widget_style_sheet(theme)

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

    def set_graphic_widget_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set graphic widget style sheet."""
        self.ui.graphic.setStyleSheet(styleSheet.get_graphic_style_sheet(theme))
        if theme == styleSheet.Theme.Dark:
            color = QColor(103, 187, 198)
            self.plot_widget.setBackground(color)
            self.plot_widget.getPlotItem().getAxis('left').setPen('k')  # Белый цвет оси
            self.plot_widget.getPlotItem().getAxis('bottom').setPen('k')  # Белый цвет оси
            left_axis = self.plot_widget.getPlotItem().getAxis('left')  # или 'bottom' для оси x
            left_axis.setTextPen(QColor(0, 0, 0))
            dawn_axis = self.plot_widget.getPlotItem().getAxis('bottom')  # или 'bottom' для оси x
            dawn_axis.setTextPen(QColor(0, 0, 0))
        else:
            color = QColor(255, 255, 255)
            self.plot_widget.setBackground(color)
            self.plot_widget.getPlotItem().getAxis('left').setPen('k')  # Черный цвет оси
            self.plot_widget.getPlotItem().getAxis('bottom').setPen('k')  # Черный цвет оси
            left_axis = self.plot_widget.getPlotItem().getAxis('left')  # или 'bottom' для оси x
            left_axis.setTextPen(QColor(0, 0, 0))
            dawn_axis = self.plot_widget.getPlotItem().getAxis('bottom')  # или 'bottom' для оси x
            dawn_axis.setTextPen(QColor(0, 0, 0))

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
            self.plot_widget.clear()
            # Извлечение времени из объектов datetime
            times = [dt.timestamp() for dt in times_datetime]  # Преобразование времени в timestamp
            values = filtered_data[cases[selected_case]].tolist()  # Извлечение численных значений
            axis = pg.DateAxisItem(orientation='bottom')
            axis.setTickSpacing(major=3600 * 24, minor=3600)  # Настройка основных и дополнительных меток
            axis.setStyle(tickTextOffset=10, tickFont=QFont("Arial", 10), autoExpandTextSpace=True)
            self.plot_widget.setAxisItems({'bottom': axis})
            self.plot_widget.getPlotItem().getAxis('left').setPen('k')  # Черный цвет оси
            self.plot_widget.getPlotItem().getAxis('bottom').setPen('k')  # Черный цвет оси
            left_axis = self.plot_widget.getPlotItem().getAxis('left')  # или 'bottom' для оси x
            left_axis.setTextPen(QColor(0, 0, 0))
            dawn_axis = self.plot_widget.getPlotItem().getAxis('bottom')  # или 'bottom' для оси x
            dawn_axis.setTextPen(QColor(0, 0, 0))
            match self.ui.comboBox.currentText():
                case 'Температура':
                    self.plot_widget.getPlotItem().setLabel('left', 'Температура', units='°C')
                case 'Влажность':
                    self.plot_widget.getPlotItem().setLabel('left', 'Влажность', units='%')
                case 'Давление':
                    self.plot_widget.getPlotItem().setLabel('left', 'Давление', units='hPa')
                case 'Полный спектр':
                    self.plot_widget.getPlotItem().setLabel('left', 'Полный спектр', units='counts')
                case 'Инфракрасный спектр':
                    self.plot_widget.getPlotItem().setLabel('left', 'Инфракрасный спектр', units='counts')
                case 'Видимый спектр':
                    self.plot_widget.getPlotItem().setLabel('left', 'Видимый спектр', units='counts')
            self.plot_widget.plot(times, values, pen='k')
            self.plot_widget.getPlotItem().showGrid(x=True, y=True, alpha=0.2)
            self.plot_widget.getPlotItem().vb.autoRange()
        else:
            self.ui.dates.hide()
            self.plot_widget.clear()

            times_datetime = self.data['timestamp'].dt.to_pydatetime()
            times = [dt.timestamp() for dt in times_datetime]
            values = self.data[cases[selected_case]].tolist()

            axis = pg.DateAxisItem(orientation='bottom')
            axis.setTickSpacing(major=3600 * 24, minor=3600)
            axis.setStyle(tickTextOffset=10, tickFont=QFont("Arial", 10), autoExpandTextSpace=True)
            self.plot_widget.setAxisItems({'bottom': axis})

            # Настройка осей
            left_axis = self.plot_widget.getPlotItem().getAxis('left')
            bottom_axis = self.plot_widget.getPlotItem().getAxis('bottom')

            left_axis.setPen('k')
            bottom_axis.setPen('k')

            left_axis.setTextPen(QColor(0, 0, 0))
            bottom_axis.setTextPen(QColor(0, 0, 0))

            # Установка метки для оси Y
            match self.ui.comboBox.currentText():
                case 'Температура':
                    self.plot_widget.getPlotItem().setLabel('left', 'Температура', units='°C')
                case 'Влажность':
                    self.plot_widget.getPlotItem().setLabel('left', 'Влажность', units='%')
                case 'Давление':
                    self.plot_widget.getPlotItem().setLabel('left', 'Давление', units='hPa')
                case 'Полный спектр':
                    self.plot_widget.getPlotItem().setLabel('left', 'Полный спектр', units='counts')
                case 'Инфракрасный спектр':
                    self.plot_widget.getPlotItem().setLabel('left', 'Инфракрасный спектр', units='counts')
                case 'Видимый спектр':
                    self.plot_widget.getPlotItem().setLabel('left', 'Видимый спектр', units='counts')

            self.plot_widget.plot(times, values, pen='k')

            # Отображение сетки
            self.plot_widget.getPlotItem().showGrid(x=True, y=True, alpha=0.2)

            # Обновление диапазона видимости
            self.plot_widget.getPlotItem().vb.autoRange()

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

    def show_analysis(self):
        if self.data.empty:
            QMessageBox.information(self, 'Таблица пуста', 'Таблица пуста,'
                                                 ' нажмите кнопку "Обновить" чтобы получить данные')
        else:
            cases = {
                'Температура': 'temperature',
                'Влажность': 'humidity',
                'Давление': 'pressure',
                'Полный спектр': 'full_spectrum',
                'Инфракрасный спектр': 'infrared_spectrum',
                'Видимый спектр': 'visible_spectrum',
            }
            analyzed_data = self.data[cases[self.ui.comboBox.currentText()]].describe()

            analyzed_data_translated = analyzed_data.rename(index={
                'count': 'Количество',
                'mean': 'Среднее',
                'std': 'Стандартное отклонение',
                'min': 'Минимум',
                '25%': '25-й перцентиль',
                '50%': 'Медиана',
                '75%': '75-й перцентиль',
                'max': 'Максимум'
            })

            # Преобразуем описание в текстовый формат
            analyzed_data_text = analyzed_data_translated.to_string()
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(f"Статистика для колонки '{self.ui.comboBox.currentText()}':\n{analyzed_data_text}\n"
                            f"Хотите сохранить данные о таблице? ")
            msg_box.setWindowTitle("Описательная статистика")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            # Обрабатываем ответ пользователя
            response = msg_box.exec_()
            if response == QMessageBox.Yes:
                filename, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Excel Files (*.xlsx)")
                if filename:
                    self.export_analysis(analyzed_data_translated, filename, cases[self.ui.comboBox.currentText()])
                    print("Пользователь выбрал 'Да' и выбрал файл:", filename)
                else:
                    print("Пользователь выбрал 'Да', но не выбрал файл")
            else:
                print("Пользователь выбрал 'Нет'")

    def export_analysis(self, data, filename, case):
        self.plot_widget.setBackground("w")
        exporter = pg.exporters.ImageExporter(self.plot_widget.plotItem)
        exporter.parameters()['width'] = 800  # Set image width
        exporter.export('plot.png')
        describe_df = data
        if self.theme == styleSheet.Theme.Dark:
            color = QColor(103, 187, 198)
            self.plot_widget.setBackground(color)

        # Save describe statistics to Excel
        with ExcelWriter(filename, engine='openpyxl') as writer:
            self.data[["timestamp", case]].to_excel(writer, sheet_name="Table_data", index=False)
            describe_df.to_excel(writer, sheet_name='Describe')

            # Load the workbook and get the active worksheet
            wb = writer.book
            ws = wb.create_sheet('Graph')

            # Add the image to the worksheet
            img = Image('plot.png')
            ws.add_image(img, 'A1')


    def set_btn_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set button style sheet."""
        self.ui.pushButton.setStyleSheet(styleSheet.get_btn_style_sheet(theme))
        self.ui.pushButton_2.setStyleSheet(styleSheet.get_btn_style_sheet(theme))
        self.ui.pushButton_3.setStyleSheet(styleSheet.get_btn_style_sheet(theme))
        self.ui.pushButton_4.setStyleSheet(styleSheet.get_btn_style_sheet(theme))

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
        self.ui.graphic_type.setStyleSheet(styleSheet.get_combo_box_style_sheet(theme))
        self.ui.dates.setStyleSheet(styleSheet.get_combo_box_style_sheet(theme))

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
