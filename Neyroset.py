# Модули
import numpy
import scipy.special

class intell:
    # методы
    # Инициализация
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # задаем кол-во узлов:
        self.inodes = inputnodes  # во входном
        self.hnodes = hiddennodes  # в скрытом
        self.onodes = outputnodes  # в выходном слое
        print("Обучение началось")
        self.wih = numpy.random.rand(self.hnodes, self.inodes) - 0.5
        self.who = numpy.random.rand(self.onodes, self.hnodes) - 0.5

        # коэффициент обучения
        self.lr = learningrate
        # Быстрое создание функции лямбда-выражение.
        # Использование сигмоиды в качестве функции активации
        self.activation_function = lambda x: scipy.special.expit(x)

        pass

    # Тренировка
    def train(self, inputs_list, targets_list):
        # Преобразует список входных значений в 2-мерный массив
        inputs = numpy.array(inputs_list, ndmin=2).T
        # Преобразует массив также как и "inputs"
        targets = numpy.array(targets_list, ndmin=2).T

        # вычисление сигналов в скрытом слое
        hidden_inputs = numpy.dot(self.wih, inputs)

        # вычисление сигналов, исходящих от скрытого слоя
        hidden_outputs = self.activation_function(hidden_inputs)

        # вычисление сигналов в конечном выходном слое
        final_inputs = numpy.dot(self.who, hidden_outputs)

        # вычисление сигналов, поступающих из конечного выходного слоя
        final_outputs = self.activation_function(final_inputs)

        # Ошибка = целевое значение - фактическое
        output_errors = targets - final_outputs
        # Распределение пропорционально весовым коэффициентам связей
        hidden_errors = numpy.dot(self.who.T, output_errors)
        # Обновить весовые коэффициенты для связей между скрытым и выходными слоями
        self.who += self.lr * numpy.dot((output_errors * final_outputs *
                                         (1.0 - final_outputs)), numpy.transpose(hidden_outputs))
        # Обновить весовые коэффициенты для связей между входным и скрытым слоями
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs *
                                         (1.0 - hidden_outputs)), numpy.transpose(inputs))
        print("Тренировка окончена")
        pass

    # опрос нейронной сети
    def query(self, inputs_list):
        # преобразовать список входных значений
        # в двумерный массив
        inputs = numpy.array(inputs_list, ndmin=2).T

        # Рассчитать входящие сигналы для скрытого слоя
        hidden_inputs = numpy.dot(self.wih, inputs)
        # Рассчитать выходящие сигналы для скрытого слоя
        hidden_outputs = self.activation_function(hidden_inputs)

        # Рассчитать входящие сигналы для выходного слоя
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # Рассчитать исходящие сигналы для выходного слоя
        final_outputs = self.activation_function(final_inputs)
        print("Опрос завершен")
        return final_outputs


# Класс вычислений
class brain:
    def Calculate(self, learning_rate=0.3, hidden_nodes=100, epochs=6, file_name="10.csv"):
        input_nodes = 784  # Кол-во входных узлов из-за разрешения 28х28
        output_nodes = 10  # Кол-во выходных узлов

        n = intell(input_nodes, hidden_nodes, output_nodes, learning_rate)

        # Открываем файл
        train_data_file = open(file_name, 'r')
        train_data_list = train_data_file.readlines()
        train_data_file.close()

        # Перебираем все записи MNIST для тренировки нейронной сети
        for record in train_data_list:
            all_values = record.split(',')
            # Масштабируем БД
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            # zeros -приравнивает элементы массива к 0
            targets = numpy.zeros(output_nodes) + 0.01
            # Целевое маркерное значение all_vaues[0]
            # т.е нужный нам элемент приравниваем к 0.99
            targets[int(all_values[0])] = 0.99
            n.train(inputs, targets)
            print("Прогоняем по тренировочному набору данных")



        # Открываем файл для нового тестового набора
        test_data_file = open(file_name, 'r')
        test_data_list = test_data_file.readlines()
        test_data_file.close()

        # Перебираем все записи для нового тестового набора
        for e in range(epochs):
            for record in train_data_list:
                all_values = record.split(',')
                inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
                targets = numpy.zeros(output_nodes) + 0.01
                targets[int(all_values[0])] = 0.99
                n.train(inputs, targets)

        # Наш журнал записи
        scorecard = []
        for record in test_data_list:
            all_values = record.split(',')
            correct_label = int(all_values[0])
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            outputs = n.query(inputs)
            label = numpy.argmax(outputs)
            if (label == correct_label):
                scorecard.append(1)  # Верно
            else:
                scorecard.append(0)  # Неверно

        # Наш показатель
        print(scorecard)
        scorecard_array = numpy.asarray(scorecard)
        effect = scorecard_array.sum() / scorecard_array.size
        print("Эффективность = ", effect)
        return effect
