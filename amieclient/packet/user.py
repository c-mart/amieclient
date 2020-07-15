"""
AMIE packets relating to users
"""

from .base import Packet, PacketInvalidData


class NotifyUserModify(Packet):
    _packet_type = 'notify_account_inactivate'
    _expected_reply = ['inform_transaction_complete']
    _data_keys_required = [
        'ActionType',
        'PersonID',
    ]
    _data_keys_allowed = [
        'AcademicDegree',
        'BusinessPhoneComment',
        'BusinessPhoneExtension',
        'BusinessPhoneNumber',
        'City',
        'Country',
        'Department',
        'DnList',
        'Email',
        'Fax',
        'FirstName',
        'HomePhoneComment',
        'HomePhoneExtension',
        'HomePhoneNumber',
        'LastName',
        'MiddleName',
        'Organization',
        'OrgCode',
        'State'
    ]

    def validate_data(self):
        action_type = self._required_data['ActionType']
        if action_type not in ['add', 'delete', 'replace']:
            error_str = 'Invalid action type for notify_user_modify: "{}"'.format(action_type)
            raise PacketInvalidData(error_str)
        return super().validate_data()


class RequestUserModify(Packet):
    _packet_type = 'request_account_inactivate'
    _expected_reply = ['inform_transaction_complete']
    _data_keys_required = [
        'ActionType',
        'PersonID',
    ]
    _data_keys_allowed = [
        'AcademicDegree',
        'BusinessPhoneComment',
        'BusinessPhoneExtension',
        'BusinessPhoneNumber',
        'CitizenshipList',
        'CitizenshipList',
        'City',
        'Country',
        'Department',
        'DnList',
        'Email',
        'Fax',
        'FirstName',
        'HomePhoneComment',
        'HomePhoneExtension',
        'HomePhoneNumber',
        'LastName',
        'MiddleName',
        'NsfStatusCode',
        'Organization',
        'OrgCode',
        'State',
        'StreetAddress',
        'StreetAddress2',
        'Title',
        'Zip',
    ]

    def validate_data(self, input_data):
        action_type = self._required_data['ActionType']
        if action_type not in ['add', 'delete', 'replace']:
            error_str = 'Invalid action type for request_user_modify: "{}"'.format(action_type)
            raise PacketInvalidData(error_str)
        return super().validate_data()
