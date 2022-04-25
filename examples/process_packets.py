from configparser import ConfigParser
from amieclient import AMIEClient

# NOTE: functionality that is required to be implemented by Service Providers 
# are marked with comments that begin with the prefix SP:

# For more information on the configparser library, please see the python docs:
# https://docs.python.org/3.5/library/configparser.html
config = ConfigParser()
config.read('config.ini')

site_config = config['NCSA']

amie_client = AMIEClient(site_name=site_config['site_name'],
                         amie_url=site_config['amie_url'],
                         api_key=site_config['api_key'])

packets = amie_client.list_packets().packets

for packet in packets:
    packet_type = packet.packet_type
    packet_rec_id = packet.packet_rec_id
    trans_rec_id = packet.trans_rec_id

    if packet_type == 'request_project_create':
        grant_number = packet.GrantNumber
        record_id = packet.RecordID
        project_id = packet.ProjectID  # site project_id (if known)
        resource = packet.ResourceList[0]  # xsede site resource name, eg, delta.ncsa.xsede.org
        request_type = packet.RequestType
        allocation_type = packet.AllocationType  # new, renewal, supplement, transfer, adjustment, advance, extension, ...
        start_date = packet.StartDate
        end_date = packet.EndDate
        amount = packet.ServiceUnitsAllocated
        abstract = packet.Abstract
        project_title = packet.ProjectTitle
        board_type = packet.BoardType
        pfos_num = packet.PfosNumber

        pi_person_id = packet.PiPersonID         # site person_id for the PI (if known)
        pi_first_name = packet.PiFirstName
        pi_middle_name = packet.PiMiddleName
        pi_last_name = packet.PiLastName
        pi_organization = packet.PiOrganization
        pi_department = packet.PiDepartment
        pi_email = packet.PiEmail
        pi_phone_number = packet.PiBusinessPhoneNumber
        pi_phone_extension = packet.PiBusinessPhoneExtension
        pi_address1 = packet.PiStreetAddress
        pi_address2 = packet.PiStreetAddress2
        pi_city = packet.PiCity
        pi_state = packet.PiState
        pi_zipcode = packet.PiZip
        pi_country = packet.PiCountry
        pi_nsf_status_code = packet.NsfStatusCode
        pi_requested_logins = packet.PiRequestedLoginList
        pi_dn_list = packet.PiDnList

        # SP: 
        # - add code to find the PI from the local database (or create the person in the local database)
        #   and set pi_person_id, pi_login
        # - add code to create the project for the grant_number (if project doesn't exist), or apply the action specified by allocation_type
        # - set the project_id to the local id for the project (if it isn't already set from the RPC)
        # - set the project state to active (if it is inactive), as the XDCDB will not send RPCs for inactive projects
        #
        # NOTE: if the record_id is not null, you should track it (associate it with the packet_rec_id).
        # If a second RPC gets sent with the same record_id, the second RPC should not be processed,
        # but the data from the first RPC sent in the reply NPC

        # construct a NotifyProjectCreate(NPC) packet.
        npc = packet.reply_packet()
        npc.ProjectID = project_id           # local project ID
        npc.PiPersonID = pi_person_id        # local person ID for the pi

        # send the NPC
        amie_client.send_packet(npc)

    if packet_type == 'data_project_create':
        person_id = packet.PersonID
        project_id = packet.ProjectID
        dn_list = packet.DnList

        # the data_project_create(DPC) packet has two functions:
        # 1. to let the site know that the project and PI account have been setup in the XDCDB
        # 2. to provide any new DNs for the PI that were added after the RPC was sent
        # NOTE: a DPC does *not* have the resource. You have to get the resource from the RPC for the trans_rec_id

        # construct the InformTransactionComplete(ITC) success packet
        itc = packet.reply_packet()
        itc.StatusCode = 'Success'
        itc.DetailCode = '1'
        itc.Message = 'OK'

        # send the ITC
        amie_client.send_packet(itc)

    if packet_type == 'request_account_create':
        grant_number = packet.GrantNumber
        project_id = packet.ProjectID  # site project_id
        resource = packet.ResourceList[0]  # xsede site resource name, eg, delta.ncsa.xsede.org

        user_person_id = packet.UserPersonID         # site person_id for the User (if known)
        user_login = packet.UserRemoteSiteLogin  # login on resource for the User (if known)
        user_first_name = packet.UserFirstName
        user_middle_name = packet.UserMiddleName
        user_last_name = packet.UserLastName
        user_organization = packet.UserOrganization
        user_department = packet.UserDepartment
        user_email = packet.UserEmail
        user_phone_number = packet.UserBusinessPhoneNumber
        user_phone_extension = packet.UserBusinessPhoneExtension
        user_address1 = packet.UserStreetAddress
        user_address2 = packet.UserStreetAddress2
        user_city = packet.UserCity
        user_state = packet.UserState
        user_zipcode = packet.UserZip
        user_country = packet.UserCountry
        user_nsf_status_code = packet.UserNsfStatusCode
        user_requested_logins = packet.UserRequestedLoginList
        user_dn_list = packet.UserDnList

        # SP: add code to find the User from the local database (or create the person in the local database)
        # then add an account for the User on the specified project (project_id) on the resource
        # RACs are also used to reactivate accounts, so if the account already exists, just set it active

        # construct a NotifyAccountCreate(NAC) packet.
        nac = packet.reply_packet()
        nac.ProjectID = project_id               # local project ID
        nac.UserRemoteSiteLogin = user_login     # local login for the User on the resource
        nac.UserPersonID = user_person_id        # local person ID for the User

        # send the NAC
        amie_client.send_packet(nac)

    if packet_type == 'data_account_create':
        person_id = packet.PersonID
        project_id = packet.ProjectID
        dn_list = packet.DnList

        # the data_account_create(DAC) packet has two functions:
        # 1. to let the site know that the User account on the project has been setup in the XDCDB
        # 2. to provide any new DNs for the User that were added after the RAC was sent
        # NOTE: a DAC does *not* have the resource. You have to get the resource from the RAC for the trans_rec_id

        # construct the InformTransactionComplete(ITC) success packet
        itc = packet.reply_packet()
        itc.StatusCode = 'Success'
        itc.DetailCode = '1'
        itc.Message = 'OK'

        # send the ITC
        amie_client.send_packet(itc)

    if packet_type == 'request_user_modify':
        person_id = packet.PersonID
        if packet.Actiontype == 'delete':
            inactive_dn_list = packet.DnList
            # SP: inactivate the specified DNs for the user
        else:
            active_dn_list = packet.DnList
            first_name = packet.FirstName
            middle_name = packet.MiddleName
            last_name = packet.LastName
            organization = packet.Organization
            department = packet.Department
            email = packet.Email
            bus_phone_number = packet.BusinessPhoneNumber
            bus_phone_extension = packet.BusinessPhoneExtension
            home_phone_number = packet.HomePhoneNumber
            home_phone_extension = packet.HomePhoneExtension
            fax = packet.Fax
            address1 = packet.StreetAddress
            address2 = packet.StreetAddress2
            city = packet.City
            state = packet.State
            zipcode = packet.Zip
            country = packet.Country
            nsf_status_code = packet.NsfStatusCode

            # SP: update the User info and DNs

        # construct the InformTransactionComplete(ITC) success packet
        itc = packet.reply_packet()
        itc.StatusCode = 'Success'
        itc.DetailCode = '1'
        itc.Message = 'OK'

        # send the ITC
        amie_client.send_packet(itc)

    if packet_type == 'request_person_merge':
        keep_person_id = packet.KeepPersonID
        delete_person_id = packet.DeletePersonID

        # SP: merge delete_person_id into keep_person_id and remove delete_person_id from local accounting system

        # construct the InformTransactionComplete(ITC) success packet
        itc = packet.reply_packet()
        itc.StatusCode = 'Success'
        itc.DetailCode = '1'
        itc.Message = 'OK'

        # send the ITC
        amie_client.send_packet(itc)



    if packet_type == 'request_project_inactivate':
        resource = packet.ResourceList[0]
        project_id = packet.ProjectID

        # SP: inactivate the project and all accounts on the project

        npi = packet.reply_packet()
        amie_client.send_packet(npi)

    if packet_type == 'request_account_inactivate':
        resource = packet.ResourceList[0]
        project_id = packet.ProjectID
        person_id = packet.PersonID

        # SP:  inactivate the account on the project

        nai = packet.reply_packet()
        amie_client.send_packet(nai)

    if packet_type == 'request_project_reactivate':
        resource = packet.ResourceList[0]
        project_id = packet.ProjectID
        pi_person_id = packet.PersonID

        # SP: reactivate the project and the PI account on the project (but no other accounts)

        npr = packet.reply_packet()
        amie_client.send_packet(npr)

    if packet_type == 'inform_transaction_complete':
        # construct the InformTransactionComplete(ITC) success packet
        itc = packet.reply_packet()
        itc.StatusCode = 'Success'
        itc.DetailCode = '1'
        itc.Message = 'OK'

        # send the ITC
        amie_client.send_packet(itc)
