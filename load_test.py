from configparser import ConfigParser 
from amieclient.client import AMIEClient 
config = ConfigParser() 
config.read('testing_credentials.ini') 
psc_client = AMIEClient(**config['PSC_TEST'])
