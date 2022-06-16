from flask import Flask, Response, request, flash, redirect, make_response, render_template
from flask import Flask, Response, request, flash, redirect, send_from_directory, make_response
from flask_cors import cross_origin

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


app.run(port=8080, debug=False)
