import matplotlib.pyplot as plt

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget,  QApplication
import sys
import os

# Класс построения тхт файла с историей эффективности с дальнейшим построением графика
class History:

    def SaveValue(self, value, file_name="history.txt"):
        # Получаем последний ID

        last_id = 0;
        # Если файла нет - то значит тут будет ошибка так как нечего читать
        try:
            with open(file_name, "r") as file:
                lines = file.readlines()
                last_id = len(lines)

            # Если записей не было, то не меняем значение
            if (len(lines) > 0):
                last_id = int(str.split(lines)[0])
            f_read.close()
        except:
            pass

        # Записываем результат
        f_write = open(file_name, "a+")
        f_write.write(str(last_id + 1) + " " + str(value) + "\n")
        f_write.close()

    def ShowGraph(self, file_name="history.txt"):
        data_x = []
        data_y = []
        try:
            f_read = open(file_name, "r")
            lines = f_read.readlines()

            for line in lines:
                arr = str.split(line)  # Возвращает str строковую версию объекта
                data_x.append(
                    int(arr[0]))  # append() добавляет в конец списка элемент, переданный ему в качестве аргумента.
                data_y.append(float(arr[1]))
        except:
            return False

        try:
            plt.plot(data_x, data_y)  # Отображение y и x в виде линий
            plt.title("График истории эффективности")
            plt.xlabel("Номер попытки")  # ось абсцисс
            plt.ylabel("Эффективность")  # ось ординат
            plt.grid()  # Настройка линии сетки
            plt.show()  # Показать график
        except:
            return False

        return True

# Второе окно
class SecondApp(QWidget):
    history = History()

    def __init__(self, parent=None):
        super(SecondApp, self).__init__(parent)
        self.ui = uic.loadUi("int22.ui")
        self.ui.show()
        self.set2()
        self.ReadComboBox_2()

    def ReadComboBox_2(self):
        files = os.listdir(os.getcwd())

        for file in files:
            arr = file.split('.')
            if (arr[len(arr) - 1].lower() == "txt"):
                self.ui.combo_history.addItem(file)

    def set2(self):
        self.ui.history_button.clicked.connect(lambda: self.drawData())
        self.ui.new_history_button.clicked.connect(lambda: self.NewHistory())

    def NewHistory(self):
        print("Так")

    def drawData(self):
        print("Мб работает")
        if self.history.ShowGraph():
            print("ok")
        else:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("График не построен. Возникла ошибка!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()  # Показываем окно ошибки пользавателю
