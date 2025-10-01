import datetime

# Generate atom:link element and return as string
def get_link(rel, href, link_type):
    out = []

    out.append('<link')
    out.append(f'rel="{rel}"')
    out.append(f'href="{href}"')
    out.append(f'type="{link_type}"')

    out.append('/>')

    return ' '.join(out)

# Main atom feed class, to use as a parent for opds classes
class OPDSFeed():
    # Initialise basic data for OPDS Feeds
    def __init__(self, feed_id, feed_title, feed_type, path, root_path):
        now = datetime.datetime.now(datetime.timezone.utc)
        self.properties = {
            'id' : feed_id,
            'title' : feed_title,
            'updated' : now.strftime('%d:%m:%YT%H:%M:%S')
        }
        
        if not (feed_type == 'navigation' or feed_type == 'acquisition'):
            ValueError("Invalid feed_type")

        self.links = [
            get_link('self', path, f'application/atom+xml;profile=opds-catalog;kind={feed_type}'), 
            get_link('start', root_path, 'application/atom+xml;profile=opds-catalog;kind=navigation')
        ]

        self.entries = []
    
    # For adding OPDS Entries
    def add_nav_entry(self, entry_id, entry_title, entry_href):
        out = []

        out.append('<entry>')
        out.append('    ' + f'<id>{entry_id}</id>')
        out.append('    ' + f'<title>{entry_title}</title>')
        out.append('    ' + f'<updated>{self.properties["updated"]}</updated>')
        out.append('    ' + get_link('subsection', entry_href, 'application/atom+xml;profile=opds-catalog;kind=navigation'))
        out.append('</entry>')

        self.entries.append('\n'.join(out))


    def __str__(self):
        output = []

        output.append('<?xml version="1.0" encoding="UTF-8"?>')
        output.append('<feed xmlns="http://www.w3.org/2005/Atom">')
        
        for property in self.properties:
            output.append(f'    <{property}>{self.properties[property]}</{property}>')
        pass
        
        # output.append(get_link('self', '/', 'navigation'))
        # output.append(get_link('start', '/', 'navigation'))

        for link in self.links:
            output.append('    ' + link)

        for entry in self.entries:
            output.append('    ' + entry)
        
        output.append('</feed>')

        return '\n'.join(output)