import sys
import io
import json
import re
import nltk
import numpy
import dateutil.parser
from termcolor import colored
import name_check
from helpers import Chapter2_Case

from sner import NERClient

#if tagger isn't running on a server, you can instaniate it here, but it's slow!
#from nltk.tag.stanford import StanfordNERTagger
#t = StanfordNERTagger('/home/zach/chapter2/chapterocr/stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')

#get google cloud APIs
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import storage



#Connect to bucket and check contents (requires API key in local service-accout.json file)
def list_images(bucket_name):
    """Lists all the images in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()
    image_list = []
    for blob in blobs:
        image_list.append(blob.name)
    return image_list


def detect_address_quadrant(block,page_dimensions):
    """Detects if block is in upper right quadrant"""
    #keep track of dimensions within quadrant
    i = 0
    #test dimensions
    for dim in block.bounding_box.vertices:
        if ((dim.x>0.5*page_dimensions[0]) and (dim.y<0.5*page_dimensions[1])) or (dim.y<0.2*page_dimensions[1]) or (dim.y>0.8*page_dimensions[1]):
            i+=1
    #if all 4 quadrants within boundary
    if i == 4:
        return True

def detect_sender_quadrant(block,page_dimensions):
    """Detects if block is in upper right quadrant"""
    #keep track of dimensions within quadrant
    j = 0
    #test dimensions
    for dim in block.bounding_box.vertices:
        if (dim.x<0.7*page_dimensions[0]) and (dim.y<0.5*page_dimensions[1]):
            j+=1
    #if all 4 polylines within boundary
    if j == 4:
        return True


def create_chapter2_case(uri):
    """takes image location, gets image of correspondence from google cloud bucket and returns a chapter2_case object using the data from the image"""

    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    #get text for analysis
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    #get logo
    response = client.logo_detection(image=image)
    #instantiate chapter2_case object
    chapter2_case = Chapter2_Case()

    #set logo field
    logos = response.logo_annotations
    for logo in logos:
        chapter2_case.set_logo(logo.description)
        break

    for page in document.pages:
        #get dimensions of page
        dimensions = (page.width,page.height)

        #extract each text block from top right quadrant and format it
        for block in page.blocks:

            if detect_address_quadrant(block, dimensions) == True:
                block_words = []
                for paragraph in block.paragraphs:
                    block_words.extend(paragraph.words)

                block_symbols = []
                for word in block_words:
                    block_symbols.extend(word.symbols)

                block_text = ''
                for symbol in block_symbols:
                    block_text = block_text + symbol.text
                    if symbol.property.detected_break.type == 1 or symbol.property.detected_break.type == 3 or symbol.property.detected_break.type == 5:
                        block_text = block_text + ' '



                #set chapter2 case object date
                if not chapter2_case.email:
                    chapter2_case.set_email(block_text)

                #set chapter2 case object date
                if not chapter2_case.date:
                    chapter2_case.set_date(block_text)

                #set chapter2 case object date
                if not chapter2_case.name:
                    chapter2_case.set_names(block_text)

            elif detect_sender_quadrant(block, dimensions) == True:
                block_words = []
                for paragraph in block.paragraphs:
                    block_words.extend(paragraph.words)

                block_symbols = []
                for word in block_words:
                    block_symbols.extend(word.symbols)

                block_text = ''
                for symbol in block_symbols:
                    block_text = block_text + symbol.text
                    if symbol.property.detected_break.type == 1 or symbol.property.detected_break.type == 3 or symbol.property.detected_break.type == 5:
                        block_text = block_text + ' '

                if not chapter2_case.to:
                    print(block_text)
                    chapter2_case.set_to(block_text)



        return chapter2_case


if __name__ == '__main__':

    #connect to NER server - https://github.com/caihaoyu/sner/
    #java -Djava.ext.dirs=./lib -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -port 9199 -loadClassifier english.all.3class.distsim.crf.ser.gz


    #get list of images in google storage bucket
    letters = list_images('chapterimages')


    for letter in letters:
        print("Letter: {}".format(letter))
        chapter_case = create_chapter2_case('gs://chapterimages/{}'.format(letter))
        print(colored("Email: {}".format(chapter_case.email), 'green'))
        print(colored("Name: {}".format(chapter_case.name), 'red'))
        print(colored("Post: {}".format(chapter_case.post), 'magenta'))

        print(colored("Date: {}".format(chapter_case.date), 'blue'))
        print(colored("Department: {}".format(chapter_case.logo), 'yellow'))
        print("\n")

def get_case(image_title):

    chapter_case = create_chapter2_case('gs://chapterimages/{}'.format(image_title))
    return chapter_case
