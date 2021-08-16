from pathlib import Path
import random
from tensorflow.keras.optimizers import SGD
# from keras.optimizers import SGD
from tensorflow.keras.layers import Dense, Activation, Dropout
# from keras.models import Sequential
from tensorflow.keras import Sequential
import numpy as np
import pickle
import json
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('punkt')
nltk.download('wordnet')

BASE_DIR = Path(__file__).resolve().parent


class Proccess_Data:
    def __init__(self, intent_data):
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_words = ['?', '!']
        # data_file = open('job_intents.json', encoding='utf-8').read()
        self.intents = json.loads(json.dumps(intent_data))
        self.lemmatizer = WordNetLemmatizer()

    def start_process(self):

        for intent in self.intents['intents']:
            for pattern in intent['patterns']:

                w = nltk.word_tokenize(pattern)
                self.words.extend(w)

                self.documents.append((w, intent['tag']))

                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [self.lemmatizer.lemmatize(
            w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))

        self.classes = sorted(list(set(self.classes)))

        print(len(self.documents), "documents")

        print(len(self.classes), "classes", self.classes)

        print(len(self.words), "unique lemmatized words", self.words)

        pickle.dump(self.words, open(BASE_DIR/'data/words.pkl', 'wb'))
        pickle.dump(self.classes, open(BASE_DIR/'data/classes.pkl', 'wb'))

        # initializing training data
        training = []
        output_empty = [0] * len(self.classes)
        for doc in self.documents:

            bag = []

            pattern_words = doc[0]
            pattern_words = [self.lemmatizer.lemmatize(
                word.lower()) for word in pattern_words]

            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1

            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)
        # create train and test lists. X - patterns, Y - intents
        train_x = list(training[:, 0])
        train_y = list(training[:, 1])
        print("Training data created")

        # Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
        # equal to number of intents to predict output intent with softmax
        model = Sequential()
        model.add(Dense(128, input_shape=(
            len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd, metrics=['accuracy'])

        # fitting and saving the model
        hist = model.fit(np.array(train_x), np.array(train_y),
                         epochs=200, batch_size=5, verbose=1)
        model.save(BASE_DIR/'data/chatbot_model.h5', hist)

        print("model created")
