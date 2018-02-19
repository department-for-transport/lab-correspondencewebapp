

## Correspondence OCR and PQ Classification web app

## Download and Installation

The directory includes all application.py, the main web application, and a number of supporting functions (e.g ocr.py, name_check.py etc etc)

Within 'model' is all the required trained models, and a number of other required objects

Within stanford-ner is the stanford named entity recogniser, which needs to be run as a java servlet. cd in the stanford-ner directory and run:

"java -Djava.ext.dirs=./lib -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -port 9199 -loadClassifier english.all.3class.distsim.crf.ser.gz"

This will load an instance of the named entity tagger, which the application makes calls to

(needs java)


###  Usage

You'll need to set the following variables in your enviro

export GOOGLE_APPLICATION_CREDENTIALS='PATHTOSERVICEACCOUNTCREDENTIALS(the api key).JSON'

This allows you to access my google cloud storage bucket, you could equally set up your own

export FLASK_APP=application.py

also set: export FLASK_DEBUG=1

so the browswer doesnt cache the site

run the app by running:

flask run






## Copyright and License

Copyright 2013-2018 Blackrock Digital LLC. Code released under the [MIT](https://github.com/BlackrockDigital/startbootstrap-portfolio-item/blob/gh-pages/LICENSE) license.
