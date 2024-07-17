# Hunt

#### The automated domain management and categorization lookup utility


## Features

* Domain name management to track operational domains and their respective roles (C2, phish, landing page, etc.)
* Automated domain categorization lookup across multiple categorization sites. Current categorizaton sites include:
  * IBM X-Force (API key required)
  * TrendMicro Site Safety
  * McAfee Site Lookup
  * Bluecoat (via selenium/ChromeDriver)
  * Cloudflare Radar
* Database-backed to collect and track categorization changes over time

## Installation

This is a Python3 project. Install dependencies with: `pip -r requirements.txt`

To begin using hunt, run the `init` command to setup the local database:

```
python hunt.py init
```

## Commands

Hunt provides a number of commands to lookup domain categorizations:

### init

This establishes a folder on disk where the hunt database is stored. For Windows, the location is in `%LOCALAPPDATA%\hunt`, for POSIX systems, the location is `~\.hunt`. A SQLite database file is created in this directory, which contains two tables: `domains` and `domaincategorizations`. This command considers the utility initialized if a non-zero byte SQLite database is present in the data directory. If any command is run, it checks for this file and exits unless the file exists.


### get-categorizations

This is the main component of the tool. It accepts a domain name or a file of domains and some boolean options for which categorization sites to check:

```
Usage: hunt.py command get-categorizations [OPTIONS] DOMAIN

Options:
  -a, --all-cats    Check with all providers
  -i, --ibm         Check IBM X-Force
  -t, --trendmicro  Check Trendmicro
  -m, --mcafee      Check McAfee
  -b, --bluecoat    Check Bluecoat
  -c, --cloudflare  Check Cloudflare Radar
  --help            Show this message and exit.
```

On the backend, asynchronous tasks are created for each selected (or all) categorization sites, and hunt performs scraping of data and returns the results as a table:

```
> python hunt.py command get-categorizations intuit.com -a

                               Recent Categorizations
┏━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ domain     ┃ source     ┃ category                         ┃ last checked        ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ intuit.com │ trendmicro │ Financial Services               │ 2024-07-02 11:22:22 │
│ intuit.com │ ibm-xforce │ Platform as a Service (Score: 1) │ 2024-07-02 11:22:22 │
│ intuit.com │ mcafee     │ Internet Services                │ 2024-07-02 11:22:50 │
└────────────┴────────────┴──────────────────────────────────┴─────────────────────┘
```

### add-domain

This command adds a domain or updates a domain in the database. It takes a name, optional registrar, and a tag with the default set of options defined in the `tag` command:

```
Usage: hunt.py command add-domain [OPTIONS] DOMAIN TAG [REGISTRAR]

Options:
  --help  Show this message and exit.
```

### refresh

This command takes each stored domain in the database and performs domain categorization checks against all available categorization services. The output of the command retrieves the last 10 categorization records stored in the database.

## Queries

Hunt provides a number of commands to query the database for information:

### domain-categories

This command retrieves all historical domain categorizations for a given domain:

```
Usage: hunt.py query domain-categories [OPTIONS] DOMAIN

Options:
  --help  Show this message and exit.
```

The output is a table similar to the `get-categorizations` command:

```
> python hunt.py query domain-categories intuit.com

                    Categorizations for: intuit.com
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ source     ┃ category                         ┃ checked at          ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ trendmicro │ Financial Services               │ 2024-07-02 11:22:22 │
│ ibm-xforce │ Platform as a Service (Score: 1) │ 2024-07-02 11:22:22 │
│ mcafee     │ Internet Services                │ 2024-07-02 11:22:50 │
└────────────┴──────────────────────────────────┴─────────────────────┘
```

### domain-categories-filter

This command takes a domain argument and prompts the user for a categorization provider to filter results by. If the provider name is invalid, a list of options are shown to choose from.

### tag

This command returns any stored domains with a specified tag. The available tags are 'phish', 'c2', 'landing' and 'misc'

### recent

This command returns the last 10 domain categorizations stored in the database.

### get-domains

This command returns all stored domains in the database.

### export

This command exports domain categorization records. if 'all' is supplied as the domain value, all stored domain categorizations are exported. An optional parameter '-p' allows you to supply a provider to filter results by:

```
Usage: hunt.py query export [OPTIONS] DOMAIN

Options:
  -p, --provider TEXT  The provider to filter domain categorizations by
  --help               Show this message and exit.
```

Export by single domain:

```
hunt.py query export intuit.com
```

Export all:

```
hunt.py query export all
```

Export all, filtering only mcafee categorizations:

```
hunt.py query export all -p mcafee
```

## Adding New Categorization Services

With some code changes, it is possible to integrate additional categorization services to the hunt project. First, define a new class in `hunt\sources` that returns a dictionary for the result:

```python
from hunt.utils.requests import RequestData


class CategorizationSiteRequestData(RequestData):
    url = 'https://api.categorizationsite.com/api/url/{target_domain}'
    name = 'some-short-name'
    
    def __init__(self, api_key, api_secret):
        super(CategorizationSiteRequestData, self).__init__(self.url)
        auth_string = f'{api_key}:{api_secret}'
        encoded_authentication = f'Basic {base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")}'
        self._update_headers({'Authorization': encoded_authentication})

    async def check(self, target_domain):
        category = 'N/A'
        self.url = self.url.format(target_domain=target_domain)
        
        response = await self.async_client.get(self.url, timeout=20)
        if response.status_code != 200:
            return {
                'name': self.name,
                'category': category,
            }
        
        response_json = response.json()
        category = [item for item in response_json['result']['cats']][0]
        score = response_json['result']['score']
        category = f'{category} (Score: {score})'
        
        return {
            'name': self.name,
            'category': category,
        }
```

Next, reference that new source module class in `helpers\lookup.py`:

```python
from hunt.sources.categorizationsite import CategorizationSiteRequestData

try:
    all, ibm, trendmicro, mcafee, categorizationsite = options
except:
    all = options

if all or categorizationsite:
    source = CategorizationSiteRequestData(config.API_KEY, config.SECRET_KEY)
    tasks.append(asyncio.create_task(source.check(domain)))
```

Next, modify `hunt.py` and add to the `shared_options` decorator:

```python
click.option('-c', '--categorizationsite', is_flag=True, default=False, help='Check Categorization Site')
```

Then, modify the function parameters for `get_categorizations` function:
```python
async def get_categorizations(domain, all_cats, ibm, trendmicro, mcafee, bluecoat, cloudflare, categorizationsite):
    categorization_lookup_options = [all_cats, ibm, trendmicro, mcafee, bluecoat, cloudflare, categorizationsite]
```

With these changes, a new categorization site can be added to the project and can be called from the utility.

## Caveats

This pertains to using IBM X-Force's API. It requires an IBM ID to use, and the current free trial is for 30 days. I use a disposable email address to set up the account initially and access my API tokens with that account. When using the X-Force categorization source with `hunt`, a notice will appear in the console reminding the user of this fact.

In order to safely scrape from Bluecoat Site Review, selenium is used. This requires [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) to be installed in order to use. For Windows, add the path to chromedriver.exe to `config.py` variable 'CHROMEDRIVER_PATH'. This should not apply to macOS and Linux hosts.

## TODO

* Add additional categorization sites to sources