from flask import Flask, Response, request, flash, redirect, make_response, render_template
from flask import Flask, Response, request, flash, redirect, send_from_directory, make_response
from flask_cors import cross_origin
import ssl
import cv2 as cv

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')


@app.route('/')
def basic_pages(**kwargs):
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.route('/getData', methods=["GET"])
@cross_origin()
def getData():
    with open('picture_mixer/servieces/data.json', 'r') as f:
        content = f.read()
    return Response(content, status=200, mimetype="application/json")


@app.route('/renderImage', methods=["POST"])
@cross_origin()
def renderImage():
    firstImage = request.values.get('firstImage')
    secondImage = request.values.get('secondImage')

    if firstImage is None:
        flash('No file part')
        return Response("Key 'firstImage' not found in request!", status=400)

    if secondImage is None:
        flash('No file part')
        return Response("Key 'secondImage' not found in request!", status=400)

    mixed_file = AppFunctions.prepareImagesToMix(firstImage, secondImage)
    _, buffer = cv.imencode('.jpg', mixed_file)
    response = make_response(buffer.tobytes())
    return response


app.run(port=8080, debug=False)
