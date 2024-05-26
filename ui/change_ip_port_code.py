from PySide6.QtWidgets import QDialog, QDialogButtonBox
from PySide6.QtCore import Signal

from change_ip_port_ui import Ui_Dialog
import styleSheet


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

    def set_theme(self,theme: styleSheet.Theme):
        self.set_line_edit_style_sheet(theme)
        self.set_button_box_style_sheet(theme)
        self.set_dialog_style_sheet(theme)
        self.set_label_style_sheet(theme)
