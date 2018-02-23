import sys
import io
import json
import re
import nltk
import numpy
import dateutil.parser
from termcolor import colored
import name_check
import random

from sner import NERClient
tagger = NERClient(host='localhost',port=9199)


class Chapter2_Case:
    """Chapter2_Case objects hold the data extracted from the incoming letter, and the methods needed to update that data"""
    def __init__(self):
        self.id = random.randint(100000, 999999)
        self.email = []
        self.name = []
        self.date = []
        self.logo = []
        self.post = []
        self.to =[]

    def set_email(self, text):
        """Extracts email using regex"""
        re_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')
        match_list = re_pattern.findall(text)
        if match_list:
            self.email.append(match_list[0])

    def set_names(self, text):
        """Extracts person names from block of text"""
        names = []
        tokens = nltk.tokenize.word_tokenize(text)
        #tagged_words = st.tag(tokens)
        tagged_words = tagger.tag(text)
        for word in tagged_words:
            if word[1] == 'PERSON':
                names.append(word[0])
        ###check names against parliament api
        api_check = name_check.check_name(names)
        if api_check is not None:
            self.name.append(api_check[0])
            try:
                self.post.append(api_check[1])

            except IndexError:
                pass
        else:
            self.name.append(names)

    def set_to(self,text):
        """Extracts person names from block of text"""
        to = []
        tokens = nltk.tokenize.word_tokenize(text)
        #tagged_words = st.tag(tokens)
        tagged_words = tagger.tag(text)
        for word in tagged_words:
            
            if word[1] == 'PERSON':
                to.append(word[0])
        print('to{}'.format(to))
        ###check names against parliament api
        api_check = name_check.check_name(to)
        if api_check is not None:
            self.to.append(api_check[0])

        else:
            self.to.append(to)

    def set_date(self, text):
        try:
            date = dateutil.parser.parse(text)
            self.date = date
        except ValueError:
            pass

    def set_logo(self, logo_description):
        self.logo.append(logo_description)
