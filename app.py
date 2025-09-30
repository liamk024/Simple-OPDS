from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def root():
    feed = ''

    return Response(feed, mimetype='application/atom+xml')