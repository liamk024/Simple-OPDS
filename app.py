from flask import Flask, Response
import opdsfeedgen, datetime

opds_catalog = opdsfeedgen.OPDSCatalog()
opds_catalog.add_nav_entry('Main library', datetime.datetime.now(datetime.timezone.utc).strftime('%d:%m:%YT%H:%M:%S'))
opds_catalog.add_nav_entry('Secondary library', datetime.datetime.now(datetime.timezone.utc).strftime('%d:%m:%YT%H:%M:%S'), '/mainlibrary')

app = Flask(__name__)

# Serve root directory for OPDS
@app.route('/')
def root():
    out = opds_catalog.return_page('/')

    return Response(out, mimetype='application/atom+xml')

# Handle subdomain mapping to correct OPDS feed
@app.route('/<path:feed>')
def show_feed(feed):
    out = opds_catalog.return_page('/' + feed)
    return Response(out, mimetype='application/atom+xml')
