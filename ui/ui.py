import sys
from PySide6.QtCore import QObject, QSize, Qt, Signal, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QAbstractItemView, \
    QLabel, QDialog, QPushButton, QFileDialog, QDialogButtonBox, QMessageBox
from Apogei_ui import Ui_MainWindow


class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.menu.actions()[0].triggered.connect(self.print_message)

    def print_message(self):
        QMessageBox.information(None, "Сообщение", "Егор - лох")
    def fill_table(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = myWindow()
    main_window.show()
    sys.exit(app.exec())

