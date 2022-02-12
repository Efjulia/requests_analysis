from tensorflow.keras.datasets import fashion_mnist
import logging
# logging.getLogger('tensorflow').disabled = True
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import utils
from keras_tuner.tuners import RandomSearch, Hyperband, BayesianOptimization
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


class tuner_model():
    num_words = 10000
    # Максимальная длина заявки
    max_request_len = 25
    # Количество классов заявок
    # 1 - запрос на апгрейд ПО
    # 2 - проблема с ПО
    # 3 - пролема с аппратной частью
    nb_classes = 3
    classes = ["functionality", "software", "hardware"]

    def __init__(self):
        pass

    def build_model(hp):
        model = Sequential()
        activation_choice = hp.Choice('activation', values=['relu', 'sigmoid', 'tanh', 'elu', 'selu'])
        model.add(Dense(units=hp.Int('units_input',  # Полносвязный слой с разным количеством нейронов
                                     min_value=512,  # минимальное количество нейронов - 128
                                     max_value=1024,  # максимальное количество - 1024
                                     step=32),
                        input_dim=25,
                        activation=activation_choice))
        model.add(Dense(units=hp.Int('units_hidden',
                                     min_value=128,
                                     max_value=600,
                                     step=32),
                        activation=activation_choice))
        model.add(Dense(3, activation='softmax'))
        model.compile(
            optimizer=hp.Choice('optimizer', values=['adam', 'rmsprop', 'SGD']),
            loss='categorical_crossentropy',
            metrics=['accuracy'])
        return model

    def tuner_model_run(self):
        num_words = 10000
        # Максимальная длина заявки
        max_request_len = 25
        # Количество классов заявок
        # 1 - запрос на апгрейд ПО
        # 2 - проблема с ПО
        # 3 - пролема с аппратной частью
        nb_classes = 3
        classes = ["functionality", "software", "hardware"]
        train = pd.read_csv('train_text_request.csv',
                            header=None,
                            names=['class', 'text'], delimiter=';')
        # используем для обучения текст заявки
        text_request = train['text']
        # создаем вектор выходных значений по названию классов заявок
        y_train = utils.to_categorical(train['class'] - 1, nb_classes)
        tokenizer = Tokenizer(num_words=num_words)
        tokenizer.fit_on_texts(text_request)
        # печатаем словарь, построенный токенизатором
        # print(tokenizer.word_index)
        # Преобразуем текст обращения в числовое представление
        sequences = tokenizer.texts_to_sequences(text_request)
        # Просматриваем текст обращения в числовом представлении
        index = 22
        x_train = pad_sequences(sequences, maxlen=max_request_len)

        tuner = RandomSearch(
            tuner_model.build_model,  # функция создания модели
            objective='val_accuracy',  # метрика, которую нужно оптимизировать -
            # доля правильных ответов на проверочном наборе данных
            max_trials=80,  # максимальное количество запусков обучения
            directory='test_directory'  # каталог, куда сохраняются обученные сети
        )
        tuner.search_space_summary()
        tuner.search(x_train,  # Данные для обучения
                     y_train,  # Правильные ответы
                     batch_size=256,  # Размер мини-выборки
                     epochs=20,  # Количество эпох обучения
                     validation_split=0.2,  # Часть данных, которая будет использоваться для проверки
                     )
        models = tuner.get_best_models(num_models=3)
        test_text = pd.read_csv('output.csv',
                                header=None,
                                names=['class', 'text'], delimiter=";")

        test_sequences = tokenizer.texts_to_sequences(test_text["text"])
        x = pad_sequences(test_sequences, maxlen=max_request_len)
        x_test = x
        y_test = utils.to_categorical(test_text['class'] - 1, nb_classes)
        for model in models:
            model.summary()
            model.evaluate(x_test, y_test)
            print("*************************************************")


