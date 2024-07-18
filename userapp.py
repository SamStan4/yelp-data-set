import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from data_base_interface import execute_query
from data_base_interface import sql_clean_string

front_end_file_path = "./user_interface.ui"

if not os.path.exists(front_end_file_path):
    raise FileNotFoundError(f"ERROR {front_end_file_path} not found")

ui_main_window, qt_base_class = uic.loadUiType(front_end_file_path)

class yelp_data_interface(QMainWindow):
    def __init__(self) -> None:
        super(yelp_data_interface, self).__init__()
        self.ui = ui_main_window()
        self.ui.setupUi(self)



def main() -> int:
    app = QApplication(sys.argv)
    window = yelp_data_interface()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()