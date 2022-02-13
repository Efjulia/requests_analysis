from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QFileDialog, QLabel, QLineEdit, QPushButton, QErrorMessage
from classificator import classification_data
import logging
import csv
logging.basicConfig(filename='main_log.log', level=logging.DEBUG,
                    format="%(asctime)s - [%(levelname)s] - %(name)s - "
                           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",)
class Window1(QWidget):
    # просмотр лог фалов
    def __init__(self):
        super(Window1, self).__init__()
        self.setWindowTitle('Лог файл')
        self.setMinimumWidth(800)
        self.setMinimumHeight(800)
        self.file_path = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', 'Лог-файл (*.log);;Все файлы (*)')[0]
        # self.file_path = 'main_log.log'
        self.le = QPlainTextEdit(self)
        self.le.setGeometry(10,10,780,780)
        with open(self.file_path, 'r') as file:
            self.le.setPlainText(file.read())


class Window2(QWidget):
    # форма для импорта файлов
    def __init__(self):
        super(Window2, self).__init__()
        self.setWindowTitle('Лог файл')
        self.setMinimumWidth(800)
        self.setMinimumHeight(800)
        # self.file_path
        # self.file_path = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', 'Лог-файл (*.log);;Все файлы (*)')[0]
        self.file_path = 'resul_classificatioin.txt'
        self.le = QPlainTextEdit(self)
        self.le.setGeometry(10,10,780,780)
        with open(self.file_path, 'r') as file:
            self.le.setPlainText(file.read())


class Window3(QWidget):
    # просмотр лог фалов
    def __init__(self):
        super(Window3, self).__init__()
        self.setWindowTitle('Словарь токенизатора')
        self.setMinimumWidth(800)
        self.setMinimumHeight(800)
        # self.file_path = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', 'Txt-файл (*.txt);;Все файлы (*)')[0]
        self.file_path = 'tokenizer.txt'
        self.le = QPlainTextEdit(self)
        self.le.setGeometry(10,10,780,780)
        with open(self.file_path, 'r', encoding="utf-8") as file:
            self.le.setPlainText(file.read())


class Window4(QWidget):
    # просмотр лог фалов
    def __init__(self):
        super(Window4, self).__init__()
        self.text = "Заявка"
        self.setWindowTitle('Классификация')
        self.setMinimumWidth(600)
        self.setMinimumHeight(300)
        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 150, 30)
        self.label.setText("Введите строку")
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(10, 40, 600, 30)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QPushButton(self)
        self.pushButton.setText("Начать классификацию")
        self.pushButton.setGeometry(10, 80, 150, 30)
        self.label2 = QLabel(self)
        self.label2.setGeometry(10, 110, 150, 30)
        self.label2.setText(" ")
        self.label3 = QLabel(self)
        self.label3.setGeometry(10, 140, 600, 30)
        self.label3.setText(" ")
        # self.button3.clicked.connect(self.crypt_image)
        self.pushButton.clicked.connect(self.run_classification)

    def read_text(self):
        self.text = self.lineEdit.Text()

    def run_classification(self):
        data = []
        myclassificator = classification_data()
        self.label3.setText("dct jr ")
        self.text = self.lineEdit.text()
        stroka = ";" + self.text
        data.append(stroka)
        logging.info(f'Запущена классификация')
        output_file_name = "result_output_data.csv"
        try:
            # data = ";" + self.text
            with open(output_file_name, "w", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\n')
                writer.writerow(data)
            myclassificator.classification()
            with open('result_classification.csv', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for r in reader:
                    self.label3.setText(r[0])


            ok_dialog = QErrorMessage()
            ok_dialog.setWindowTitle("Успешно")
            ok_dialog.showMessage('Классификация выполнена', "")
            ok_dialog.exec_()
            logging.info(f'Классификация выполнена')
        except Exception as e:
            ok_dialog = QErrorMessage()
            ok_dialog.setWindowTitle("Ошибка")
            ok_dialog.showMessage('Произошла ошибка' + str(e), "")
            ok_dialog.exec_()
            logging.info(f'Классификация не выполнена, завершено с проблемой' + str(e))



