from feedgen.feed import FeedGenerator
from flask import Flask

fg = FeedGenerator()
fg.id('root')
fg.title('Simple-OPDS')
fg.author({'name':'Liam Kelly'})

fe = fg.add_entry()
fe.id()

app = Flask(__name__)


