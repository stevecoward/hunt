import click
import sys
from hunt.helpers import is_initialized


def validate_tag_choices(ctx, param, value):
    tags = ['c2','phish','landing','misc']
    if value not in tags:
        raise click.BadParameter(f'please select from the following tags: {", ".join(tags)}')
    return value


def validate_categorization_providers(ctx, param, value):
    providers = ['bluecoat', 'ibm-xforce', 'mcafee', 'trendmicro', 'cloudflare']
    if value not in providers:
        raise click.BadParameter(f'please select from the following providers: {", ".join(providers)}')
    return value


def check_initialized(ctx, param, value):
    if not is_initialized():
        raise click.UsageError('hunt is not initialized. please run "command init" first.')
    return value
