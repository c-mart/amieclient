#!/usr/bin/env python3

"""
This example demonstrates how to create and send along a new packet."""
from amieclient import Client
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
rpc.ResourceList = ['IDK, somthing pretty fast', 'maybe with a gpu in it']
rpc.ServiceUnitsAllocated = '3'

# Send the packet
with Client('psc') as c:
    c.send_packet(rpc)
