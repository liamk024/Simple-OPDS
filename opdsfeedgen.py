import datetime

# Generate xml link element and return as string
def get_link(rel, href, link_type, other=''):
    out = []
    out.append('<link')
    out.append(f'rel="{rel}"')
    out.append(f'href="{rel}"')
    
    if link_type == 'navigation':
        out.append('type="application/atom+xml;profile=opds-catalog;kind=navigation"')
    elif link_type == 'acquisition':
        out.append('type="application/atom+xml;profile=opds-catalog;kind=acquisition"')
    else:
        if other != '':
            out.append(f'type="{other}"')

    out.append('/>')

    return ' '.join(out)

# Main class for OPDSFeed
class OPDSFeed():
    def __init__(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        self.root = {
            'id' : 'root',
            'title' : 'OPDS Catalogue Root',
            'updated' : now.strftime('%d:%m:%YT%H:%M:%S')
        }

        self.entries = []
    
    # def add_entry(self, )

    def __str__(self):
        output = []

        output.append('<?xml version="1.0" encoding="UTF-8"?>')
        output.append('<feed xmlns="http://www.w3.org/2005/Atom">')
        
        for property in self.root:
            output.append(f'<{property}>{self.root[property]}</{property}>')
        pass
        
        output.append(get_link('self', '/', 'navigation'))
        output.append(get_link('start', '/', 'navigation'))

        for entry in self.entries:
            output.append(entry)
        
        output.append('</feed>')

        return '\n'.join(output)
