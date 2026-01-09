from flask import Flask, Response
from tomllib import load
import opdsfeedgen, datetime, os

config = load(open('opds.toml', 'rb'))
opds_catalog = opdsfeedgen.OPDSCatalog()

# # Crawls through content folder specified in opds.toml and adds to opds
# for (root, dirs, files) in os.walk(config['content_path']):
#     for dir in dirs:
#         curr_path = '/'
#         if config['content_path'] != root:
#             curr_path = str(root).replace(config['content_path'], '')
#         print(curr_path)
#         #opds_catalog.add_nav_entry(dir, datetime.datetime.now(datetime.timezone.utc).strftime('%d:%m:%YT%H:%M:%S'), root)

# opds_catalog.add_nav_entry('Main library', datetime.datetime.now(datetime.timezone.utc).strftime('%d:%m:%YT%H:%M:%S'))
# opds_catalog.add_nav_entry('Secondary library', datetime.datetime.now(datetime.timezone.utc).strftime('%d:%m:%YT%H:%M:%S'), '/mainlibrary')

app = Flask(__name__)

# Single route for /content and any nested subfolders
@app.route('/content', defaults={'path': ''}, strict_slashes=False)
@app.route('/content/<path:path>', strict_slashes=False)
def show_content(path):
    path = path.rstrip('/')
    href = '/content'
    if path:
        href += '/' + path
    out = opds_catalog.get_nav_page(href)
    return Response(out, mimetype='application/atom+xml')
