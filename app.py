from flask import Flask, Response
import opdsfeedgen

app = Flask(__name__)

@app.route('/')
def root():
    feed = str(opdsfeedgen.OPDSFeed())

    return Response(feed, mimetype='application/atom+xml')
