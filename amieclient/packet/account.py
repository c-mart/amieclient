"""
AMIE packets relating to accounts
"""

from . import Packet


class DataAccountCreate(Packet):
    _packet_type = 'data_account_create'
    _expected_reply = ['inform_transaction_complete']
    _data_keys_required = ['PersonID', 'ProjectID']
    _data_keys_allowed = ['DnList']


class NotifyAccountCreate(Packet):
    _packet_type = 'notify_account_create'
    _expected_reply = ['data_account_create']
    _data_keys_required = [
        'AccountActivityTime',
        'AcademicDegree',
        'ProjectID',
        'ResourceList',
        'UserFirstName',
        'UserLastName',
        'UserOrganization',
        'UserOrgCode',
        'UserPersonID',
        'UserRemoteSiteLogin',
    ]
    _data_keys_allowed = [
        'NsfStatusCode',
        'RoleList',
        'UserBusinessPhoneExtension',
        'UserBusinessPhoneNumber',
        'UserCity',
        'UserCountry',
        'UserDepartment',
        'UserDnList',
        'UserDnList',
        'UserEmail',
        'UserFax',
        'UserGlobalID',
        'UserHomePhoneExtension',
        'UserHomePhoneNumber',
        'UserMiddleName',
        'UserPasswordAccessEnable',
        'UserPosition',
        'UserRequestedLoginList',
        'UserState',
        'UserStreetAddress',
        'UserStreetAddress2',
        'UserTitle',
    ]


class NotifyAccountInactivate(Packet):
    _packet_type = 'notify_account_inactivate'
    _expected_reply = ['inform_transaction_complete']
    _data_keys_required = ['PersonID', 'ProjectID', 'ResourceList']
    _data_keys_allowed = ['Comment']


class NotifyAccountReactivate(Packet):
    _packet_type = 'notify_account_reactivate'
    _expected_reply = ['inform_transaction_complete']
    _data_keys_required = ['PersonID', 'ProjectID', 'ResourceList']
    _data_keys_allowed = ['Comment']


class RequestAccountCreate(Packet):
    _packet_type = 'request_account_create'
    _expected_reply = ['notify_account_create']
    _data_keys_required = [
        'GrantNumber',
        'ResourceList',
        'UserFirstName',
        'UserLastName',
        'UserOrganization',
        'UserOrgCode',
    ]
    _data_keys_allowed = [
        'RoleList',
        'UserGlobalID',
        'AllocatedResource',
        'NsfStatusCode',
        'ProjectID',
        'SitePersonId',
        'AcademicDegree',
        'CitizenshipList',
        'UserBusinessPhoneComment',
        'UserBusinessPhoneExtension',
        'UserBusinessPhoneNumber',
        'UserCity',
        'UserCountry',
        'UserDepartment',
        'UserDnList',
        'UserEmail',
        'UserFax',
        'UserHomePhoneComment',
        'UserHomePhoneExtension',
        'UserHomePhoneNumber',
        'UserMiddleName',
        'UserPasswordAccessEnable',
        'UserPersonID',
        'UserRequestedLoginList',
        'UserState',
        'UserStreetAddress',
        'UserStreetAddress2',
        'UserTitle',
        'UserZip',
    ]


class RequestAccountInactivate(Packet):
    _packet_type = 'request_account_inactivate'
    _expected_reply = ['notify_account_inactivate']
    _data_keys_required = ['PersonID', 'ProjectID', 'ResourceList']
    _data_keys_allowed = ['Comment']


class RequestAccountReactivate(Packet):
    _packet_type = 'request_account_reactivate'
    _expected_reply = ['notify_account_reactivate']
    _data_keys_required = ['PersonID', 'ProjectID', 'ResourceList']
    _data_keys_allowed = ['Comment']