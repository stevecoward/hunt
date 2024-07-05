from hunt.utils.table import RecentDomainCategorizationTable, TagDomainCategorizationTable
from hunt.models.domain import Domain
from hunt.models.domain_categorization import DomainCategorization

class DomainHelper:
    @staticmethod
    def get_recent(table=False):
        results = []
        records = Domain.select(Domain.domain, DomainCategorization.source, DomainCategorization.category, DomainCategorization.checked_at)\
            .join(DomainCategorization)\
            .where(DomainCategorization.category != "").order_by(Domain.id.desc()).limit(10)

        for record in records:
            results.append({
                "domain": record.domain,
                "source": record.domaincategorization.source,
                "category": record.domaincategorization.category,
                "checked_at": record.domaincategorization.checked_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        if table:
            table = RecentDomainCategorizationTable(f'\nRecent Categorizations')
            table.add_row(results)
            table.print()

        return results

    @staticmethod
    def get_by_tag(tag, table=False):
        results = []

        records = Domain(Domain.domain, Domain.registrar, Domain.status)\
            .select()\
            .where(Domain.tag == tag)\
            .order_by(Domain.status)

        for record in records:
            results.append({
                'domain': record.domain,
                'registrar': record.registrar,
                'status': record.status,
            })
        
        if table:
            table = TagDomainCategorizationTable(f'\nDomains having tag: {tag}')
            table.add_row(results)
            table.print()
        
        return results
    
    @staticmethod
    def check_add_domain_record(domain, registrar="", tag="", status="N/A"):
        try:
            domain_record = Domain.get(Domain.domain == domain)
        except Exception as e:
            domain_record = Domain(
                domain=domain, registrar=registrar, tag=tag, status=status)
            domain_record.save()        
