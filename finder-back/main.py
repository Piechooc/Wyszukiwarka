from flask import render_template
from flask import Flask, Response, redirect
from flask_cors import cross_origin

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')


@app.route('/')
def basic_pages(**kwargs):
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.route('/getLinks', methods=["GET"])
@cross_origin()
def getData():
    with open('finder-back/data.json', 'r') as f:
        content = f.read()
    return Response(content, status=200, mimetype="application/json")


app.run(port=8080, debug=False)
