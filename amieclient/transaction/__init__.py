import json
from datetime import datetime

from ..packet import Packet


class Transaction(object):
    def __init__(self, transaction_id, state,
                 originating_site, local_site, remote_site,
                 packets=None):
        self.id = transaction_id
        self.state = state
        self.originating_site = originating_site
        self.local_site = local_site
        self.remote_site = remote_site
        if packets:
            self.packets = packets
        else:
            self.packets = []

    @classmethod
    def from_json(cls, json_in):
        tx_in = json.loads(json_in)
        tx = cls(
                 transaction_id=tx_in['transaction_id'],
                 state=tx_in['state'],
                 originating_site=tx_in['originating_site_name'],
                 local_site=tx_in['local_site_name'],
                 packets=[Packet.from_json(p) for p in tx_in['DATA']]
        )
        return tx

    @property
    def json(self):
        data_dict = {
            'DATA_TYPE': 'transaction',
            'transaction_ID': self.id,
            'originating_site_name':  self.originating_site,
            'local_site_name': self.local_site,
            'remote_site_name': self.remote_site,
            'state': self.state,
            'DATA': [pkt.json for pkt in self.packets]
        }

        return json.dumps(data_dict)
