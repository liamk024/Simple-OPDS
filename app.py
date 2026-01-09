from flask import Flask, Response, send_file
from tomllib import load
import opdsfeedgen, datetime, os, uuid

# Loads config file and creates OPDSCatalog object
config = load(open('opds.toml', 'rb'))
opds_catalog = opdsfeedgen.OPDSCatalog()

app = Flask(__name__)

# Route for root directory
@app.route('/', strict_slashes=False)
def show_root():
    out = opds_catalog.get_nav_page('/content')
    return Response(out, mimetype='application/atom+xml')

# Single route for /content and any nested subfolders
@app.route('/content/<path:path>', strict_slashes=False)
def show_content(path):
    # Handles trailing slashes
    path = path.rstrip('/')
    href = '/content'
    if path:
        href += '/' + path

    # Generate and serve page to user
    out = opds_catalog.get_nav_page(href)
    return Response(out, mimetype='application/atom+xml')

# Single route for series and individual files in said series
@app.route('/series', defaults={'path': ''}, strict_slashes=False)
@app.route('/series/<path:path>', strict_slashes=False)
def show_series(path):
    # Handles trailing shashes
    path = path.rstrip('/')
    href = '/series'
    if path:
        href += '/' + path

    # Check if user is requesting series page or actual file
    path = path.split('/')

    # Checks if the URL ends in a uuid
    try:
        uuid_obj = uuid.UUID(path[-1])
        is_uuid = True
    except ValueError:
        is_uuid = False

    if is_uuid:
        # Generate and serve page to user
        out = opds_catalog.get_series_page(href)
        return Response(out, mimetype='application/atom+xml')
    else:
        # Parse series UUID from 
        series_id = path[-2]
        file_path = opds_catalog.lookup_table[series_id]['files'][int(path[-1])]
        return send_file(file_path, mimetype='application/epub+zip')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )