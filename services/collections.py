from . import  nice_json
from flask import Flask, request
from werkzeug.exceptions import NotFound
from database.collections import Collections

app = Flask(__name__)


@app.route("/")
def hello():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "add_collection": "/add",
            "collections": "/all",
            "collection": "/all/<username>",
            "delete": "/delete/<id>",
            "clean": "/clean"
        }
    })


@app.route("/add", methods=['POST'])
def add():
    form = request.form
    c = Collections.new(form)
    c = c.json()
    return nice_json(c)

@app.route('/all')
def all():
    cs = Collections.all()
    # rediscache
    cs = Collections.cache_all()
    cs = [i.json() for i in cs]
    return nice_json(cs)

@app.route("/all/<username>")
def find_by(username):
    c = Collections.find_by(username=username)
    c = c.json()
    return nice_json(c)

@app.route("/delete")
def delete():
    id = int(request.args.get('id'))
    Collections.delete(id)
    return 'delete success!'


@app.route("/clean")
def clean():
    Collections.clean()
    return "clean done!"

if __name__ == "__main__":
    app.run(port=5004, debug=True)
