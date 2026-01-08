import uuid
from tomllib import load
from pathlib import Path
from datetime import datetime, timezone

config = load(open('opds.toml', 'rb'))
library_root = './content'

class OPDSCatalog():
    # Generate atom:link element and return as string
    def link(self, rel, href, link_type):
        return f'<link rel="{rel}" href="{href}" type="{link_type}"/>'
    
    # Generate URN UUID from book files to use in URL and as ID
    def get_book_id(self, name, timestamp):
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        else:
            timestamp = timestamp.astimezone(timezone.utc)

        unix_time = int(timestamp.timestamp())

        u = uuid.uuid5(uuid.NAMESPACE_DNS, f'{name}:{unix_time}')
        return u.urn
    
    # Returns entries for 
    def get_children(self, path, is_acquisition=False):
        output = []

        # Returns list of folder names in path
        folders = [p for p in Path(library_root + path).iterdir() if p.is_dir()]
        for f in folders:
            # Checks if folder contains any files and if so, registers it as an acquisition feed
            has_files = any(child.is_file() for child in f.iterdir())
            timestamp = datetime.now(timezone.utc)

            output.append('<entry>')
            output.append(f'<updated>{timestamp.strftime("%Y-%m-%dT%H:%M:%S")}</updated>')

            folder_name = f.name
            
            # Add link as an acquisition or navigation feed depending on it's children
            if has_files:
                folder_id = get_book_id()
                output.append(self.link('subsection', 'application/atom+xml;profile=opds-catalog;kind=acquisition', path + folder_id))
            else:
                folder_id = path_name.replace(' ', '+')
                output.append(self.link('subsection', 'application/atom+xml;profile=opds-catalog;kind=navigation', path + folder_id))

            output.append(f'<id>{folder_id}</id>')
            output.append(f'<title>{folder_name}</title>')
            output.append(f'<content type="text">Browse {folder_name}</content>')




            output.append('</entry>')
        
        return output

    # Return Atom xml feed for requested path
    def get_page(self, path):
        full_path = path.split('/')
        full_path.pop(0)

        # Checks if path ends in a URN UUID
        if full_path[-1].startswith('urn:uuid:'):
            path_type = 'application/atom+xml;profile=opds-catalog;kind=acquisition'
        else:
            path_type = 'application/atom+xml;profile=opds-catalog;kind=navigation'

        output = []
        output.append('<?xml version="1.0" encoding="UTF-8"?>')
        output.append('<feed xmlns="http://www.w3.org/2005/Atom">')

        output.append(f'<id>{path}</id>')

        # Add links for self and root path
        if self.path_type == 'acquisition':
            output.append(link('self', path, 'application/atom+xml;profile=opds-catalog;kind=acquisition'))
        else:
            output.append(link('self', path, 'application/atom+xml;profile=opds-catalog;kind=navigation'))
        output.append(link('start', '/', 'application/atom+xml;profile=opds-catalog;kind=navigation'))



        output.append('</feed>')

        

# Main OPDS catalog class
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
    self.contents = {'navigation' : {'/' : {'title' : self.title, 'id' : 'root', 'updated': self.updated, 'entries' : []}}, 'acquisition' : []}

# For adding OPDS navigation feeds and entries to those feeds
def add_nav_entry(self, entry_title, entry_timestamp, parent_path='/'):
    entry_id = ''.join([c for c in entry_title.lower() if c.isalnum()])
    entry_path = parent_path.rstrip('/') + '/' + entry_id
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

    output.append('    ' + f'<id>{page_definition["id"]}</id>')
    output.append('    ' + f'<title>{page_definition["title"]}</title>')
    output.append('    ' + f'<updated>{page_definition["updated"]}</updated>')
    
    # TODO: Everything below this needs to be rewritten
    for link in self.links:
        output.append('    ' + link)

    for entry in page_definition['entries']: 
        entry_definition = None
        if entry in self.contents['navigation']:
            entry_definition = self.contents['navigation'][entry]
        elif path in self.contents['acquisition']:
            entry_definition = self.contents['acquisition'][path]
        else:
            return None

        output.append('    ' + '<entry>')
        if 'link' in entry_definition.keys():
            output.append('        ' + get_link('http://opds-spec.org/acquisition', entry, 'application/epub+zip')) # TODO: rewrite to actually serve file and also to not assume file is epub
        else:
            output.append('        ' + get_link('subsection', entry, 'application/atom+xml;profile=opds-catalog;kind=navigation'))
            print(path)
        for line in entry_definition.keys():
            if not line == 'link' and not line == 'entries':
                output.append('        ' + f'<{line}>{entry_definition[line]}</{line}>')

        output.append('    ' + '</entry>')

    output.append('</feed>')

    return '\n'.join(output)
    # out = []

    # out.append('    ' + f'<id>{entry_id}</id>')
    # out.append('    ' + f'<title>{entry_title}</title>')
    # out.append('    ' + f'<updated>{self.properties["updated"]}</updated>')
    # out.append('    ' + get_link('subsection', f'/{entry_id}', 'application/atom+xml;profile=opds-catalog;kind=navigation'))

    # self.entries.append(out)
