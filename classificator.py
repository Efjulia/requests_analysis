from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Conv1D, GlobalMaxPooling1D
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils
import pandas as pd
import numpy as np
import csv
import pickle



num_words = 10000
# Максимальная длина заявки
max_request_len = 25
# Количество классов заявок
# 1 - запрос на апгрейд ПО
# 2 - проблема с ПО
# 3 - пролема с аппратной частью
nb_classes = 3
classes = ["functionality", "software", "hardware"]

class classification_data:
    def __init__(self):
        pass

    def classification(self):
        # данные для обучения модели, в файле сначала номер класса,
        # к которому принадлежит заявка, далее сам текст заявки
        train = pd.read_csv('output.csv',
                            header=None,
                            names=['class', 'text'], delimiter=';')
        # используем для обучения текст заявки
        text_request = train['text']
        # создаем вектор выходных значений по названию классов заявок
        y_train = utils.to_categorical(train['class'] - 1, nb_classes)
        # print(y_train)
        tokenizer = Tokenizer(num_words=num_words)
        tokenizer.fit_on_texts(text_request)
        # печатаем словарь, построенный токенизатором
        # print(tokenizer.word_index, type(tokenizer.word_index))
        token = list(tokenizer.word_index.items())
        try:
            # for key, val in tokenizer.word_index.items():
            #     out.write('{}:{}\n'.format(key, val))
            with open("tokenizer.txt", "w", encoding="utf-8") as file:
                for elem in token:
                    file.write(str(elem) + "\n")
                # writer.writerow(list(tokenizer.word_index.items()))
            print('Данные загружены в словарь')
        except Exception as e:
            print('Ошибка загрузки данных в словарь' + str(e))

        # Преобразуем текст обращения в числовое представление
        sequences = tokenizer.texts_to_sequences(text_request)
        # Просматриваем текст обращения в числовом представлении
        index = 22
        x_train = pad_sequences(sequences, maxlen=max_request_len)


        model_cnn = Sequential()
        model_cnn.add(Embedding(num_words, 32, input_length=max_request_len))
        model_cnn.add(Conv1D(250, 5, padding='valid', activation='relu'))
        model_cnn.add(GlobalMaxPooling1D())
        model_cnn.add(Dense(128, activation='relu'))
        model_cnn.add(Dense(3, activation='softmax'))
        model_cnn.compile(optimizer='adam',
                          loss='categorical_crossentropy',
                          metrics=['accuracy'])
        model_cnn.summary()
        model_cnn_save_path = 'best_model_cnn.h5'
        checkpoint_callback_cnn = ModelCheckpoint(model_cnn_save_path,
                                                  monitor='val_accuracy',
                                                  save_best_only=True,
                                                  verbose=1)
        model_cnn_save_path = 'best_model_cnn.h5'
        checkpoint_callback_cnn = ModelCheckpoint(model_cnn_save_path,
                                                  monitor='val_accuracy',
                                                  save_best_only=True,
                                                  verbose=1)
        history_cnn = model_cnn.fit(x_train,
                                    y_train,
                                    epochs=5,
                                    batch_size=128,
                                    validation_split=0.2,
                                    callbacks=[checkpoint_callback_cnn])

        test = pd.read_csv('test_text_request.csv',
                           header=None,
                           names=['class', 'text'], delimiter=";")

        test_sequences = tokenizer.texts_to_sequences(test['text'])
        x_test = pad_sequences(test_sequences, maxlen=max_request_len)
        y_test = utils.to_categorical(test['class'] - 1, nb_classes)
        # model_cnn.load_weights(model_cnn_save_path)
        test_text = pd.read_csv('result_output_data.csv',
                           header=None,
                           names=['class', 'text'], delimiter=";")
        model = load_model("best_model_lstm.h5")

        # print(test_text["text"])
        test_sequences = tokenizer.texts_to_sequences(test_text["text"])
        # print(test_sequences)
        x = pad_sequences(test_sequences, maxlen=max_request_len)
        # print(x)
        prediction = model.predict(x)
        # print(prediction)
        prediction = np.argmax(prediction)
        print("Номер класса:", prediction + 1)
        print("Название класса:", classes[prediction])



