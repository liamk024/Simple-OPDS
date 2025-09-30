from feedgen.feed import FeedGenerator
from flask import Flask, Response
from datetime import datetime, timezone

fg = FeedGenerator()
fg.id('root')
fg.title('Simple-OPDS')
fg.author({'name':'Liam Kelly'})
fg.link(rel='self', type='application/atom+xml;profile=opds-catalog;kind=navigation', link='')

now = datetime.now(timezone.utc)
fg.updated(now)

app = Flask(__name__)

@app.route('/')
def returnRoot():
    xml_out = fg.atom_str(pretty=True)
    return Response(xml_out, mimetype='application/atom+xml')

