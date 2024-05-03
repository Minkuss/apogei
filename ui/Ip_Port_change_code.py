from PySide6.QtWidgets import QDialog, QDialogButtonBox
from PySide6.QtCore import Signal
from Authorisation_ui import Ui_Dialog


class ChangeConnectionData(QDialog):
    ReturnChange = Signal(str, int)

    def __init__(self):
        super(ChangeConnectionData, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Смена IP и порта')
        self.ui.label.setText('IP')
        self.ui.label_2.setText('Порт')
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        self.ui.lineEdit.textChanged.connect(self.check_line_edits)
        self.ui.lineEdit_2.textChanged.connect(self.check_line_edits)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setText('Отмена')
        self.setMaximumWidth(290)
        self.setMaximumHeight(243)
        self.setMinimumWidth(290)
        self.setMinimumHeight(243)

    def accept(self) -> None:
        """Read data from user and return data to base window."""
        ip = self.ui.lineEdit.text()
        port = self.ui.lineEdit_2.text()
        self.ReturnChange.emit(ip, int(port))
        super(ChangeConnectionData, self).accept()

    def check_line_edits(self):
        """Check line edits if they clear or not."""
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        if (self.ui.lineEdit.text() != '') and (self.ui.lineEdit_2.text() != ''):
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)
