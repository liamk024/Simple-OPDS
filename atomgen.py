from datetime import datetime, timezone

class OPDSFeed():
    def __init__(self):
        self.root = {
            'id' : 'root',
            'title' : 'OPDS Catalogue Root',
            'updated' : datetime.now(timezone.utc)
        }

        self.entries = []
    
    # def add_entry(self, )

    def __str__(self):
        output = []

        output.append('<?xml version="1.0" encoding="UTF-8"?>')
        output.append('<feed xmlns="http://www.w3.org/2005/Atom">')
        
        for property in self.root:
            output.append(f'    <{property}>{self.root[property]}</{property}>')
        pass

        for entry in self.entries:
            output.append('        ' + entry)
        
        output.append('</feed>')

        return '\n'.join(output)