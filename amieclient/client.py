from urllib.parse import urljoin

import requests
import dateutil


from .packet import PacketList
from .packet.base import Packet
from .transaction import Transaction

from .demo_json_str import (DEMO_JSON_PKT_LIST, DEMO_JSON_PKT_1,
                            DEMO_JSON_PKT_2, DEMO_JSON_TXN_LIST,
                            DEMO_JSON_TXN)


"""AMIE client class"""


class Client(object):
    """
    AMIE Client.

    Args:
        site_name (str): Name of the client site.
        api_key (str): API key secret
        base_url (str): Base URL for the XSEDE api
    Example:
        psc_client = amieclient.Client(site_name='PSC', api_key=some_secrets_store['amie_api_key'])
        psc_alt_base_client = amieclient.Client(site_name='PSC',
                                                api_key='test_api_key',
                                                base_url='https://amieclient.xsede.org/v0.20_beta/)

    """
    def __init__(self, site_name, api_key, base_url='https://amieclient.xsede.org/v0.10/'):
        self.base_url = base_url
        self.site_name = site_name
        self.full_url = urljoin(self.base_url, self.site_name)

        amie_headers = {
            'XA-API-KEY': api_key,
            'XA-SITE': site_name
        }
        s = requests.Session()
        s.headers.update(amie_headers)
        self._session = s

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    @staticmethod
    def _join_list(things):
        if things is not None and things != []:
            # If we're given a list, join it with commas
            return ','.join(things)
        elif things == []:
            # if we're given an empty list, return None
            return None
        else:
            # If we're given anything else, i.e. None or some other single thing,
            # give it back
            return things

    @staticmethod
    def _dt_range(start, end):
        if start is None and end is None:
            time_str = None
        else:
            start_str = start.isoformat() if start else ""
            end_str = end.isoformat() if end else ""
            time_str = "{},{}".format(start_str, end_str)
        return time_str

    def get_transaction(self, *, trans_rec_id):
        """
        Given a single transaction id, fetches the related transaction.
        """
        url = urljoin(self.base_url,
                      f'/transactions/{self.site_name}/{trans_rec_id}/packets')
        r = self._session.get(url)
        r.raise_for_status()
        return Transaction.from_dict(r.json())

    def get_packet(self, *, packet_rec_id):
        """
        Given a single packet record id, fetches the packet.
        """
        return Transaction.from_json(DEMO_JSON_TXN)


    def list_packets(self, *, trans_rec_ids=None, outgoing=None,
                     update_time_start=None, update_time_until=None,
                     states=None, client_states=None, incoming=None):
        """
        Fetches a list of transactions based on the provided search parameters
        """
        trans_rec_ids_str = self._join_list(trans_rec_ids)
        states_str = self._join_list(states)
        client_states_str = self._join_list(client_states)
        time_str = self._dt_range(update_time_start, update_time_until)

        # Build a dict of parameters. Requests skips any with a None value,
        # so no need to weed them out
        params = {
            'trans_rec_id': trans_rec_ids_str,
            'outgoing': outgoing,
            'update_time': time_str,
            'states': states_str,
            'client_states': client_states_str,
            'incoming': incoming
        }

        # Get the list of packets
        # response = self._session.get('/packet_list', params=params)
        # DEMO TIME
        return PacketList.from_json(DEMO_JSON_PKT_LIST)


    def send_packet(self, packet, skip_validation=False):
        """
        Send a packet
        """
        if not skip_validation:
            packet.validate_data()

        print("Here's what I would send...")
        print(packet.json)
