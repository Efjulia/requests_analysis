import csv


class importer_data:
# класс для загрузки данных из файлов обращений сотрудников и  бд
    def import_user_data(self, input_file_name="result_input_data.csv", output_file_name="result_output_data.csv"):
        # Функция для импортирования данных
        # по умолчанию файлы называются
        # input_file_name = 'result_input_data.csv'
        # output_file_name = 'result_output_data.csv'
        try:
            with open(input_file_name, encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                data = []
                for index, row in enumerate(reader):
                    data_1 = []
                    data_1 = row[4].split('"')
                    # класс не указываем, т.к. это реальные данные для классификации
                    stroka = " ;" + str(data_1[0])
                    data.append(stroka)
            with open(output_file_name, "a", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\n')
                writer.writerow(data)
            return 'Данные загружены'
        except Exception as e:
            return 'Ошибка загрузки данных' + str(e)


