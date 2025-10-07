from flask import Flask, Response
import opdsfeedgen, uuid

main_id = uuid.uuid4()
feeds = {main_id:opdsfeedgen.OPDSFeed(main_id.urn, 'Main Library', False)}

root_feed = opdsfeedgen.OPDSFeed(uuid.uuid4().urn, 'OPDS Catalogue Root')
root_feed.add_nav_entry(main_id.urn, 'Main Library')

app = Flask(__name__)

# Serve root directory for OPDS
@app.route('/')
def root():
    out = str(root_feed)

    return Response(out, mimetype='application/atom+xml')

# Handle subdomain mapping to correct OPDS feed
@app.route('/<path:feed>')
def show_feed(feed):
    out = str(feeds[feed])
    return Response(out, mimetype='application/atom+xml')
