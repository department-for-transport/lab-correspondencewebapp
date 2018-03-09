

# Correspondence OCR and PQ Classification web app

A flask web app that can extract names, addresses etc from correspondence and also sort parliamentary questions into responding units.

## Download and Installation

The repo contains pretty much everything you need

### /model

Within 'model' are all the required trained models, and a number of other required data structures that we pickled

### /stanford-ner


Within stanford-ner is the stanford named entity recogniser, which needs to be run as a java servlet in my implementation. In the stanford-ner directory and run:

"java -Djava.ext.dirs=./lib -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -port 9199 -loadClassifier english.all.3class.distsim.crf.ser.gz"

This will load an instance of the named entity tagger, which the application makes calls to. You need java installed.

Alternatively you can load the tagger in your code, but it's slower!

https://nlp.stanford.edu/software/CRF-NER.html

### /static

All the javascript and css for the front end (required by flask)

### /templates

The HTML for the front end

### application.py
Loads our models and does all the route handling

### allocator.py
Sorry, stupid name. Contains our NeuralNet class, which contains the neural net and has prediction methods

### SGDpredict.py
Another dumb name. Contains the SGDModel class, which containes the sgd classifier and has prediction methods

### getpq.py
Contains a get_pqs function which gets the most recent PQs from the parliament written question API 
http://explore.data.parliament.uk/?learnmore=Commons%20Written%20Questions

### helpers.py
bad name. This contains our Chapter2_Case class which holds all the data about the scanned correspondence image and the methods to extract that data. Think of it like a case file that you pass data to and it decides what to extract to build the case file.

### name_check.py
checks the extracted names against parliament's member API
http://www.data.parliament.uk/dataset/members-of-the-house-of-commons/resource/7523521e-e724-4824-927c-58c50ffd6c9e

### ocr.py
conducts the optical character recognition on the images of correspondence, sorts it into chunks of text, sifts it by position on the page, and passes it to a chapter2_case object to identify the relevant data. Kind of messy...more details on how to use it below

### sklearn_tools.py
I think this prepares input strings for prediction by the sgd classifier...but it's not very explicit. Maybe ask Will B...all i know is it needs to be in the directory.


## Optical Character Recognition (ocr.py)

We use google cloud storage to host our correspondence images, and the google vision API to read them, so you'll need to set up your own google cloud project to use these services.

To access those services you the easiest way is to store the Service Account Credentials that google provide as a .json in the workding directory, and put that location on your path, e.g.

export GOOGLE_APPLICATION_CREDENTIALS='PATH/TO/SERVICEACCOUNT/CREDENTIALS.JSON'

## To run the app:

export FLASK_APP=application.py

also set: export FLASK_DEBUG=1

so the browswer doesnt cache the site

run the app by running:

flask run


