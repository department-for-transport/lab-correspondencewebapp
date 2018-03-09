

## Correspondence OCR and PQ Classification web app

## Download and Installation

The directory includes all application.py, the main web application, and a number of supporting functions (e.g ocr.py, name_check.py etc etc)

Within 'model' is all the required trained models, and a number of other required objects

Within stanford-ner is the stanford named entity recogniser, which needs to be run as a java servlet in my implementation. In the stanford-ner directory and run:

"java -Djava.ext.dirs=./lib -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -port 9199 -loadClassifier english.all.3class.distsim.crf.ser.gz"

This will load an instance of the named entity tagger, which the application makes calls to. You need java isntalled.

Alternatively you can load the tagger in your code, but it's slower!

###  Optical Character Recognition

We use google cloud storage to host our correspondence images, and the google vision API to read them, so you'll need to set up your own google cloud project to use these services.

To access those services you the easiest way is to store the Service Account Credentials that google provide as a .json in the workding directory, and put that location on your path, e.g.

export GOOGLE_APPLICATION_CREDENTIALS='PATH/TO/SERVICEACCOUNT/CREDENTIALS.JSON'

### To run the app:

export FLASK_APP=application.py

also set: export FLASK_DEBUG=1

so the browswer doesnt cache the site

run the app by running:

flask run






## Copyright and License

Copyright 2018 Department for Transport
