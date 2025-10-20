from flask import Flask, Response
from tomllib import load
import opdsfeedgen, datetime, os

config = load(open('opds.toml', 'rb'))
opds_catalog = opdsfeedgen.OPDSCatalog()

# Crawls through content folder specified in opds.toml and adds to opds
for (root, dirs, files) in os.walk(config['content_path']):
    for dir in dirs:
        curr_path = '/'
        if config['content_path'] != root:
            curr_path = str(root).replace(config['content_path'], '')
        print(curr_path)
        #opds_catalog.add_nav_entry(dir, datetime.datetime.now(datetime.timezone.utc).strftime('%d:%m:%YT%H:%M:%S'), root)

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
