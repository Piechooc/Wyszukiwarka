from flask import render_template, request
from flask import Flask, Response, redirect
from flask_cors import cross_origin, CORS
from SearchEngine import SearchEngine

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='template')
CORS(app)

# search_engine = SearchEngine(10000, "10k", idf=False)
# search_engine_IDF = SearchEngine(10000, "10k_IDF")
# search_engine_LRA = SearchEngine(10000, "10k_LRA", idf=False, low_rank=True, k=1000)
# search_engine_IDF_LRA = SearchEngine(10000, "10k_LRA", low_rank=True, k=1000)


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

        # if json["approx"]:
        #     if json["idf"]:
        #         search_engine_IDF_LRA.search(json["value"])
        #     else:
        #         search_engine_LRA.search(json["value"])
        # else:
        #     if json["idf"]:
        #         search_engine_IDF.search(json["value"])
        #     else:
        #         search_engine.search(json["value"])

    with open('data.json', 'r') as f:
        content = f.read()
    return Response(content, status=200, mimetype="application/json")


app.run(port=8080, debug=False)
