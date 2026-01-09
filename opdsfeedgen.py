import uuid
from tomllib import load
from pathlib import Path
from datetime import datetime, timezone

config = load(open('opds.toml', 'rb'))
library_root = './actual_content'

class OPDSCatalog():
    # Declare lookup table for files and folders
    # def __init__(self):
    #     self.lookup_table = {'files': {}, 'folders': {}}
    #     self.crawl(library_root)
    
    # Rebuilds lookup table from library root
    def crawl(self, path):
        for item in path.iterdir():
            if item.is_dir():
                # Checks if a folder contains any actual files
                has_files = any(child.is_file() for child in item.iterdir())
                if has_files:
                    # Generate series ID if it contains files and register in lookup table
                    series_id = self.get_book_id(item.name, item.stat().st_mtime)
                    series_properties = {
                        'name': item.name,
                        'modified': item.stat().st_mtime,
                        'path': str(item)
                    }

                    # Register in lookup table
                    self.lookup_table[series_id] = series_properties
                else:
                    # Iterate on child folders
                    self.crawl(item)

    # Generate atom:link element and return as string
    def link(self, rel, link_type, href):
        return f'<link rel="{rel}" type="{link_type}" href="{href}"/>'
    
    # Generate URN UUID for series to use in URL and as ID
    def get_book_id(self, name, timestamp):
        u = uuid.uuid5(uuid.NAMESPACE_DNS, f'{name}:{timestamp}')
        return u.urn
    
    # Returns entries for 
    def get_children(self, path, href):
        output = []
        timestamp = datetime.now(timezone.utc)

        # Returns list of folder and files in path
        folders = [p for p in Path(path).iterdir() if p.is_dir()]
        files = [p for p in Path(path).iterdir() if p.is_file()]
        files.sort(key=lambda p: p.name)

        for f in folders:
            folder_name = f.name
            
            # Set folder_id based on whether or not it contains files
            has_files = any(child.is_file() for child in f.iterdir())
            if has_files:
                folder_id = self.get_book_id(f.name, f.stat().st_mtime)
            else:
                folder_id = f.name.lower().replace(' ', '+')

            # Generate entry for each folder in the 
            output.append('<entry>')
            output.append(f'<updated>{timestamp.strftime("%Y-%m-%dT%H:%M:%S")}</updated>')
            output.append(f'<id>{folder_id}</id>')
            output.append(f'<title>{folder_name}</title>')
            output.append(f'<content type="text">Browse {folder_name}</content>')

            # Get new href for child
            if has_files:
                child_href = '/series/' + folder_id
            else:
                child_href = href.rstrip('/') + '/' + folder_id
            output.append(self.link('subsection', 'application/atom+xml;profile=opds-catalog;kind=navigation', child_href))
            output.append('</entry>')
        
        for f in files:
            pass

        return output
    
    # Parses URL to actual file path
    def resolve_path_from_url(self, href):
        # Remove leading /content/ if present
        url_path = href.strip('/').split('/')
        if url_path[0] == 'content':
            url_path = url_path[1:]

        current_path = Path(library_root)

        for slug in url_path:
            # Build a lookup table for current folder
            folder_lookup_table = {
                p.name.lower().replace(' ', '+'): p.name
                for p in current_path.iterdir()
                if p.is_dir()
            }

            if slug not in folder_lookup_table:
                raise FileNotFoundError(f"No folder matches slug '{slug}' in '{current_path}'")

            # Move into next folder
            current_path = current_path / folder_lookup_table[slug]

        return current_path
    
    # Searches lookup table for series ID
    def resolve_path_from_id(self, series_id):
        pass

    # Return Navigation page for requested path
    def get_nav_page(self, href):
        output = []
        timestamp = datetime.now(timezone.utc)

        # Resolve actual file path
        path = self.resolve_path_from_url(href)

        # Document metadata
        output.append('<?xml version="1.0" encoding="UTF-8"?>')
        output.append('<feed xmlns="http://www.w3.org/2005/Atom">')
        
        output.append(f'<updated>{timestamp.strftime("%Y-%m-%dT%H:%M:%S")}</updated>')
        output.append(f'<id>{href}</id>')

        # Parse URL to get folder name
        if href.rstrip('/') == '/content':
            page_name = 'Root'
        else:
            page_name = str(path).split('/')[-1]
        output.append(f'<title>{page_name}</title>')

        # Add links for self and root path
        output.append(self.link('self', 'application/atom+xml;profile=opds-catalog;kind=navigation', href))
        output.append(self.link('start', 'application/atom+xml;profile=opds-catalog;kind=navigation', '/content'))

        # Add children for current path
        output.extend(self.get_children(path, href))

        output.append('</feed>')

        return '\n'.join(output)

    # Handle series pages differently to navigation pages
    def get_series_page(self, href):
        output = []
        timestamp = datetime.now(timezone.utc)

        # Get properties from series ID
        series_properties = self.lookup_table[href.split('/')[-1]]

        # Document metadata
        output.append('<?xml version="1.0" encoding="UTF-8"?>')
        output.append('<feed xmlns="http://www.w3.org/2005/Atom">')
        
        output.append(f'<updated>{timestamp.strftime("%Y-%m-%dT%H:%M:%S")}</updated>')
        output.append(f'<id>{href.split('/')[-1].split(':')[-1]}</id>')

        output.append(f'<title>{series_properties['name']}</title>')

        # Add links for self and root path
        output.append(self.link('self', 'application/atom+xml;profile=opds-catalog;kind=navigation', href))
        output.append(self.link('start', 'application/atom+xml;profile=opds-catalog;kind=navigation', '/content'))

        # Add children for current path
        output.extend(self.get_children(path, href))

        output.append('</feed>')

        return '\n'.join(output)