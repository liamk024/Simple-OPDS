from flask import Flask, Response
import atomgen

app = Flask(__name__)

@app.route('/')
def root():
    feed = str(atomgen.OPDSFeed())

    return Response(feed, mimetype='application/atom+xml')