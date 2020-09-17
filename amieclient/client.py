
import requests

from .packet import PacketList
from .packet.base import Packet
from .transaction import Transaction


"""AMIE client class"""


class Client(object):
    """
    AMIE Client.

    Args:
        site_name (str): Name of the client site.
        api_key (str): API key secret
        amie_url (str): Base URL for the XSEDE AMIE api
        usage_url (str): Base URL for the XSEDE Usage api

    Examples:
        >>> psc_client = amieclient.Client(site_name='PSC', api_key=some_secrets_store['amie_api_key'])

        You can also override the amie_url and usage_url parameters, if you're
        doing local development or testing out a new version.

        >>> psc_alt_base_client = amieclient.Client(site_name='PSC', api_key='test_api_key', amie_url='https://amieclient.xsede.org/v0.20_beta/)

    """
    def __init__(self, site_name, api_key,
                 amie_url='https://amieclient.xsede.org/v0.10/',
                 usage_url='https://usage.xsede.org/api/v1'):
        if not amie_url.endswith('/'):
            self.amie_url = amie_url + '/'
        else:
            self.amie_url = amie_url

        if not usage_url.endswith('/'):
            self.usage_url = usage_url + '/'
        else:
            self.usage_url = usage_url

        self.site_name = site_name

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
            # If we're given anything else, i.e. None or some other single
            # thing, give it back
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
        Given a single transaction record id, fetches the related transaction.

        Args:
            trans_rec_id: The transaction record ID.

        Returns:
            amieclient.Transaction

        """
        url = self.amie_url + 'transactions/{}/{}/packets'.format(self.site_name, trans_rec_id)
        r = self._session.get(url)
        r.raise_for_status()
        return Transaction.from_dict(r.json())

    def get_packet(self, *, packet_rec_id):
        """
        Given a single packet record id, fetches the packet.

        Args:
            packet_rec_id: The transaction record ID.

        Returns:
            amieclient.Packet
        """
        url = self.amie_url + 'packets/{}/{}'.format(self.site_name, packet_rec_id)
        r = self._session.get(url)
        r.raise_for_status()
        return Packet.from_dict(r.json())

    def list_packets(self, *, trans_rec_ids=None, outgoing=None,
                     update_time_start=None, update_time_until=None,
                     states=None, client_states=None, incoming=None):
        """
        Fetches a list of transactions based on the provided search parameters

        Args:
            trans_rec_ids (list): Searches for packets with these transaction record  IDs.
            states (list): Searches for packets with the provided states.
            update_time_start (datetime.Datetime): Searches for packets updated since this time.
            update_time_until (datetime.Datetime): Searches for packets updated before this time.
            states (list): Searches for packets in the provided states.
            client_states (list): Searches for packets in the provided client states.
            incoming (bool): If true, search is limited to incoming packets.

        Returns:
            amieclient.PacketList: a list of packets matching the provided parameters.
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
        url = self.amie_url + 'packets/{}'.format(self.site_name)
        r = self._session.get(url, params=params)
        r.raise_for_status()
        return PacketList.from_dict(r.json())

    def send_packet(self, packet, skip_validation=False):
        """
        Send a packet

        Args:
            packet (amieclient.Packet): The packet to send.

        Returns:
            requests.Response: The response from the AMIE API.
        """
        if not skip_validation:
            packet.validate_data()

        url = self.amie_url + 'packets/{}'.format(self.site_name)
        r = self._session.post(url, json=packet.as_dict)
        r.raise_for_response()
        return r
