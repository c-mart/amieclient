"""
AMIE packets relating to accounts

notify_account_create
notify_account_inactivate 
notify_account_reactivate 
request_account_create 
request_account_inactivate
request_account_reactivate 
"""

from . import Packet

class DataAccountCreate(Packet):
    _packet_type = 'data_account_create'
    _expected_reply = ['inform_transaction_complete']
    _data_keys_required = ['PersonID', 'ProjectID']
    _data_keys_allowed = ['DnList']
