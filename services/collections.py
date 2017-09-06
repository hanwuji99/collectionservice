import cPickle
from . import root_dir, nice_json
from flask import Flask, request, redirect, url_for, Response, jsonify
import json
from werkzeug.exceptions import NotFound
from database.collections import Collections

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "collections": "/collections",
            "collection": "/collections/<username>"
        }
    })


@app.route("/add", methods=['POST'])
def add():
    form = request.form
    c = Collections.new(form)
    return redirect('/')


@app.route("/delete")
def delete():
    id = int(request.args.get('id'))
    Collections.delete(id)
    return redirect('/')


@app.route('/all')
def all():
    # cs = Collections.all()
    cs = Collections.cache_all()
    # cs = Collections.all_delay()
    # ret = []
    # for c in cs:
    #     c.to_json()
    #     ret.append(c)
    # print  ret
    # cs = json.dumps(ret)
    cs = cPickle.dumps(cs)
    return nice_json(cs)


# @app.route("/collections", methods=['GET'])
# def collection_list():
#     return nice_json(collections)

#
# @app.route("/collections/<username>", methods=['GET'])
# def collection_record(username):
#     if username not in collections:
#         raise NotFound
#
#     return nice_json(collections[username])

if __name__ == "__main__":
    app.run(port=5004, debug=True)
