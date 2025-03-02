import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox
from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeForm_ui import Ui_Dialog


class EditCoffee(QDialog, Ui_Dialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)

        self.setupUi(self)
        self.coffe_id = coffee_id
        self.saveButton.clicked.connect(self.save_coffee)
        self.cancelButton.clicked.connect(self.reject)

        if self.coffe_id:
            self.load_element()

    def load_element(self):
        conn = sqlite3.connect('data/coffee.sqlite')
        cur = conn.cursor()
        res = cur.execute("SELECT * FROM coffee WHERE id = ?", (self.coffe_id,)).fetchone()

        if res:
            self.nameLineEdit.setText(res[1])
            self.roastLineEdit.setText(res[2])
            self.groundedBeansLineEdit.setText(res[3])
            self.tasteLineEdit.setText(res[4])
            self.priceLineEdit.setText(str(res[5]))
            self.volumeLineEdit.setText(str(res[6]))
        conn.close()

    def save_coffee(self):
        name = self.nameLineEdit.text()
        roast = self.roastLineEdit.text()
        grounded_beans = self.groundedBeansLineEdit.text()
        taste = self.tasteLineEdit.text()
        price = self.priceLineEdit.text()
        volume = self.volumeLineEdit.text()

        if not name or not roast or not grounded_beans or not taste or not price or not volume:
            QMessageBox.warning(self, "Error", "Все поля должны быть заполнены")
            return

        conn = sqlite3.connect('data/coffee.sqlite')
        cur = conn.cursor()
        if self.coffe_id:
            cur.execute(
                "UPDATE coffee SET name=?, roast_level=?, grounded_beans=?, taste=?, price=?, volume=? WHERE id=?",
                (name, roast, grounded_beans, taste, price, volume, self.coffe_id))
        else:
            cur.execute(
                "INSERT INTO coffee (name, roast_level, grounded_beans, taste, price, volume) VALUES (?, ?, ?, ?, ?, ?)",
                (name, roast, grounded_beans, taste, price, volume))

        conn.commit()
        conn.close()
        self.accept()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.load_data()
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

    def load_data(self):
        conn = sqlite3.connect('data/coffee.sqlite')
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

    def add_coffee(self):
        dialog = EditCoffee(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def edit_coffee(self):
        selected_row = int(self.tableWidget.currentRow())
        if selected_row == -1:
            QMessageBox.warning(self, "Error", 'Нужно выбрать ячейку таблицы, которую хотите редактировать')
            return

        coffe_id = self.tableWidget.item(selected_row, 0).text()
        dialog = EditCoffee(self, coffe_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
