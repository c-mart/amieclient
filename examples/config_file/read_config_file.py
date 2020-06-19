#!/usr/bin/env python3

"""
This example demonstrates one way to store neccessary connection information
for amieclient. Take a look at ./config.ini for an example of the format that
Python's configparser expects. Three different sections are defined there --
PSC, PSC_TEST, and NCSA -- representing three different configurations.

We load and parse that configuration file, then use that to create client
objects.
"""

from configparser import ConfigParser

from amieclient import Client

# For more information on the configparser library, please see the python documentation
# https://docs.python.org/3.5/library/configparser.html
config = ConfigParser()
config.read('config.ini')

# Get each section of the config file and give it a friendly name.
psc_config = config['PSC']
psc_test_config = config['PSC_TEST']
ncsa_config = config['NCSA']

# Create the various clients. In real life, you'd almost certainly only have
# one client.

# These clients all use the default value for the base URL, which is
# https://amieclient.xsede.org/v0.10/
psc_client = Client(site_name=psc_config['site_name'])
ncsa_client = Client(site_name=ncsa_config['site_name'])

# This client uses a (made-up) different base URL.
psc_test_client = Client(site_name=psc_test_config['site_name'],
                         base_url=psc_test_config['base_url'])

# If you're into being mysterious and obscure, you could also use dictionary
# expansion to pass your configuration variables based on the configuration
# section of your choice.
psc_test_client_2 = Client(**psc_test_config)

