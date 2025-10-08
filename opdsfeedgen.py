import datetime, uuid
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

# Main OPDS catalog class
class OPDSCatalog():
    def __init__(self):
        # Apply config
        self.base_path = config['base_path']
        self.title = config['title']
        self.updated = datetime.datetime.now(datetime.timezone.utc).strftime('%d:%m:%YT%H:%M:%S') # TODO: Change to use timestamp for last time files were changed

        # Generates the atom:link elements at the top of the feed
        self.links = []

        self.links.append(get_link('self', self.base_path, 'application/atom+xml;profile=opds-catalog;kind=navigation'))
        self.links.append(get_link('start', self.base_path, 'application/atom+xml;profile=opds-catalog;kind=navigation'))

        # Setup dictionary to store navigation and acquisition feeds and declare root
        self.contents = {'navigation' : [{'title' : self.title, 'id' : 'root', 'updated': self.updated, 'entries' : []}], 'acquisition' : []}
    
    # For adding OPDS navigation feeds and entries to those feeds
    def add_nav_entry(self, entry_title, entry_timestamp, parent_path='/'):
        entry_id = ''.join([c for c in entry_title.lower() if ord(c) >= 97 and ord(c) <= 122])
        entry_path = parent_path + entry_id
        self.contents['navigation'][parent_path]['entries'].append(entry_path)
        self.contents['navigation'][entry_path] = {'title' : entry_title, 'id' : entry_id, 'updated': entry_timestamp, 'entries' : []}

    # For adding OPDS acquisition feeds
    def add_acquisition_entry(self, entry_title, entry_timestamp, parent_path='/'):
        unique_id = uuid.uuid4() # TODO: Make UUID generate based off of combination of file timestamp and name
        entry_id = unique_id.urn
        entry_path = parent_path + str(unique_id)
        self.contents['navigation'][parent_path]['entries'].append(entry_path)
        self.contents['acquisition'][entry_path] = {'title' : entry_title, 'id' : entry_id, 'updated': entry_timestamp, 'entries' : []}

    # Returns a complete atom document for the requested path
    def return_page(self, path):
        output = []

        output.append('<?xml version="1.0" encoding="UTF-8"?>')
        output.append('<feed xmlns="http://www.w3.org/2005/Atom">')

        page_definition = None
        # Handle for root page request        
        if path == '/':         
            page_definition = self.contents['navigation']['/']

        # Handle for page other than root
        else:
            if path in self.contents['navigation']:
                page_definition = self.contents['navigation'][path]
            elif path in self.contents['acquisition']:
                page_definition = self.contents['acquisition'][path]
            else:
                return None

        output.append(f'<id>{page_definition["id"]}</id>')
        output.append(f'<title>{page_definition["title"]}</title>')
        output.append(f'<updated>{page_definition["updated"]}</updated>')
        
        # TODO: Everything below this needs to be rewritten
        for link in self.links:
            output.append(link)

        for entry in page_definition['entries'].keys(): 
            entry_definition = None
            if entry in self.contents['navigation']:
                entry_definition = self.contents['navigation'][entry]
            elif path in self.contents['acquisition']:
                entry_definition = self.contents['acquisition'][path]
            else:
                return None

            output.append('<entry>')
            for line in entry:
                output.append('    ' + line)
            output.append('</entry>')

        output.append('</feed>')

        return '\n'.join(output)
        # out = []

        # out.append('    ' + f'<id>{entry_id}</id>')
        # out.append('    ' + f'<title>{entry_title}</title>')
        # out.append('    ' + f'<updated>{self.properties["updated"]}</updated>')
        # out.append('    ' + get_link('subsection', f'/{entry_id}', 'application/atom+xml;profile=opds-catalog;kind=navigation'))

        # self.entries.append(out)
