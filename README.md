# cloudendure-python

Python wrapper and CLI for [CloudEndure](https://www.cloudendure.com/)

[![PyPI](https://img.shields.io/pypi/v/cloudendure) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cloudendure)](https://pypi.org/project/cloudendure/) [![Build Status](https://travis-ci.com/mbeacom/cloudendure-python.svg?branch=master)](https://travis-ci.com/mbeacom/cloudendure-python)

[Documentation](https://mbeacom.github.io/cloudendure-python/)

## Requirements

[Python 3.7+](https://www.python.org/downloads/)

## Installation & Usage

### pipenv

```sh
brew install pipenv # if not installed
pipenv install cloudendure
```

### pip

```sh
pip install cloudendure
```

### Usage

Then import the package:

```python
import cloudendure
```

## Getting Started

![CloudEndure Flow](images/migration_pipeline.svg)

### Logging in via CLI using environment variables

Please note: `cloudendure` and `ce` can be used interchangeably

```sh
export CLOUDENDURE_USERNAME=<your_ce_user>
export CLOUDENDURE_PASSWORD=<your_ce_password>
export CLOUDENDURE_DESTINATION_ACCOUNT=<destination_aws_account_id>

cloudendure api login
```

or

```sh
export CLOUDENDURE_USER_API_TOKEN=<your_ce_user_api_token>
export CLOUDENDURE_DESTINATION_ACCOUNT=<destination_aws_account_id>

ce api login
```

### Logging in via CLI inline

Please note: `cloudendure` and `ce` can be used interchangeably

```sh
cloudendure api login --user=<your_ce_user> --password=<your_ce_password>
```

or

```sh
ce api login --token=<your_ce_user_api_token>
```

Logging in for the first time will generate the `~/.cloudendure.yml` file.

## Coming Soon

This project is currently a work in progress and will actively change. This client has not yet been finalized and is entirely subject to change.

## Changelog

Check out the [CHANGELOG](CHANGELOG.md)
