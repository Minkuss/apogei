from PySide6.QtWidgets import QDialog, QDialogButtonBox, QApplication, QLabel
from PySide6.QtCore import Signal
import sys
from authorisation import Ui_Dialog
import styleSheet
import os
import json
from ui import MyWindow


class AuthorisationRegistration(QDialog):
    ReturnChange = Signal(str, int)

    def __init__(self):
        super(AuthorisationRegistration, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Авторизация')
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        self.ui.lineEdit.textChanged.connect(self.check_line_edits)
        self.ui.lineEdit_2.textChanged.connect(self.check_line_edits)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setText('Отмена')
        self.ui.pushButton.clicked.connect(self.change_forms)
        self.setMaximumWidth(290)
        self.setMaximumHeight(243)
        self.setMinimumWidth(290)
        self.setMinimumHeight(243)
        self.users_data = None
        self.file_path = '..\\users.json'
        self.main_window = MyWindow()

    def accept(self) -> None:
        """Read data from user and return data to base window."""
        name = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if self.ui.pushButton.text() == "Авторизация":
            self.registration(name, password)
        else:
            for user in self.users_data:
                if user["username"] == name and user["password"] == password:
                    self.main_window.show()
                    self.main_window.load_from_excel_data()
                    self.main_window.current_user = name
                    self.main_window.current_password = password
                    self.main_window.ip = user['ip']
                    self.main_window.port = user['port']
                    self.main_window.json_data = self.users_data
                    self.close()
                    break


    def registration(self, name, password):
        # Создать новую запись
        new_entry = {
            "username": name,
            "password": password,
            "ip": "127.0.0.1",
            "port": 30033
        }

        # Добавить новую запись к существующим данным
        self.users_data.append(new_entry)

        # Записать обновленные данные обратно в файл
        with open(self.file_path, 'w') as file:
            json.dump(self.users_data, file, indent=4)
        self.change_forms()

    def change_forms(self):
        if self.ui.pushButton.text() == "Регистрация":
            self.setWindowTitle('Регистрация')
            self.ui.pushButton.setText("Авторизация")
        else:
            self.setWindowTitle('Авторизация')
            self.ui.pushButton.setText("Регистрация")
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit.clear()

    def get_users_data(self):
        try:
            with open(self.file_path, 'r') as file:
                self.users_data = json.load(file)
        except FileNotFoundError:
            self.users_data = []
        # print(self.users_data)


    def check_line_edits(self):
        """Check line edits if they clear or not."""
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        if (self.ui.lineEdit.text() != '') and (self.ui.lineEdit_2.text() != ''):
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)

    def set_line_edit_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set edit line style sheet."""
        self.ui.lineEdit.setStyleSheet(styleSheet.get_line_edit_style_sheet(theme))
        self.ui.lineEdit_2.setStyleSheet(styleSheet.get_line_edit_style_sheet(theme))


    def set_dialog_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set dialog  style sheet."""
        self.setStyleSheet(styleSheet.get_dialog_style_sheet(theme))

    def set_button_box_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set buttonBox style sheet."""
        self.ui.buttonBox.setStyleSheet(styleSheet.get_btnbox_style_sheet(theme))

    def set_label_style_sheet(self, theme: styleSheet.Theme) -> None:
        """Set label style sheet."""
        self.ui.label.setStyleSheet(styleSheet.get_label_style_sheet(theme))
        self.ui.label_2.setStyleSheet(styleSheet.get_label_style_sheet(theme))

    def setTheme(self, theme: styleSheet.Theme):
        self.set_line_edit_style_sheet(theme)
        self.set_button_box_style_sheet(theme)
        self.set_dialog_style_sheet(theme)
        self.set_label_style_sheet(theme)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = AuthorisationRegistration()
    main_window.get_users_data()
    main_window.show()
    sys.exit(app.exec())
