#!/usr/bin/env python3

"""
This example demonstrates how to create and send along a new packet."""
from amieclient import AMIEClient
from amieclient.packet import RequestProjectCreate

from datetime import datetime, timedelta

# Create the packet
rpc = RequestProjectCreate()
rpc.AllocationType = 'extremely hihg most important'
rpc.GrantNumber = '3'
rpc.PfosNumber = '3'
rpc.PiFirstName = 'Jessica'
rpc.PiLastName = 'Scienceperson'
rpc.PiOrganization = 'PSC'
rpc.PiOrgCode = '12345'
rpc.EndDate = datetime.now() + timedelta(days=90)
rpc.StartDate = datetime.now()
rpc.ResourceList = ['IDK, somthing pretty fast']
rpc.ServiceUnitsAllocated = '3'

# Send the packet
with AMIEClient('psc', 'some_secret_key') as c:
    c.send_packet(rpc)
