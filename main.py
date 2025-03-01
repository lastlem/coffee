import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.uic import loadUi


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cur = conn.cursor()

        result = cur.execute("SELECT * FROM coffee").fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        column_names = ["Id", "Name", "Roast Level", "Grounded/Beans", "Taste", "Price", "Volume"]
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for i, row in enumerate(result):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
