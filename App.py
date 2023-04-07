from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import *
import sys
import os

import SecondApp
import Neyroset


# Класс графический интерфейс основного окна
class App(QMainWindow):
    effect = -1

    def __init__(self, parent=None):
        super().__init__()
        self.win2 = None  # Внешнего окна пока нет
        self.ui = uic.loadUi("int21.ui")
        self.ui.closeEvent = self.closeEvent
        self.ui.show()
        self.set()
        self.ReadComboBox()


    def ReadComboBox(self):
        files = os.listdir(os.getcwd())

        for file in files:
            arr = file.split('.')
            if (arr[len(arr) - 1].lower() == "csv"):
                self.ui.MNIST.addItem(file)

    # Привязка методов к кнопкам (что кнопки будут вытворять)
    def set(self):
        # Реагирование на клик
        self.ui.clear_buttom.clicked.connect(lambda: self.all_clear())
        self.ui.train_button.clicked.connect(
            lambda: self.obuch_click(teht="<span style=\"color: #5d5;\">Эффективность = </span>"))
        self.ui.save_button.clicked.connect(lambda: self.saveData())
        self.ui.data_button.clicked.connect(lambda: self.show_new_window())

        # Реагирование на изменение индекса в комбобокс
        self.ui.MNIST.activated.connect(lambda: self.warning_combobox())

        # Добавление картинки к сообщениям
        self.ui.CommentButton_2.setIcon(QIcon('ikonka-informacija.jpg'))
        self.ui.CommentButton_3.setIcon(QIcon("ikonka-informacija.jpg"))
        self.ui.CommentButton_1.setIcon(QIcon("ikonka-informacija.jpg"))

        # Коментарии
        self.ui.CommentButton_1.setToolTip(
            'Коэффициент обучения вводится в пределах [0,1]')  # Комменты к гиперпараметрам
        self.ui.CommentButton_2.setToolTip(
            'Количество скрытых узлов не может быть отрицательным, т.к по ним проходит нейросеть для обучения')
        self.ui.CommentButton_3.setToolTip(
            'Количество эпох показывает: сколько раз нейросеть пройдет по дополнительному тренировочному набору,\n'
            ' поэтому, чем больше число, тем дольше будет проходить обучение.')

    # Работа с комбобокс
    def warning_combobox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Рекомендация")
        msg.setText("Перейти в Данные об обучении?")
        msg.setInformativeText('Для каждого набора данных, для более глубокого анализа лучше использовать свою историю обучения')
        msg.setStandardButtons(QMessageBox.Open | QMessageBox.Cancel)
        returnValue = msg.exec()

        if returnValue == QMessageBox.Open:
            self.show_new_window()
            print('OK clicked')

       # def msgButtonClick(i):
       #     print("Button clicked is:", i.text())




    # Открываем 2е окно
    def show_new_window(self):
        if self.win2 is None:
            self.win2 = SecondApp.SecondApp(self)
            return

        self.win2.ui.hide()
        self.win2.ui.show()

    # Запись
    def saveData(self):

        if (self.effect < 0):
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Для записи результата нужно посчитать эффективность!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()  # Показываем окно ошибки пользавателю
            return False
        print("Сохраниение пошло")
        history = SecondApp.History()
        history.SaveValue(self.effect)
        # history.SaveValue(self.effect, self.obuch, self.usel, self.filename)
        self.ui.textEdit.setText("<span style=\"color: #5d5;\">результат записан</span>")

        # чтобы не записать снова тот же результат
        self.effect = -1
        return True

    # Метод очистки полей от введенных значений
    def all_clear(self):
        self.ui.usel.clear()
        self.ui.obuch.clear()
        self.ui.epoh.clear()
        self.ui.textEdit.clear()

    # Метод рассчета значений
    def obuch_click(self, teht):
        self.ui.textEdit.clear()
        zombie = Neyroset.brain()

        # берем веденные значения
        try:
            obuch = float(self.ui.obuch.toPlainText())
            usel = int(self.ui.usel.toPlainText())
            epoh = int(self.ui.epoh.toPlainText())
            file_name = self.ui.MNIST.currentText()
        except:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Гиперпараметры введены неверно!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.setInformativeText("Предупреждение! \nКоличество эпох не может быть отрицательным;"
                                     " \nкоэффициент обучения вводится в пределах [0;1];"
                                     " \nколичество скрытых узлов не может быть отрицательным или дробным.")

            error.exec_()  # Показываем окно ошибки пользавателю
            return

        self.effect = zombie.Calculate(obuch, usel, epoh, file_name)
        self.display(text=str(teht) + str(self.effect))

    def display(self, text):
        dialog = self.ui.textEdit.setText(text)

    def closeEvent(self, event):
        print("Закрываем окно")
        reply = QMessageBox.information(self, 'Выход', 'Вы точно хотите выйти?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.closeAllWindows()  # Закрытие всех окон, которые существуют
            event.accept()
        else:
            event.ignore()


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
