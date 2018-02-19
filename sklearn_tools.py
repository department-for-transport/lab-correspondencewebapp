from textblob import TextBlob
from sklearn.metrics import (confusion_matrix, classification_report,
                             roc_auc_score)
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.stem.lancaster import LancasterStemmer


class LemmaTokenizer(object):
    '''
    Lemmatizes text using TextBlob (NLTK) - can be used as a tokenizer blass in
    SKlearn vectorizers.
    e.g. CountVectorizer(tokenizer=LemmaTokenizer)
    '''

    def __init__(self, stem=False):
        self.stem = stem
        if stem:
            self.stemmer = LancasterStemmer()
        pass

    def __call__(self, doc):
        tb = TextBlob(doc)
        tb = tb.words.lemmatize()

        if self.stem:
            tb = [self.stemmer.stem(word) for word in tb]

        return tb


def nice_report(grid, actual, test_data):
    '''
    Print out some useful metrics from an SKlearn pipeline
    '''

    def ruler():
        print('-' * 50)

    print('Best Params: \t {}'.format(grid.best_params_))
    print('Best Score: \t {}'.format(grid.best_score_))
    ruler()

    prediction = grid.predict(test_data)
    print('Confusion Matrix: \n {}'.format(
        confusion_matrix(actual, prediction)))
    ruler()

    print(classification_report(actual, prediction))
    ruler()

    print(roc_auc_score(actual, prediction))
    ruler()


class DataFrameSelector(BaseEstimator, TransformerMixin):
    '''
    Expects a DataFrame to be passed and a list of attributes to extract
    '''

    def __init__(self, attribute_names=[]):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.attribute_names].values
