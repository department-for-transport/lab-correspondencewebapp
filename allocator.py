import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import string
import unicodedata
import sys
from nltk.corpus import stopwords
import pickle


class NeuralNet():
    def __init__(self, modelpath, wordpath, categorypath):
        self.model = None
        self.modelpath = modelpath
        self.stemmer = LancasterStemmer()
        self.words = wordpath
        self.categories = categorypath
    def load_model(self):
        with open('{}'.format(self.words), 'rb') as f:
            self.words = pickle.load(f)
        with open('{}'.format(self.categories), 'rb') as f:
            self.categories = pickle.load(f)
            #net is expecting a shape the size of the bag of words
            net = tflearn.input_data(shape=[None,len(self.words)])
            #layer?
            net = tflearn.fully_connected(net,8)
            #layer?
            net = tflearn.fully_connected(net,8)
            #output layer
            net = tflearn.fully_connected(net, len(self.categories),activation='softmax')
            net = tflearn.regression(net)

            self.model = tflearn.DNN(net)
            self.model.load('{}'.format(self.modelpath))
    def create_bow(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.stemmer.stem(word.lower()) for word in sentence_words]
        BoW = [0]*len(self.words)
        for s in sentence_words:
            for i, w in enumerate(self.words):
                if w==s:
                    BoW[i]=1
        return(np.array(BoW))


    def predict(self, query):
        unit = self.categories[np.argmax(self.model.predict([self.create_bow(query)]))]
        return unit
