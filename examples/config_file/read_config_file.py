#!/usr/bin/env python3

"""
This example demonstrates one way to store neccessary connection information
for amieclient. Take a look at ./config.ini for an example of the format that
Python's configparser expects. Three different sections are defined there --
PSC, PSC_TEST, and NCSA_LOCAL_DEV -- containing three different configurations.

PSC: Site name is PSC; points to the production URL endpoint
PSC_TEST: Site name is also PSC, but the base URL is for a hypothetical version 0.2
NSCA_LOCAL_TEST: Site name is NSCA. It points to a AMIE REST API running on localhost:12345

We load and parse that configuration file, then use that to create client
objects for each of the provided configurations.
"""

from configparser import ConfigParser

from amieclient import Client

# For more information on the configparser library, please see the python docs:
# https://docs.python.org/3.5/library/configparser.html
config = ConfigParser()
config.read('config.ini')

# Get each section of the config file and give it a friendly name.
psc_config = config['PSC']
psc_test_config = config['PSC_TEST']
local_dev_config = config['NCSA_LOCAL_DEV']

# Create the various clients. In real life, you'd almost certainly only have
# one client.

# These clients all use the default value for the base URL, which is
# https://amieclient.xsede.org/v0.10/
psc_client = Client(site_name=psc_config['site_name'], api_key=psc_config['api_key'])

# These clients use (made-up) different base URLs.
psc_test_client = Client(site_name=psc_test_config['site_name'],
                         base_url=psc_test_config['base_url'],
                         api_key=psc_test_config['api_key'])
local_dev_client = Client(site_name=local_dev_config['site_name'],
                          base_url=local_dev_config['base_url'],
                          api_key=local_dev_config['api_key'])

# If you're into being mysterious and obscure, you could also use dictionary
# expansion to pass your configuration variables based on the configuration
# section of your choice. This will save yourself like 10 keystrokes.
psc_test_client_2 = Client(**psc_test_config)
