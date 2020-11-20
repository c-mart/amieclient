from math import ceil, floor

import requests

from .packet import PacketList
from .packet.base import Packet
from .transaction import Transaction
from .usage import (UsageMessage, UsageRecord, UsageResponse, UsageResponseError,
                    UsageStatus)


"""AMIE client and Usage Client classes"""

class AMIERequestError(requests.RequestException):
    pass


class AMIEClient(object):
    """
    AMIE Client.

    Args:
        site_name (str): Name of the client site.
        api_key (str): API key secret
        amie_url (str): Base URL for the XSEDE AMIE api

    Examples:
        >>> psc_client = amieclient.AMIEClient(site_name='PSC', api_key=some_secrets_store['amie_api_key'])

        You can also override the amie_url and usage_url parameters, if you're
        doing local development or testing out a new version.

        >>> psc_alt_base_client = amieclient.AMIEClient(site_name='PSC', api_key='test_api_key', amie_url='https://amieclient.xsede.org/v0.20_beta/)

    """
    def __init__(self, site_name, api_key,
                 amie_url='https://amieclient.xsede.org/v0.10/'):
        if not amie_url.endswith('/'):
            self.amie_url = amie_url + '/'
        else:
            self.amie_url = amie_url

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
        response = r.json()
        if r.status_code > 200:
            message = response.get('message', 'Server did not provide an error message')
            raise AMIERequestError(message, response=r)
        return Transaction.from_dict(response)

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
        response = r.json()
        if r.status_code > 200:
            message = response.get('message', 'Server did not provide an error message')
            raise AMIERequestError(message, response=r)
        return Packet.from_dict(response)

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
        response = r.json()
        if r.status_code > 200:
            message = response.get('message', 'Server did not provide an error message')
            raise AMIERequestError(message, response=r)
        return PacketList.from_dict(response)

    def send_packet(self, packet, skip_validation=False):
        """
        Send a packet

        Args:
            packet (amieclient.Packet): The packet to send.

        Returns:
            requests.Response: The response from the AMIE API.
        """
        if not skip_validation:
            packet.validate_data(raise_on_invalid=True)

        url = self.amie_url + 'packets/{}'.format(self.site_name)
        r = self._session.post(url, json=packet.as_dict())
        response = r.json()
        if r.status_code > 200:
            message = response.get('message', 'Server did not provide an error message')
            raise AMIERequestError(message, response=r)
        return r


class UsageClient:
    """
    AMIE Usage Client.

    Args:
        site_name (str): Name of the client site.
        api_key (str): API key secret
        usage_url (str): Base URL for the XSEDE Usage api

    Examples:
        >>> psc_client = amieclient.UsageClient(site_name='PSC', api_key=some_secrets_store['amie_api_key'])

        You can also override the amie_url and usage_url parameters, if you're
        doing local development or testing out a new version.

        >>> psc_alt_base_client = amieclient.UsageClient(site_name='PSC', api_key='test_api_key', usage_url='https://amieclient.xsede.org/v0.20_beta/)

    """
    def __init__(self, site_name, api_key,
                 usage_url='https://usage.xsede.org/api/v1'):

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

    def send_usage(self, usage_packets):
        """
        Sends a usage update to the Usage API host. This function accepts
        individual UsageMessages, lists of UsageRecords, or even a single
        UsageRecord. Returns a list of UsageResponses

        The API currently has a request size limit of 1024KiB. We get
        ample room for overhead that may be added by intermediate layers
        (reverse proxies, etc) by capping the size of the request we send
        to 768KiB. This happens automatically, no need to chunk your usage
        packets yourself. But this potential chunking means that we may get
        more than one response, so for the sake of consistency this method
        will return a list of responses.

        Args:
            usage_packets (UsageMessage, [UsageRecord], UsageRecord):
                A UsageMessage object, list of UsageRecords, or a single
                UsageRecord to send.
        Returns:
            list of responses
        """
        if isinstance(usage_packets, UsageRecord):
            pkt_list = UsageMessage([usage_packets])
        elif isinstance(usage_packets, list):
            pkt_list = UsageMessage(usage_packets)
        elif isinstance(usage_packets, UsageMessage):
            pkt_list = usage_packets
        url = self.usage_url + '/usage'

        # prepare the request
        req = requests.Request('POST',  url, json=pkt_list.as_dict())
        prepped_req = self._session.prepare_request(req)
        # Get the size of the content
        content_length = int(prepped_req.headers.get('Content-Length'))

        # Cap content_length at 786432 bytes
        if content_length >= 786432:
            # Get the safe number of safe chunks:
            number_of_chunks = ceil(content_length / 786432)
            # Get the size of those chunks
            chunk_size = floor(len(pkt_list) / number_of_chunks)
            results = list()
            for chunk in pkt_list._chunked(chunk_size=chunk_size):
                # Send each chunk
                r = self.send_usage(chunk)
                results.extend(r)
            return results

        r = self._session.send(prepped_req)
        if r.status_code == 200:
            resp = UsageResponse.from_dict(r.json())
        elif r.status_code == 400:
            # Get the message if we're given one; otherwise
            msg = r.json().get('error', 'Bad Request, but error not specified by server')
            raise UsageResponseError(msg)
        else:
            r.raise_for_status()
        return [resp]

    def usage_summary(self):
        """
        Gets a usage summary

        Not implemented yet
        """
        pass

    def usage_status(self, from_time=None, to_time=None):
        """
        Gets the status of records processed from the queue in the provided interval.


        Args:
            from_date (Datetime): Start date and time
            to_date (Datetime): End date and time

        """
        from_iso = from_time.isoformat() if from_time is not None else None
        to_iso = to_time.isoformat() if to_time is not None else None
        p = {'FromTime': from_iso, 'ToTime': to_iso}

        url = self.usage_url + 'usage/status'
        r = self._session.get(url, params=p)
        if r.status_code == 200:
            resp = UsageResponse.from_dict(r.json())
        elif r.status_code == 400:
            # Get the message if we're given one; otherwise
            msg = r.json().get('error', 'Bad Request, but error not specified by server')
            raise UsageResponseError(msg)
        else:
            r.raise_for_status()
        return UsageStatus.from_dict(resp)
