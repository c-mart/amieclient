from configparser import ConfigParser 
from amieclient.client import AMIEClient, UsageClient
config = ConfigParser() 
config.read('testing_credentials.ini') 
chosen_config = 'PSC_TEST'
#chosen_config = 'SDSC_TEST'
site = config[chosen_config]['site_name']
a_url = config[chosen_config]['amie_url']
u_url = config[chosen_config]['usage_url']
api_key = config[chosen_config]['api_key']

amie_client = AMIEClient(site_name=site, amie_url=a_url, api_key=api_key)
usage_client = UsageClient(site_name=site, usage_url=u_url, api_key=api_key)
