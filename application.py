from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue
from google.cloud import storage
import ocr
import SGDpredict
import allocator
import urllib.request
import getpq
from oauth2client import service_account



def list_images(bucket_name):
    """Lists all the images in the bucket."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)

        blobs = bucket.list_blobs()
        image_list = []
        for blob in blobs:
            image_list.append(blob.name)
        return image_list
    except:
        pass




#Load SGDmodel
sgdmodel = SGDpredict.SGDModel()
sgdmodel.load('model/sk_SGD_model.pickle')
print('SGD loaded')

#load NeuralNet
neuralnet = allocator.NeuralNet('model/model.tflearn', 'model/words.pickle', 'model/categories.pickle')
neuralnet.load_model()
print('neuralnet loaded')

app = Flask(__name__)
JSGlue(app)

#get list of images from bucket
image_list = list_images('chapterimages')


if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/draft")
def draft():

    return render_template('draft.html')


@app.route("/parliamentaryquestions")
def parliamentaryquestions():

    return render_template('parliamentaryquestions.html')

@app.route("/getunit")
def getunit():
    if request.args.get("question"):
        question = request.args.get("question")
        prediction1 = sgdmodel.predict(question)
        prediction2 = neuralnet.predict(question)
        return(jsonify(unit1 = prediction1, unit2 = prediction2))

@app.route("/getpqs")
def getpqs():
    return(jsonify(getpq.get_pqs()))



@app.route("/getcase")
def getcase():
    if request.args.get("number"):
        image_number = int(request.args.get("number"))
        case_details = ocr.get_case(image_list[image_number])
        print(case_details.email)
        print(case_details.date)
        print(case_details.name)
        return jsonify(image_name = image_list[image_number],
        name = case_details.name, email = case_details.email,
        date = case_details.date, post = case_details.post,
        id = case_details.id, to = case_details.to)
    else:
        print('Error, no image index')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
