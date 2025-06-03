from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer

class InfoPopup(QMessageBox):
    def __init__(self, message, timeout=2000):
        super().__init__()
        self.setWindowTitle("Info")
        self.setText(message)
        self.setStandardButtons(QMessageBox.NoButton)
        QTimer.singleShot(timeout, self.close)
        self.show()

    @staticmethod
    def show_message(message, timeout=2000):
        popup = InfoPopup(message, timeout)
        popup.exec_()
