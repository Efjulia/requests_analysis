import csv
import logging
# Включить, если не надо выводить в консоль параметры обучения и настройки модели
# сообщение от тензофло выпадает когда нет графического процессора GPU, это не ошибка, просто работает медленнее
# logging.getLogger('tensorflow').disabled = True
from log_file_UI import Window1, Window3, Window4
from importer_user_data import importer_data
import sys


from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QErrorMessage,QLabel

from PyQt5.QtGui import QIcon,QPixmap
from my_ui import Ui_MainWindow
from importer import importer
from importer import predobr
from model import model
from tuner_model import tuner_model
from classificator import classification_data
# os.system('cls')
logging.basicConfig(filename='main_log.log', level=logging.DEBUG,
                    format="%(asctime)s - [%(levelname)s] - %(name)s - "
                           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",)
# логин работающего в системе пользователя, глобальная переменная NB!!!!
usver = '1'
# Максимальное количество слов
num_words = 10000
# Максимальная длина заявки
max_request_len = 25
# Количество классов заявок
# 1 - запрос на апгрейд ПО
# 2 - проблема с ПО
# 3 - пролема с аппратной частью
nb_classes = 3

myModel = model()
myclassificator = classification_data()
myimporter = importer()
mypredobr = predobr()
my_tuner_model = tuner_model()

# Наследуемся от виджета из PyQt5.QtWidgets и от класса с интерфейсом
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        SCREEN_SIZE = [400, 400]
        self.setGeometry(400, 400, *SCREEN_SIZE)
        myModel = model()
        self.setWindowIcon(QIcon('icons/icon program.png'))
        ## Изображение
        self.pixmap = QPixmap('NS.jpg')
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        self.image = QLabel(self)
        self.image.move(550, 20)
        self.image.resize(300, 300)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)
        self.setupUi(self)
        # Просмотр лог файла
        self.pushButton_9.setIcon(QIcon('icons/saveas.png'))
        self.pushButton_9.clicked.connect(self.run_log)
        self.pushButton_11.clicked.connect(self.registration)
        self.pushButton_10.clicked.connect(self.auntentification)
        # Запуск импорта файло с текстом
        self.pushButton.clicked.connect(self.impotr_file)
        # Предобработка текстовых данных
        self.pushButton_2.clicked.connect(self.predobr_file)
        # Обучение модели
        self.pushButton_4.clicked.connect(self.fit_my_model)
        # Подбор гиперпараметров нейронной сети, результат сохраняетсяв папку text_dirextory,
        # очищать папку перед каждым запуском, иначе запускается без действий!!!
        self.pushButton_5.clicked.connect(self.tuner_function)
        #запускаем импорт и предобработку пользовательских заявок
        self.pushButton_6.clicked.connect(self.predobr_user_file)
        # запуск классификации пользовательских заявок
        self.pushButton_7.clicked.connect(self.run_user_data)
        # просмотр результата классификации пользовательских заявок
        # self.pushButton_8.clicked.connect(self.run_user_data)
        # просмотр словаря
        self.pushButton_8.clicked.connect(self.tokenizer_look)

    # просмотр словаря токенизотора
    def tokenizer_look(self):
        self.win1 = Window3()
        self.win1.show()


    def tuner_function(self):
        try:
            logging.info(f'Запущена настройка параметров модели')
            my_tuner_model.tuner_model_run()
            ok_dialog = QErrorMessage()
            ok_dialog.setWindowTitle("Успешно")
            ok_dialog.showMessage('Результаты настройке расположены в папке test_directory', "")
            logging.info(f'Настройка параметров модели завершена успешно')
            ok_dialog.exec_()
        except Exception as e:
            logging.info(f'Запущена настройка параметров модели, завершена с проблемой' + str(e))
            ok_dialog = QErrorMessage()
            ok_dialog.setWindowTitle("Ошибка")
            ok_dialog.showMessage('Произошла ошибка' + str(e), "")
            ok_dialog.exec_()


    def fit_my_model(self):
        try:
            logging.info(f'Запущено обучение модели')
            myModel.input_file()
            self.image_update('my_chart_chat.jpg')
            ok_dialog = QErrorMessage()
            ok_dialog.setWindowTitle("Успешно")
            ok_dialog.showMessage('Обучение успешно завершено', "")
            logging.info(f'Обучение модели успешно завершено')
            ok_dialog.exec_()
        except Exception as e:
            ok_dialog = QErrorMessage()
            ok_dialog.setWindowTitle("Ошибка")
            ok_dialog.showMessage('Произошла ошибка' + str(e), "")
            logging.info(f'Запущено обучение имодели, завершено с проблемой' + str(e))
            ok_dialog.exec_()


    def predobr_user_file(self):
        # предобработка текста с  данными
        # пример файлов:
        # input_file_name = 'input_text.csv'
        # output_file_name = 'output.csv'
        input_filename = QFileDialog.getOpenFileName(self, 'Выбрать файл c данными для классификации', '',
                                                     ' Text Files(*.csv);;Все файлы (*)')[0]

        if len(input_filename) > 0:
            logging.info(f'Предобработка для классификации запущена, используется файл:' + str(input_filename))
        else:
            input_filename = "result_output_data.csv"
            logging.info(f'Предобработка для классификации запущена, используется файл по умолчанию')
        try:
            importer_data.import_user_data(input_filename, output_file_name="result_output_data.csv")
            ok_dialog = QErrorMessage()
            ok_dialog.setWindowTitle("Успешно")
            ok_dialog.showMessage('Данные добавлены', "")
            ok_dialog.exec_()
            logging.info(f'Предобработка успешно завершена')
        except Exception as e:
            ok_dialog = QErrorMessage()
            ok_dialog.setWindowTitle("Ошибка")
            ok_dialog.showMessage('Произошла ошибка' + str(e), "")
            logging.info(f'Запущена предобработка, завершена с проблемой' + str(e))
            ok_dialog.exec_()


    def predobr_file(self):
        # импорт данных
        # пример файлов:
        # input_file_name = 'input_text.csv'
        # output_file_name = 'output.csv'
        input_filename = QFileDialog.getOpenFileName(self, 'Выбрать файл c входными данными', '',
                                                         ' Text Files(*.csv);;Все файлы (*)')[0]
        output_filename = QFileDialog.getOpenFileName(self, 'Выбрать файл c выходными данными', '',
                                                          ' Text Files(*.csv);;Все файлы (*)')[0]
        if len(input_filename) > 0 and len(output_filename) > 0:
            logging.info(f'Запущен импорт данных, используются файлы:' + str(input_filename) + str(output_filename))
            try:
                importer.import_from_test(input_filename, output_filename)
                ok_dialog = QErrorMessage()
                ok_dialog.setWindowTitle("Успешно")
                ok_dialog.showMessage('Данные добавлены', "")
                ok_dialog.exec_()
                logging.info(f'Импорт данных успешно завершен')
            except Exception as e:
                ok_dialog = QErrorMessage()
                ok_dialog.setWindowTitle("Ошибка")
                ok_dialog.showMessage('Произошла ошибка' + str(e), "")
                ok_dialog.exec_()
                logging.info(f'Запущен импорт данных, завершено с проблемой' + str(e))
            else:
                ok_dialog = QErrorMessage()
                ok_dialog.setWindowTitle("Ошибка")
                ok_dialog.showMessage('Не выбран файл')
                ok_dialog.exec_()
                logging.info(f'Импорт данных не запущен, не выбран файл')


    def impotr_file(self):
        # импорт данных
        # пример файлов:
        # input_file_name = 'input_text.csv'
        # output_file_name = 'output.csv'
        input_filename = QFileDialog.getOpenFileName(self, 'Выбрать файл c входными данными', '',
                                            ' Text Files(*.csv);;Все файлы (*)')[0]
        output_filename = QFileDialog.getOpenFileName(self, 'Выбрать файл c выходными данными', '',
                                                         ' Text Files(*.csv);;Все файлы (*)')[0]
        if len(input_filename) > 0 and len(output_filename)>0:
            logging.info(f'Запущен импорт данных, используются файлы:' + str(input_filename) + str(output_filename))
            try:
                importer.import_from_test(input_filename, output_filename)
                ok_dialog = QErrorMessage()
                ok_dialog.setWindowTitle("Успешно")
                ok_dialog.showMessage('Данные добавлены', "")
                ok_dialog.exec_()
                logging.info(f'Импорт данных успешно завершен')
            except Exception as e:
                ok_dialog = QErrorMessage()
                ok_dialog.setWindowTitle("Ошибка")
                ok_dialog.showMessage('Произошла ошибка' + str(e), "")
                ok_dialog.exec_()
                logging.info(f'Запущен импорт данных, завершено с проблемой' + str(e))
        else:
            ok_dialog = QErrorMessage()
            ok_dialog.setWindowTitle("Ошибка")
            ok_dialog.showMessage('Не выбран файл')
            ok_dialog.exec_()
            logging.info(f'Импорт данных не запущен, не выбран файл')




    def image_update(self, input_filename):
        self.pixmap1 = QPixmap(input_filename)
        self.pixmap.load(input_filename)

        self.image.resize(590, 390)
        # self.image.u
        self.resize(1200, 500)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)

    def run(self):
        # проверка связи :)
        self.label.setText(" ")
        myModel.input_file()
        self.image_update("my_chart.jpg")
        # fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]

    def run_user_data(self):
        # проверка связи :)
        self.label.setText(" ")
        self.win4 = Window4()
        self.win4.show()
        # self.pushButton.clicked.connect(self.run_classification())


    def run_classification(self):
        self.win4.run_classification()

    def run_log(self):
        # Просмотр лог файла
        self.win1 = Window1()
        self.win1.show()


    def auntentification(self):
        # Аутентификация файл с паролями password_user.csv
        global usver
        logging.info(f'Попытка входа в систему')
        usver = self.lineEdit.text()
        user_from_txt = self.lineEdit.text()
        password_from_txt = self.lineEdit_2.text()
        flag = True
        with open('password_user.csv', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for r in reader:
                user_from_file = r[0]
                password_from_file = r[1]
                if user_from_file == user_from_txt and password_from_txt == password_from_file:
                    flag = False
                    ok_dialog = QErrorMessage()
                    ok_dialog.setWindowTitle("Успешно")
                    ok_dialog.showMessage('Пользователь успешно авторизован', "")
                    logging.info(f'Пользователь '+user_from_txt+' успешно авторизован')
                    self.pushButton.setEnabled(True)
                    self.pushButton_2.setEnabled(True)
                    # self.pushButton_3.setEnabled(True)
                    self.pushButton_4.setEnabled(True)
                    self.pushButton_5.setEnabled(True)
                    self.pushButton_6.setEnabled(True)
                    self.pushButton_7.setEnabled(True)
                    self.pushButton_8.setEnabled(True)
                    self.pushButton_9.setEnabled(True)
                    ok_dialog.exec_()
            if flag:
                error_dialog = QErrorMessage()
                error_dialog.setWindowTitle("Ошибка")
                error_dialog.showMessage('Не найден пользователь или неверный пароль.')
                logging.info(f'Пользователь ' + user_from_txt + ' не авторизован. Не найден пользователь или неверный пароль.')
                self.pushButton.setEnabled(False)
                self.pushButton_2.setEnabled(False)
                # self.pushButton_3.setEnabled(False)
                self.pushButton_4.setEnabled(False)
                self.pushButton_5.setEnabled(False)
                self.pushButton_6.setEnabled(False)
                self.pushButton_7.setEnabled(False)
                self.pushButton_8.setEnabled(False)
                self.pushButton_9.setEnabled(False)
                error_dialog.exec_()

    def registration(self):
        # Регистрация, файл с паролями password_user.csv
        logging.info(f'Регистрация нового пользователя началась')
        global usver
        usver = self.lineEdit.text()
        user_from_txt = self.lineEdit.text()
        password_from_txt = self.lineEdit_2.text()
        flag = False
        with open('password_user.csv', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for r in reader:
                if r:
                    user_from_file = r[0]
                    password_from_file = r[1]
                    if user_from_file == user_from_txt:
                        flag = True
        if flag:
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle("Ошибка")
            error_dialog.showMessage('Такой пользователь зарегистрирован, придумайте новый логин')
            logging.info(f'Регистрация не завершена, такой логин существует')
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            # self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_7.setEnabled(False)
            self.pushButton_8.setEnabled(False)
            self.pushButton_9.setEnabled(False)

            error_dialog.exec_()
        else:
            with open('password_user.csv', "a", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                data = [user_from_txt, password_from_txt, ""]
                writer.writerow(data)
                ok_dialog = QErrorMessage()
                ok_dialog.setWindowTitle("Успешно")
                ok_dialog.showMessage('Пользователь успешно зарегистрирован. Авторизуйтесь')
                logging.info(f'Пользователь '+ user_from_txt +' успешно зарегистрирован')
                self.pushButton.setEnabled(False)
                self.pushButton_2.setEnabled(False)
                # self.pushButton_3.setEnabled(False)
                self.pushButton_4.setEnabled(False)
                self.pushButton_5.setEnabled(False)
                self.pushButton_6.setEnabled(False)
                self.pushButton_7.setEnabled(False)
                self.pushButton_8.setEnabled(False)
                self.pushButton_9.setEnabled(False)
                ok_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())


