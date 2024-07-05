import os
from peewee import SqliteDatabase


class HuntDb():
    db_name = 'hunt.db'

    def __init__(self):        
        if os.name == 'nt':
            self.data_dir = f'{os.getenv("LOCALAPPDATA")}\hunt'
        else:
            self.data_dir = f'{os.path.join(os.path.expanduser("~"), ".hunt")}'
        
        if not os.path.isdir(self.data_dir):
            os.mkdir(self.data_dir)
        
        self.db = SqliteDatabase(f'{os.path.join(self.data_dir, self.db_name)}')


    def setup(self):
        from hunt.models.domain import Domain
        from hunt.models.domain_categorization import DomainCategorization
        
        self.db.connect()
        self.db.create_tables([Domain, DomainCategorization])
        self.db.close()
