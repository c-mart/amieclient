from configparser import ConfigParser
from amieclient import AMIEClient

# For more information on the configparser library, please see the python docs:
# https://docs.python.org/3.5/library/configparser.html
config = ConfigParser()
config.read('config.ini')

site_config = config['NCSA']

amie_client = AMIEClient(site_name=site_config['site_name'],
                         amie_url=site_config['amie_url'],
                         api_key=site_config['api_key'])

packets = amie_client.list_packets()

for packet in packets:
  packet_type = packet.packet_type
  packet_rec_id = packet.packet_rec_id
  trans_rec_id = packet.trans_rec_id

  if packet_type == 'request_project_create':
    grant_number    = packet.GrantNumber
    record_id       = packet.RecordID
    project_id      = packet.ProjectID # site project_id (if known)
    resource        = packet.ResourceList[0] # xsede site resource name, eg, delta.ncsa.xsede.org
    request_type    = packet.RequestType
    allocation_type = packet.AllocationType # new, renewal, supplement, transfer, adjustment, advance, extension, ...
    start_date      = packet.StartDate
    end_date        = packet.EndDate
    amount          = packet.ServiceUnitsAllocated
    abstract        = packet.Abstract
    project_title   = packet.ProjectTitle
    board_type      = packet.BoardType
    pfos_num        = packet.PfosNumber

    pi_person_id        = packet.PiPersonID  # site person_id for the PI (if known)
    pi_login            = packet.PiRemoteSiteLogin # login on resource for the PI (if known)
    pi_first_name       = packet.PiFirstName
    pi_middle_name      = packet.PiMiddleName
    pi_last_name        = packet.PiLastName
    pi_organization     = packet.PiOrganization
    pi_department       = packet.PiDepaartment
    pi_email            = packet.PiEmail
    pi_phone_number     = packet.PiBusinessPhoneNumber
    pi_phone_extension  = packet.PiBusinessPhoneExtension
    pi_address1         = packet.PiStreetAddress1
    pi_address2         = packet.PiStreetAddress2
    pi_city             = packet.PiCity
    pi_state            = packet.PiState
    pi_zipcode          = packet.PiZip
    pi_country          = packet.PiCountry
    pi_nsf_status_code  = packet.PiNsfStatusCode
    pi_requested_logins = packet.PiRequestedLoginList
    pi_dn_list          = packet.PiDnList

    # add code to find the PI from the local database (or create the person in the local database)
    # and set pi_person_id, pi_login
    # add code to create the project for the grant_number, if it doesn't exist, or apply the action specified by allocation_type
    # set the project_id to the local id for the project (if it isn't already set from the RPC)
    # NOTE: if the record_id is not null, you should track it (associate it with the packet_rec_id).
    # If a second RPC gets sent with the same record_id, the second RPC should not be processed,
    # and the data from the first RPC sent in the reply NPC

    # construct a NotifyProjectCreate(NPC) packet.
    npc = packet.reply_to()
    npc.ProjectID = project_id           # local project ID
    npc.PiRemoteSiteLogin = pi_login     # local login for the PI
    npc.PiPersonID = pi_person_id        # local person ID for the pi

    # send the NPC
    amie_client.send_packet(npc)

  if packet_type == 'data_project_create':
    person_id  = packet.PersonID
    project_id = packet.ProjectID
    dn_list    = packet.DnList

    # the data_project_create packet has two functions:
    # 1. to let the site know that the project and PI account have been setup in the XDCDB
    # 2. to provide any new DNs for the PI that were added after the RPC was sent

    # construct the InformTransactionComplete(ITC) success packet
    itc = packet.reply_to()
    itc.StatusCode = 'Success'
    itc.DetailCode = '1'
    itc.Message = 'OK'

    # send the ITC
    amie_client.send_packet(itc)