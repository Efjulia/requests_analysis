import csv
import re

class importer:
# класс для загрузки данных из файлов обращений сотрудников и  бд, полученных из интернета
    def import_from_outdate(self, input_file_name, output_file_name):
    # Функция для импортирования данных из теста от сотрудников первого филиала
    # не забыть поменять класс для каждой категории!!!!!!!
    # input_file_name = 'test1.csv'
    # output_file_name = 'test_1.csv'
        try:
            with open(input_file_name, encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                data = []
                for index, row in enumerate(reader):

                    data_1 = []
                    data_1 = row[0].split('"')
                    # print(data_1[0])

                    data_2 = []
                    data_2 = str(data_1[0]).split(',')
                    if len(data_2) > 1 :
                        if data_2[1] != '':
                            # print(data_2[1])
                            stroka = "2;" + str(data_2[1])
                            data.append(stroka)

            with open(output_file_name, "a", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\n')
                writer.writerow(data)
            return 'Данные загружены'
        except Exception as e:
            return 'Ошибка загрузки данных' + str(e)


    def import_from_first_test(self, input_file_name, output_file_name):
        # Функция для импортирования данных из теста от сотрудников второго филиала
        # не забыть поменять класс для каждой категории!!!!!!!
        # input_file_name = 'test 05122021.csv'
        # output_file_name = 'prom123.csv'
        try:
            with open(input_file_name, encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                data = []
                for index, row in enumerate(reader):
                    data_1 = []
                    data_1 = row[3].split('"')
                    stroka = "2;" + str(data_1[0])
                    data.append(stroka)
                # print(data)
            with open(output_file_name, "a", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\n')
                writer.writerow(data)
            return 'Данные загружены'
        except Exception as e:
            return 'Ошибка загрузки данных' + str(e)


    def import_from_second_db(self, input_file_name, output_file_name):
        # Функция для импортирования данных из теста от сотрудников третьего филиала
        # не забыть поменять класс для каждой категории!!!!!!!
        # input_file_name = 'SampleInput.csv'
        # output_file_name = 'prom.csv'
        try:
            with open(input_file_name, encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                data = []
                for index, row in enumerate(reader):
                    data.append(row[0])
                # print(data)
            with open(output_file_name, "a", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\n')
                writer.writerow(data)
            return 'Данные загружены'
        except Exception as e:
            return 'Ошибка загрузки данных' + str(e)


    def import_from_test(input_file_name, output_file_name):
        # Функция для импортирования данных из теста от сотрудников второго филиала
        # не забыть поменять класс для каждой категории!!!!!!!
        # input_file_name = 'test 05122021.csv'
        # output_file_name = 'prom123.csv'
        try:
            # print('Данные загружены')
            with open(input_file_name, encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                data = []
                for index, row in enumerate(reader):
                    data_1 = []
                    data_1 = row[3].split('"')
                    stroka = "2;" + str(data_1[0])
                    data.append(stroka)
                # print(data)
            with open(output_file_name, "a", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\n')
                writer.writerow(data)
            return 'Данные загружены'
        except Exception as e:
            return 'Ошибка загрузки данных' + str(e)


class predobr:
    # Объявляем функцию приведения строки к нижнему регистру
    def lower(input_file_name, output_file_name):
        try:
            with open(input_file_name, encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                data = []
                for index, row in enumerate(reader):

                    data_1 = []
                    data_1 = row[0].split('"')
                    # print(data_1[0])

                    data_2 = []
                    data_2 = str(data_1[0].lower()).split(',')
                    if len(data_2) > 1 :
                        if data_2[1] != '':
                            # print(data_2[1])
                            stroka = "2;" + str(data_2[1]).lower()
                            data.append(stroka.lower())

            with open(output_file_name, "a", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\n')
                writer.writerow(data)
            return 'Данные преобразованы'
        except Exception as e:
            return 'Ошибка преобразования данных' + str(e)
        # return str.lower()

    # Метод для  деления строки по ряду символов. Возвращает массив слов
    def splitstring(self, str):
        words = []
        # разбиваем строку по символам из [], символы подбирали опытным путем
        for i in re.split('[;,.,\n,\s,:,-,+,-,(,),=,-,/,«,»,-,@,-,-,\d,!,?,"]', str):
            words.append(i)
        return words
