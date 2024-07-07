#!/usr/bin/env python
import argparse
import asyncio
import click
import sys
from hunt.helpers.click_validators import check_initialized, validate_tag_choices, validate_categorization_providers
from hunt.helpers.domain import DomainHelper
from hunt.helpers.domain_categorization import DomainCategorizationHelper
from hunt.helpers.lookup import LookupHelper
from hunt.models.domain import Domain
from hunt.utils.hunt_db import HuntDb


@click.group()
@click.pass_context
def cli(ctx):
    pass


@click.group()
def command():
    pass


@click.command()
def init():
    hunt_db = HuntDb()
    hunt_db.setup()
    sys.exit(0)


@click.command()
@click.argument('domain', required=True)
@click.argument('tag', required=True, callback=validate_tag_choices)
@click.argument('registrar', required=False, default='')
@click.option('--initialize', is_flag=True, callback=check_initialized, expose_value=False, hidden=True)
def add_domain(domain, tag, registrar):
    domain_record, created = Domain.get_or_create(domain=domain, registrar=registrar, tag=tag)
    DomainHelper.get_by_domain(domain_record.domain, table=True)


@click.command()
def refresh():
    DomainCategorizationHelper.refresh()


@click.command()
@click.argument('domain', required=True)
@click.option('-a', '--all-cats', is_flag=True, default=False, help='Check with all providers')
@click.option('-i', '--ibm', is_flag=True, default=False, help='Check IBM X-Force')
@click.option('-t', '--trendmicro', is_flag=True, default=False, help='Check Trendmicro')
@click.option('-m', '--mcafee', is_flag=True, default=False, help='Check McAfee')
@click.option('-b', '--bluecoat', is_flag=True, default=False, help='Check Bluecoat')
@click.option('--initialize', is_flag=True, callback=check_initialized, expose_value=False, hidden=True)
def get_categorizations(domain, all_cats, ibm, trendmicro, mcafee, bluecoat):
    categorization_lookup_options = [all_cats, ibm, trendmicro, mcafee, bluecoat]
    if all(not option for option in categorization_lookup_options):
        print('Please select a categorization site option or choose --all')
        sys.exit(-1)
    asyncio.run(LookupHelper.lookup(domain, categorization_lookup_options))


@click.group()
def query():
    pass


@click.command()
@click.argument('domain', required=True)
@click.option('--initialize', is_flag=True, callback=check_initialized, expose_value=False, hidden=True)
def domain_categories(domain):
    DomainCategorizationHelper.get_by_domain(domain, table=True)


@click.command()
@click.argument('domain', required=True)
@click.option('-p', '--provider', prompt='Provider', callback=validate_categorization_providers, help='The provider to filter domain categorizations by')
@click.option('--initialize', is_flag=True, callback=check_initialized, expose_value=False, hidden=True)
def domain_categories_filter(domain, provider):
    DomainCategorizationHelper.get_by_domain(domain, provider, table=True)


@click.command()
@click.option('--initialize', is_flag=True, callback=check_initialized, expose_value=False, hidden=True)
def recent():
    DomainHelper.get_recent(table=True)


@click.command()
@click.argument('name', required=True, callback=validate_tag_choices)
@click.option('--initialize', is_flag=True, callback=check_initialized, expose_value=False, hidden=True)
def tag(name):
    DomainHelper.get_by_tag(name, table=True)


@click.command()
@click.option('--initialize', is_flag=True, callback=check_initialized, expose_value=False, hidden=True)
def get_domains():
    DomainHelper.get_all(table=True)



command.add_command(init)
command.add_command(add_domain)
command.add_command(refresh)
command.add_command(get_categorizations)

query.add_command(domain_categories_filter)
query.add_command(domain_categories)
query.add_command(recent)
query.add_command(tag)
query.add_command(get_domains)

cli.add_command(command)
cli.add_command(query)


if __name__ == '__main__':    
    cli()
