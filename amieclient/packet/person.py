"""
AMIE packets relating to persons
"""

from . import Packet, PacketInvalidData


class NotifyPersonDuplicate(Packet):
    _packet_type = 'notify_person_duplicate'
    _expected_reply = ['inform_transaction_complete']
    _data_keys_required = []
    _data_keys_allowed = ['GlobalID1', 'GlobalID2', 'PersonID1', 'PersonID2']

    def _validate_data(self, input_data):
        """
        Validates that there are no unallowed tags, and additionally checks to
        make sure that either a global ID or person ID is provided for
        the two duplicate people
        """
        validated_data = super()._validate_data(input_data)
        if ('GlobalID1' not in validated_data) or ('PersonID1' not in validated_data):
            raise PacketInvalidData("Must provide either GlobalID1 or PersonID1")
        if ('GlobalID2' not in validated_data) or ('PersonID2' not in validated_data):
            raise PacketInvalidData("Must provide either GlobalID2 or PersonID2")
        return validated_data


class NotifyPersonIDs(Packet):
    _packet_type = 'notify_person_ids'
    _expected_reply = ['inform_transaction_complete']
    _data_keys_required = ['PersonID', 'PrimaryPersonID']
    _data_keys_allowed = ['PersonIDList', 'RemoveResourceList', 'ResourceLogin']


class RequestPersonMerge(Packet):
    _packet_type = 'request_person_merge'
    _expected_reply = ['inform_transaction_complete']
    _data_keys_required = ['KeepGlobalID', 'KeepPersonID', 'DeleteGlobalID',
                           'DeletePersonID']
    _data_keys_allowed = ['DeletePortalLogin', 'KeepPortalLogin']
