# https://github.com/tatiblockchain/python-deep-learning-chatbot


from pathlib import Path
import random
import json
from tensorflow.keras.models import load_model
# from keras.models import load_model
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# intents = json.loads(open('job_intents.json', encoding='utf-8').read())
BASE_DIR = Path(__file__).resolve().parent

print(BASE_DIR)


class OyeBot:
    def __init__(self, intent_data):
        self.intents = json.loads(json.dumps(intent_data))
        self.words = pickle.load(open(BASE_DIR/'data/words.pkl', 'rb'))
        self.classes = pickle.load(open(BASE_DIR/'data/classes.pkl', 'rb'))
        self.model = load_model(BASE_DIR/'data/chatbot_model.h5')

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(
            word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

    def bow(self, sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return(np.array(bag))

    def predict_class(self, sentence, model):
        # filter out predictions below a threshold
        p = self.bow(sentence, self.words, show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.15
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append(
                {"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def getResponse(self, ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag'] == tag):
                result = random.choice(i['responses'])
                break
            else:
                result = "You must ask the right questions"
        return result

    def startChat(self, msg):
        ints = self.predict_class(msg, self.model)
        res = self.getResponse(ints, self.intents)
        return res
