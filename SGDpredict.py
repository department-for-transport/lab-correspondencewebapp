from textblob import TextBlob
import numpy as np
import pandas as pd
import pickle


class SGDModel:

    def __init__(self):
        self.model = None
        self.categories = ['Buses and Taxis','Driver and Vehicle Licensing Agency',
        'High Speed Rail', 'Maritime And Coastguard Agency','Rail Passenger Services',
    '   Road Investment Strategy Client', 'low_group',]

    def load(self, path):
        with open('{}'.format(path), 'rb') as f:
            self.model = pickle.load(f)

    def predict(self, sentence_in):
        s = pd.DataFrame({'summary_cleaned': [sentence_in]})
        prediction = self.model.predict(s)
        return self.categories[int(prediction)]
