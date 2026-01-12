# Simple OPDS: Lightweight implementation of the OPDS spec in python
# Copyright (C) 2026  Liam Kelly
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Dependencies on inbuilt python modules
import datetime, os, uuid, logging

# Module for reading from .env files
import dotenv

# OPDS feed constructor
import opds

# Modules for creating and hosting the webapp
from flask import Flask, Response, send_file, request
from waitress import serve

# =====================================
# Main application file for Simple OPDS
# =====================================

# Load environment variables from .env
dotenv.load_dotenv()
library_path = os.getenv('LIBRARY_PATH', './content')
port = os.getenv('PORT', 5000)

# Create OPDSCatalog object from local content directory
opds_catalog = opds.OPDSCatalog(library_path)

# Create flask application object
app = Flask(__name__)

# =====================================
# Handle connections to server endpoint
# =====================================

# Output incoming connections to stdout
@app.before_request
def log_only_get():
    if request.method == "GET":
        app.logger.info('GET %s', request.path)

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

# =======================
# Launching the webserver
# =======================

if __name__ == "__main__":
    # logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

    # Launch the Flask app via Waitress
    serve(
        app,
        host="0.0.0.0",
        port=port,
        threads=4
    )