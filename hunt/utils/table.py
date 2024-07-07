from rich.console import Console
from rich.table import Table


class HuntTable():
    table = None
    headers = None
    console = Console()

    def __init__(self, title):
        self.table = Table(title=title, show_header=True,
                           header_style='bold dark_orange3')
        for prop in self.headers:
            style = prop['attributes']['style'] if len(
                prop['attributes']) else ''
            self.table.add_column(prop['column'], style=style)

    def add_row(self, row_data):
        if type(row_data) == list:
            for row in row_data:
                self.add_row(row)
            return
        self.table.add_row(*list(row_data.values()))
    
    def print(self):
        self.console.print(self.table)


class RecentDomainCategorizationTable(HuntTable):
    headers = [{
        'column': 'domain',
        'attributes': {},
    }, {
        'column': 'source',
        'attributes': {},
    }, {
        'column': 'category',
        'attributes': {},
    }, {
        'column': 'last checked',
        'attributes': {
            'style': 'dim',
        }
    }]

    def __init__(self, title):
        super(RecentDomainCategorizationTable, self).__init__(title)


class SingleDomainCategorizationTable(HuntTable):
    headers = [{
        'column': 'source',
        'attributes': {},
    }, {
        'column': 'category',
        'attributes': {},
    }, {
        'column': 'checked at',
        'attributes': {
            'style': 'dim',
        },
    }]

    def __init__(self, title):
        super(SingleDomainCategorizationTable, self).__init__(title)


class TagDomainCategorizationTable(HuntTable):
    headers = [{
        'column': 'domain',
        'attributes': {},
    }, {
        'column': 'registrar',
        'attributes': {},
    }, {
        'column': 'status',
        'attributes': {
            'style': 'dim',
        },
    }]

    def __init__(self, title):
        super(TagDomainCategorizationTable, self).__init__(title)


class DomainTable(HuntTable):
    headers = [{
        'column': 'domain',
        'attributes': {},
    }, {
        'column': 'registrar',
        'attributes': {},
    }, {
        'column': 'tag',
        'attributes': {},
    }, {
        'column': 'status',
        'attributes': {
            'style': 'dim',
        },
    }]

    def __init__(self, title):
        super(DomainTable, self).__init__(title)
