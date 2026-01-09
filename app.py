from flask import Flask, Response
from tomllib import load
import opdsfeedgen, datetime, os

# Loads config file and creates OPDSCatalog object
config = load(open('opds.toml', 'rb'))
opds_catalog = opdsfeedgen.OPDSCatalog()

app = Flask(__name__)

# Single route for /content and any nested subfolders
@app.route('/content', defaults={'path': ''}, strict_slashes=False)
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
    if path[-1].startswith('urn:uuid'):
        # Generate and serve page to user
        out = opds_catalog.get_series_page(href)
        return Response(out, mimetype='application/atom+xml')
    else:
        # Parse series UUID from 
        series_id = path[-2].split(':')[-1]
        file_path = opds_catalog.resolve_path_from_id(series_id)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )