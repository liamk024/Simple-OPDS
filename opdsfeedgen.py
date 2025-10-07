import datetime, os, uuid
from tomllib import load

config = load(open('opds.toml', 'rb'))

# Generate atom:link element and return as string
def get_link(rel, href, link_type):
    link = '<link'
    link += f' rel="{rel}"'
    link += f' href="{href}"'
    link += f' type="{link_type}"'
    link += '/>'

    return link

# Main OPDS feed class
class OPDSFeed():
    def __init__(self):
        now = datetime.datetime.now(datetime.timezone.utc)

        # Apply config
        self.base_path = config['base_path']
        self.title = config['title']
        self.updated = now.strftime('%d:%m:%YT%H:%M:%S') # TODO: Change to use timestamp for last time files were changed

        # Generates the atom:link elements at the top of the feed
        self.links = []

        self.links.append(get_link('self', self.base_path, 'application/atom+xml;profile=opds-catalog;kind=navigation'))
        self.links.append(get_link('start', self.base_path, 'application/atom+xml;profile=opds-catalog;kind=navigation'))

        # Prepare dictionary for all feed entries
        self.contents = {}
    
    # For adding OPDS Entries
    def add_nav_entry(self, title, path, is_directory=True):
        # out = []

        # out.append('    ' + f'<id>{entry_id}</id>')
        # out.append('    ' + f'<title>{entry_title}</title>')
        # out.append('    ' + f'<updated>{self.properties["updated"]}</updated>')
        # out.append('    ' + get_link('subsection', f'/{entry_id}', 'application/atom+xml;profile=opds-catalog;kind=navigation'))

        # self.entries.append(out)

        if is_directory:
            entry_id = "".join([c for c in title.lower() if ord(c) >= 97 and ord(c) <= 122])
            self.contents[entry_id] = {'title' : title, }
        else:
            pass

    # 
    def return_page(self, page_id):
        pass

    # Properly return document as string to be sent over web
    def __str__(self):
        output = []

        output.append('<?xml version="1.0" encoding="UTF-8"?>')
        output.append('<feed xmlns="http://www.w3.org/2005/Atom">')
        
        for property in self.properties:
            output.append(f'    <{property}>{self.properties[property]}</{property}>')
        pass

        for link in self.links:
            output.append('    ' + link)

        for entry in self.entries:
            output.append('    ' + '<entry>')
            for line in entry:
                output.append('    ' + line)
            output.append('    ' + '</entry>')

        output.append('</feed>')

        return '\n'.join(output)
