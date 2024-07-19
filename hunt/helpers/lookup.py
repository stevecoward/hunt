import asyncio
import logging
from hunt import config
from hunt.helpers.domain import DomainHelper
from hunt.helpers.domain_categorization import DomainCategorizationHelper
from hunt.sources.mcafee import McAfeeRequestData
from hunt.sources.trendmicro import TrendMicroRequestData
from hunt.sources.ibm import IbmXforceRequestData
from hunt.sources.bluecoat import BluecoatRequestData
from hunt.sources.cloudflare_webdriver import CloudflareRadarWebDriver


class LookupHelper:
    @staticmethod
    async def lookup(domain, options):
        try:
            all, ibm, trendmicro, mcafee, bluecoat, cloudflare = options
        except:
            all = options

        tasks = []
        if all or mcafee:
            source = McAfeeRequestData()
            tasks.append(asyncio.create_task(source.check(domain)))
        if all or bluecoat:
            source = BluecoatRequestData()
            tasks.append(asyncio.create_task(source.check(domain)))
        if all or trendmicro:
            source = TrendMicroRequestData()
            tasks.append(asyncio.create_task(source.check(domain)))
        if all or ibm:
            print('IBM X-Force: Ensure your API credentials are valid. Only good for 30 days per account.')
            source = IbmXforceRequestData(config.IBM_XFORCE_API_KEY, config.IBM_XFORCE_SECRET_KEY)
            tasks.append(asyncio.create_task(source.check(domain)))
        if all or cloudflare:
            source = CloudflareRadarWebDriver()
            tasks.append(asyncio.create_task(source.check(domain)))
        
        data = await asyncio.gather(*tasks)
        
        for item in data:
            try:
                DomainCategorizationHelper.check_add_categorization_record(domain, item['name'], item['category'])
            except Exception as e:
                logging.warn(f'something went wrong when trying to add categorization records for item: {item}')

        DomainHelper.get_recent(table=True)