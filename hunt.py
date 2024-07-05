#!/usr/bin/env python
import argparse
import asyncio
import sys
from hunt.helpers import is_initialized
from hunt.helpers.domain import DomainHelper
from hunt.helpers.domain_categorization import DomainCategorizationHelper
from hunt.helpers.lookup import LookupHelper
from hunt.models.domain import Domain
from hunt.utils.hunt_db import HuntDb


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description='check a domain across multiple categorization services')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # init command args
    parser_init = subparsers.add_parser('init', help="initialize hunt database")
    
    # lookup command args
    parser_lookup = subparsers.add_parser('lookup', help='lookup a domain')
    parser_lookup.add_argument('-d', '--domain', required=True, help='domain to check')
    parser_lookup.add_argument('-a', '--all', action='store_true', default=False, help='check with all')
    parser_lookup.add_argument('-i', '--ibm', action='store_true', default=False, help='check ibm x-force')
    parser_lookup.add_argument('-t', '--trendmicro', action='store_true', default=False, help='check trendmicro')
    parser_lookup.add_argument('-m', '--mcafee', action='store_true', default=False, help='check mcafee')
    parser_lookup.add_argument('-b', '--bluecoat', action='store_true', default=False, help='check bluecoat')
    
    # retrieve command args
    parser_retrieve = subparsers.add_parser('retrieve', help="retrieve categorization results for a domain")
    parser_retrieve.add_argument('-d', '--domain', required=True, help="domain to retrieve")
        
    # tag command args
    parser_tag = subparsers.add_parser('tag', help="get stored domains by tag")
    parser_tag.add_argument('-n', '--name', required=True, help="tag to retrieve")
    
    # recent command args
    parser_recent = subparsers.add_parser('recent', help="get recent records")
    
    # domain command args
    parser_domain = subparsers.add_parser('domain', help="manage domains in database")
    parser_domain.add_argument('-d', '--domain', required=True, help="domain to retrieve")
    parser_domain.add_argument('-r', '--registrar', help="domain registrar")
    parser_domain.add_argument('-t', '--tag', choices=['phish', 'c2', 'landing', 'misc'], required=True, help="tag to apply")
    
    # recent command args
    parser_refresh = subparsers.add_parser('refresh', help="refresh lookup records")

    args = parser.parse_args()
    
    if args.command == 'init':
        hunt_db = HuntDb()
        hunt_db.setup()
        sys.exit(0)
    
    if not is_initialized():
        sys.exit(-1)
    
    if args.command == 'lookup':
        categorization_lookup_options = [args.all, args.ibm, args.trendmicro, args.mcafee, args.bluecoat]
        if all(not option for option in categorization_lookup_options):
            print('Please select a categorization site option or choose --all')
            sys.exit(-1)
        asyncio.run(LookupHelper.lookup(args.domain, categorization_lookup_options))
    
    if args.command == 'retrieve':
        results = DomainCategorizationHelper.get_by_domain(args.domain, table=True)
        
    if args.command == 'tag':
        results = DomainHelper.get_by_tag(args.name, table=True)

    if args.command == 'recent':
        results = DomainHelper.get_recent(table=True)
    
    if args.command == 'domain':
        domain_record, created = Domain.get_or_create(domain=args.domain, registrar=args.registrar or '', tag=args.tag)
    
    if args.command == 'refresh':
        DomainCategorizationHelper.refresh()
