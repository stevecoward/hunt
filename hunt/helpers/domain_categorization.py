import asyncio
from datetime import datetime
from hunt.helpers.csv import Csv
from hunt.helpers.domain import DomainHelper
from hunt.models.domain_categorization import DomainCategorization
from hunt.models.domain import Domain
from hunt.utils.table import SingleDomainCategorizationTable

class DomainCategorizationHelper:
    @staticmethod
    def get_all(source=None):
        domains = DomainHelper.get_all()
        results = []
        for domain_record in domains:
            categorization_records = DomainCategorizationHelper.get_by_domain(domain_record['domain'], source=source)
            for record in categorization_records:
                record.update({
                    'domain': domain_record['domain']
                })
            results.extend(categorization_records)

        return results


    @staticmethod
    def get_by_domain(domain, source=None, table=False):
        results = []

        if not source:
            records = DomainCategorization.select()\
                .join(Domain)\
                .where(Domain.domain == domain)\
                .order_by(DomainCategorization.checked_at)
        else:
            records = DomainCategorization.select()\
                .join(Domain)\
                .where(Domain.domain == domain)\
                .where(DomainCategorization.source == source)\
                .order_by(DomainCategorization.checked_at)

        for record in records:
            results.append({
                "source": record.source,
                "category": record.category,
                "checked_at": record.checked_at.strftime("%Y-%m-%d %H:%M:%S"),
            })

        if table:
            table = SingleDomainCategorizationTable(f'\nCategorizations for: {domain}')
            table.add_row(results)
            table.print()

        return results


    @staticmethod
    def check_add_categorization_record(domain, source, category):
        try:
            domain_record = Domain.get(Domain.domain == domain)
        except Exception as e:
            domain_record = DomainHelper.check_add_domain_record(domain)

        cat_record = DomainCategorization(
            domain_id=domain_record.id, source=source, category=category, checked_at=datetime.now())
        cat_record.save()


    @staticmethod
    def refresh():
        from hunt.helpers.lookup import LookupHelper

        records = Domain.select(Domain.domain)
        for record in records:
            asyncio.run(LookupHelper.lookup(record.domain, True))


    @staticmethod
    def export(domain, source=None):
        if domain.lower() == 'all':
            results = DomainCategorizationHelper.get_all(source=source)
        else:
            results = DomainCategorizationHelper.get_by_domain(domain, source=source)

        Csv.write_to_file(results, f'hunt-export-{domain.replace(".", "_").replace("-", "_")}.csv')
