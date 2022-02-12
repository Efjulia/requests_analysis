from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QFileDialog


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