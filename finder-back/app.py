from flask import render_template, request
from flask import Flask, Response, redirect
from flask_cors import cross_origin, CORS

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
CORS(app)


@app.route('/')
def basic_pages(**kwargs):
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.route('/getLinks', methods=["POST"])
@cross_origin()
def getData():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        print(json['value'])
    with open('data.json', 'r') as f:
        content = f.read()
    return Response(content, status=200, mimetype="application/json")


app.run(port=8080, debug=False)
