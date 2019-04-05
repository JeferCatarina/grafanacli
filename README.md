# grafanacli [![GitHub license](https://img.shields.io/github/license/m0nhawk/grafana_api.svg?style=flat-square)](https://github.com/JeferCatarina/grafanacli/blob/master/LICENSE) 

## What the heck is that?

GrafanaCLI is a Python library used to manage Grafana API

## Requirements

Python :: 2
Python :: 3

## Installation

Install the pip package:

```
pip install grafanacli
```

## Usage

```python
from grafanacli import GrafanaAdmin

ga = GrafanaAdmin('http://127.0.0.1:3000')

# Disable SSL verification
ga.verify = False
SSL verification must by disabled after use GrafanaAuth

# Authentication using username and password
ga.GrafanaAuth(Username='admin', Password='admin')

# Authentication using API-Key
ga.GrafanaAuth(AuthType='APIKey', Key='xxxxxxxxxxxxx')

# List your current organization
ga.CurrentOrganization()

# List all organizations
ga.OrganizationList()

# Search Organization
ga.OrganizationSearch('MyOrganization')

# Create Organization
ga.OrganizationCreate('MyNewOrganization')

# Update Organization
ga.OrganizationUpdate('1', 'NewOrganizationName')
Where "1" is the organization Id that will be updated.

# Delete Organization
ga.OrganizationDelete('1')
Where "1" is the organization Id that will be deleted.

# Switch Organization
ga.OrganizationSwitch('2')
Where "2" is the organization Id what I want to switch

# Search dashboard whitout filter
ga.DashboardSearch()

# Search dashboard by title
ga.DashboardSearch(DashboardName='My Dashboard')

# Search dashboard by tag
ga.DashboardSearch(Tag='My Tag')

# Search starred dashboards
ga.DashboardSearch(Starred=True)

# Search dashboard aplying more than one conditition
ga.DashboardSearch(Starred=True, Tag='My Tag')
ga.DashboardSearch(Name='My Dashboard', Tag='My Tag')
ga.DashboardSearch(Name='My Dashboard', Tag='My Tag', Starred=True)

# Download Dashboard
ga.DashboardDownload('DashboardUid', '/tmp/mydash.json')

# Upload Dashboard
ga.DashboardUpload('/tmp/mydash.json', Overwrite=True)
ga.DashboardUpload('/tmp/mydash.json')
ga.DashboardUpload('/tmp/mydash.json, FolderId=3'

```

## License

GrafanaCLI is licensed under the terms of the MIT License (see the
[LICENSE](LICENSE) file).