import csv
import os
import logging
# logging.getLogger('tensorflow').disabled = True
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Conv1D, GlobalMaxPooling1D, LSTM, GRU
from tensorflow.keras import utils
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


num_words = 10000
# Максимальная длина заявки
max_request_len = 25
# Количество классов заявок
# 1 - запрос на апгрейд ПО
# 2 - проблема с ПО
# 3 - пролема с аппратной частью
nb_classes = 3
classes = ["functionality", "software", "hardware"]

class model:
    def __init__(self):
        pass

    def build_model(self, hp):
        model = Sequential()
        activation_choice = hp.Choice('activation', values=['relu', 'sigmoid', 'tanh', 'elu', 'selu'])
        model.add(Dense(units=hp.Int('units_input',  # Полносвязный слой с разным количеством нейронов
                                     min_value=512,  # минимальное количество нейронов - 128
                                     max_value=1024,  # максимальное количество - 1024
                                     step=32),
                        input_dim=784,
                        activation=activation_choice))
        model.add(Dense(units=hp.Int('units_hidden',
                                     min_value=128,
                                     max_value=600,
                                     step=32),
                        activation=activation_choice))
        model.add(Dense(10, activation='softmax'))
        model.compile(
            optimizer=hp.Choice('optimizer', values=['adam', 'rmsprop', 'SGD']),
            loss='categorical_crossentropy',
            metrics=['accuracy'])
        return model


    def input_file(self):
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
        print(tokenizer.word_index)
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
        plt.plot(history_cnn.history['accuracy'],
                 label='Доля правильных ответов  на проверочном обучающем наборе')
        plt.plot(history_cnn.history['val_accuracy'],
                 label='Доля правильных ответов на обучающем наборе')
        plt.xlabel('Эпохи')
        plt.ylabel('Доля правильно классифицированных заявок ')
        plt.legend()
        # 590*393
        plt.savefig('my_chart_chat.jpg')
        plt.show()




        model_lstm = Sequential()
        model_lstm.add(Embedding(num_words, 32, input_length=max_request_len))
        model_lstm.add(LSTM(16))
        model_lstm.add(Dense(3, activation='softmax'))
        model_lstm.compile(optimizer='adam',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])
        model_lstm.summary()
        model_lstm_save_path = 'best_model_lstm.h5'
        checkpoint_callback_lstm = ModelCheckpoint(model_lstm_save_path,
                                                   monitor='val_accuracy',
                                                   save_best_only=True,
                                                   verbose=1)
        history_lstm = model_lstm.fit(x_train,
                                      y_train,
                                      epochs=5,
                                      batch_size=128,
                                      validation_split=0.2,
                                      callbacks=[checkpoint_callback_lstm])
        plt.plot(history_lstm.history['accuracy'],
                 label='Доля правильно классифицированных заявок на обучающем наборе')
        plt.plot(history_lstm.history['val_accuracy'],
                 label='Доля правильно классифицированных заявок на проверочном наборе')
        plt.xlabel('Эпохи')
        plt.ylabel('Доля правильно классифицированных заявок ')
        plt.legend()
        plt.show()

        prediction = model_lstm.predict(x_train[:1])


        model_gru = Sequential()
        model_gru.add(Embedding(num_words, 32, input_length=max_request_len))
        model_gru.add(GRU(16))
        model_gru.add(Dense(3, activation='softmax'))

        model_gru.compile(optimizer='adam',
                          loss='categorical_crossentropy',
                          metrics=['accuracy'])
        model_gru.summary()
        model_gru_save_path = 'best_model_gru.h5'
        checkpoint_callback_gru = ModelCheckpoint(model_gru_save_path,
                                                  monitor='val_accuracy',
                                                  save_best_only=True,
                                                  verbose=1)
        history_gru = model_gru.fit(x_train,
                                    y_train,
                                    epochs=5,
                                    batch_size=128,
                                    validation_split=0.2,
                                    callbacks=[checkpoint_callback_gru])
        plt.plot(history_gru.history['accuracy'],
                 label='Доля правильных ответов на обучающем наборе')
        plt.plot(history_gru.history['val_accuracy'],
                 label='Доля правильных ответов на проверочном наборе')
        plt.xlabel('Эпохи')
        plt.ylabel('Доля правильно классифицированных заявок ')
        plt.legend()
        plt.show()

        test = pd.read_csv('test_text_request.csv',
                           header=None,
                           names=['class', 'text'], delimiter=";")

        test_sequences = tokenizer.texts_to_sequences(test['text'])
        x_test = pad_sequences(test_sequences, maxlen=max_request_len)
        # print(x_test[:1])
        y_test = utils.to_categorical(test['class'] - 1, nb_classes)
        # print(y_test)
        # model_cnn.load_weights(model_cnn_save_path)
        # model_cnn.evaluate(x_test, y_test, verbose=1)
        # model_lstm.load_weights(model_lstm_save_path)
        # model_gru.load_weights(model_gru_save_path)
        # model_gru.evaluate(x_test, y_test, verbose=1)
        test_text = pd.read_csv('test_test.csv',
                           header=None,
                           names=['class', 'text'], delimiter=";")
        model = load_model("best_model_lstm.h5")
        # model_cnn = Sequential()
        # model_cnn = load_model(model_cnn_save_path)
        print(test_text["text"])
        test_sequences = tokenizer.texts_to_sequences(test_text["text"])
        x = pad_sequences(test_sequences, maxlen=max_request_len)
        print(x)
        prediction = model.predict(x)
        print(prediction)
        prediction = np.argmax(prediction)
        print("Номер класса:", prediction + 1)
        print("Название класса:", classes[prediction])

# myModel = model()
# myModel.input_file()


