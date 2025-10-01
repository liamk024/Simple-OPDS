from flask import Flask, Response
import opdsfeedgen

feeds = {'main':opdsfeedgen.OPDSFeed('main', 'Main Library', 'acquisition', '/main', '/')}

root_feed = opdsfeedgen.OPDSFeed('root', 'OPDS Catalogue Root', 'navigation', '/', '/')
root_feed.add_nav_entry('main', 'Main Library', '/main')

app = Flask(__name__)

@app.route('/')
def root():
    out = str(root_feed)

    return Response(out, mimetype='application/atom+xml')

@app.route('/<feed>')
def show_feed(feed):
    out = str(feeds[feed])
    return Response(out, mimetype='application/atom+xml')