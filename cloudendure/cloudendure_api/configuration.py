# -*- coding: utf-8 -*-
"""Define the CloudEndure API configuration."""
from __future__ import absolute_import, print_function

import copy
import logging
import multiprocessing
import os
import sys
from pathlib import Path
from typing import Any, Dict

import requests
import six
import urllib3
import yaml
from six.moves import http_client as httplib


class TypeWithDefault(type):
    def __init__(cls, name, bases, dct):
        super(TypeWithDefault, cls).__init__(name, bases, dct)
        cls._default = None

    def __call__(cls):
        if cls._default is None:
            cls._default = type.__call__(cls)
        return copy.copy(cls._default)

    def set_default(cls, default):
        cls._default = copy.copy(default)


class Configuration(six.with_metaclass(TypeWithDefault, object)):
    """NOTE: This class is auto generated by the swagger code generator program.

    Ref: https://github.com/swagger-api/swagger-codegen
    Do not edit the class manually.
    """

    def __init__(self):
        """Constructor"""
        self.active_config = {}

        # Default Base url
        _config_path = os.environ.get("CLOUDENDURE_CONFIG_PATH", "~/.cloudendure.yaml")
        if _config_path.startswith("~"):
            self.config_path = os.path.expanduser(_config_path)
        _config = Path(self.config_path)
        if not _config.exists():
            print(
                "No CloudEndure YAML configuration found! Creating it at: (%s)",
                self.config_path,
            )
            self.write_yaml_config(
                config={
                    "host": "https://console.cloudendure.com",
                    "api_version": "latest",
                    "auth_ttl": "3600",
                    "username": "",
                    "password": "",
                    "token": "",
                }
            )
        self.update_config()

        self.host = "https://console.cloudendure.com/api/latest"
        # Temp file folder for downloading files
        self.temp_folder_path = None

        # Authentication Settings
        # dict to store API key(s)
        self.api_key = {"X-XSRF-TOKEN": ""}
        # dict to store API prefix (e.g. Bearer)
        self.api_key_prefix = {}
        # Logging Settings
        self.logger = {}
        self.logger["package_logger"] = logging.getLogger("cloudendure_api")
        self.logger["urllib3_logger"] = logging.getLogger("urllib3")
        # Log format
        self.logger_format = "%(asctime)s %(levelname)s %(message)s"
        # Log stream handler
        self.logger_stream_handler = None
        # Log file handler
        self.logger_file_handler = None
        # Debug file location
        self.logger_file = None
        # Debug switch
        self.debug = False

        # SSL/TLS verification
        # Set this to false to skip verifying SSL certificate when calling API
        # from https server.
        self.verify_ssl = True
        # Set this to customize the certificate file to verify the peer.
        self.ssl_ca_cert = None
        # client certificate file
        self.cert_file = None
        # client key file
        self.key_file = None
        # Set this to True/False to enable/disable SSL hostname verification.
        self.assert_hostname = None

        # urllib3 connection pool's maximum number of connections saved
        # per pool. urllib3 uses 1 connection as default value, but this is
        # not the best value when you are making a lot of possibly parallel
        # requests to the same host, which is often the case here.
        # cpu_count * 5 is used as default value to increase performance.
        self.connection_pool_maxsize = multiprocessing.cpu_count() * 5

        # Proxy URL
        self.proxy = None
        # Safe chars for path_param
        self.safe_chars_for_path_param = ""

    @property
    def logger_file(self):
        """Define the logger file getter.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str

        """
        return self.__logger_file

    @logger_file.setter
    def logger_file(self, value):
        """Define the logger file setter.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str

        """
        self.__logger_file = value
        if self.__logger_file:
            # If set logging file,
            # then add file handler and remove stream handler.
            self.logger_file_handler = logging.FileHandler(self.__logger_file)
            self.logger_file_handler.setFormatter(self.logger_formatter)
            for _, logger in six.iteritems(self.logger):
                logger.addHandler(self.logger_file_handler)
                if self.logger_stream_handler:
                    logger.removeHandler(self.logger_stream_handler)
        else:
            # If not set logging file,
            # then add stream handler and remove file handler.
            self.logger_stream_handler = logging.StreamHandler()
            self.logger_stream_handler.setFormatter(self.logger_formatter)
            for _, logger in six.iteritems(self.logger):
                logger.addHandler(self.logger_stream_handler)
                if self.logger_file_handler:
                    logger.removeHandler(self.logger_file_handler)

    @property
    def debug(self):
        """Get the Debug status

        :param value: The debug status, True or False.
        :type: bool

        """
        return self.__debug

    @debug.setter
    def debug(self, value):
        """Set the Debug status.

        :param value: The debug status, True or False.
        :type: bool

        """
        self.__debug = value
        if self.__debug:
            # if debug status is True, turn on debug logging
            for _, logger in six.iteritems(self.logger):
                logger.setLevel(logging.DEBUG)
            # turn on httplib debug
            httplib.HTTPConnection.debuglevel = 1
        else:
            # if debug status is False, turn off debug logging,
            # setting log level to default `logging.WARNING`
            for _, logger in six.iteritems(self.logger):
                logger.setLevel(logging.WARNING)
            # turn off httplib debug
            httplib.HTTPConnection.debuglevel = 0

    @property
    def logger_format(self):
        """Define the logger format getter.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        return self.__logger_format

    @logger_format.setter
    def logger_format(self, value):
        """Define the logger format setter.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str

        """
        self.__logger_format = value
        self.logger_formatter = logging.Formatter(self.__logger_format)

    def get_api_key_with_prefix(self, identifier: str) -> str:
        """Get the API key (with prefix if set).

        :param identifier: The identifier of apiKey.
        :return: The token for api key authentication.

        """
        if self.api_key.get(identifier) and self.api_key_prefix.get(identifier):
            return (
                f"{self.api_key_prefix[identifier]} {self.api_key[identifier]}"
            )  # noqa: E501
        if self.api_key.get(identifier):
            return self.api_key[identifier]
        return ""

    def get_basic_auth_token(self):
        """Get HTTP basic authentication header (string).

        :return: The token for basic HTTP authentication.

        """
        return urllib3.util.make_headers(
            basic_auth=f'{self.active_config.get("username", "")}:{self.active_config.get("password", "")}'
        ).get("authorization")

    def auth_settings(self) -> Dict[str, Any]:
        """Get the Auth Settings dict for api client.

        :return: The Auth Settings information dict.

        """
        return {
            "api_key": {
                "type": "api_key",
                "in": "header",
                "key": "X-XSRF-TOKEN",
                "value": self.get_api_key_with_prefix("X-XSRF-TOKEN"),
            }
        }

    def to_debug_report(self) -> str:
        """Get the essential information for debugging.

        :return: The report for debugging.

        """
        return (
            "Python SDK Debug Report:\n"
            f"OS: {sys.platform}\n"
            f"Python Version: {sys.version}\n"
            "Version of the API: 5\n"
            "SDK Package Version: 0.1.0"
        )

    def read_yaml_config(self):
        """Read the CloudEndure YAML configuration file."""
        with open(self.config_path, "r") as yaml_stream:
            try:
                config = yaml.safe_load(yaml_stream)
            except yaml.YAMLError as e:
                config = {}
                print(e)
        return config

    def write_yaml_config(self, config):
        """Write to the CloudEndure YAML configuration file."""
        with open(self.config_path, "w") as yaml_file:
            try:
                yaml.dump(config, yaml_file, default_flow_style=False)
                return True
            except Exception as e:
                print(
                    f"Exception encountered while writing the CloudEndure YAML configuration file - ({e})"
                )
        return False

    def update_yaml_config(self, kwargs):
        _config = self.read_yaml_config()
        _config.update(kwargs)
        self.write_yaml_config(_config)
        self.update_config()

    def get_env_vars(self, prefix="cloudendure"):
        """Get all environment variables starting with CLOUDENDURE_."""
        prefix = prefix.strip("_")
        env_vars = {
            x[0].lower().lstrip(prefix.lower()).strip("_"): x[1]
            for x in os.environ.items()
            if x[0].lower().startswith(prefix.lower())
        }
        print(env_vars)
        return env_vars

    def refresh_auth(self, username="", password=""):
        """Refresh the authentication token with the CloudEndure API.

        Args:
            username (str): The CloudEndure username to be used.
                Defaults to the environment specific default.
            password (str): The CloudEndure password to be used.
                Defaults to the environment specific default.

        Attributes:
            endpoint (str): The CloudEndure API endpoint to be used.
            _username (str): The CloudEndure API username.
            _password (str): The CloudEndure API password.
            _auth (dict): The CloudEndure API username/password dictionary map.
            response (requests.Response): The CloudEndure API login request response object.
            _xsrf_token (str): The XSRF token to be used for subsequent API requests.

        """
        endpoint: str = "login"
        _username: str = self.active_config.get("username", "") or username
        _password: str = self.active_config.get("password", "") or password
        _auth: Dict[str, str] = {"username": _username, "password": _password}

        # Attempt to login to the CloudEndure API via a POST request.
        response: requests.Response = requests.post(
            f"{self.host}/{endpoint}", json=_auth
        )
        print("response: ", response, response.status_code)

        # Check whether or not the request was successful.
        if response.status_code not in [200, 307]:
            raise Exception()

        print("response: ", response, response.cookies)
        _xsrf_token: str = str(response.cookies["XSRF-TOKEN"])

        # Strip the XSRF token of wrapping double-quotes from the cookie.
        if _xsrf_token.startswith('"') and _xsrf_token.endswith('"'):
            _xsrf_token: str = _xsrf_token[1:-1]

        # Set the XSRF token data on the CloudEndureAPI object.
        return _xsrf_token

    def update_config(self):
        self.yaml_config_contents = self.read_yaml_config()
        self.env_config = self.get_env_vars()
        self.active_config = {**self.yaml_config_contents, **self.env_config}

    def update_token(self, token):
        self.update_yaml_config({"token": token})

    def get_var(self, var):
        """Get the specified environment or config variable."""
        env_var = os.environ.get(var.upper(), "")

        if not env_var:
            env_var = self.yaml_config_contents.get(var.lower(), "")

        return env_var
