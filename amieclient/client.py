"""AMIE client class"""


class Client(object):
    """
    AMIE Client

    Example:
    psc_client = amieclient.Client('https://amieclient.xsede.org/v0.10/', 'PSC')

    """
    def __init__(self, base_url, site_name):
        self.base_url = base_url
        self.site_name = site_name

    @staticmethod
    def _join_list(things):
        if things is not None and things != []:
            return ','.join(things)
        else:
            return None

    def get_transaction(self, *, transaction_id):
        """
        Given a single transaction id, fetches the related transaction.
        """
        pass

    def transaction_list(self, *,
                         transaction_ids=None, remote_sites=None,
                         originating_sites=None, local_sites=None,
                         update_time_start=None, update_time_until=None,
                         transaction_state=None, incoming=True):
        """
        Fetches a list of transactions based on the provided search parameters
        """
        transaction_ids_str = self._join_list(transaction_ids)
        remote_sites_str = self._join_list(remote_sites)
        originating_sites_str = self._join_list(originating_sites)
        local_sites_str = self._join_list(local_sites)

    def send_packet(self, *, packet, transaction_id):
        pass
