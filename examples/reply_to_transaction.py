#!/usr/bin/env python3

"""
This example demonstrates how to respond to a transaction in progress
For this example, Transaction 12345 has an incoming RequestProjectCreate
packet, which we will respond to with a NotifyProjectCreate.
"""
from amieclient import Client

# Create the client
psc_client = Client(site_name='PSC')

# Get the transaction you want
transaction = psc_client.get_transaction(transaction_id='12345')

# Get the most recent packet (? this may need a more robust method)
project_creation_request = transaction.packets[-1]

# The assumption here is that rpc is a RequestProjectCreate.
# Here, you'd go ahead and do what you need to create the project.

# SomeInternalSystem.create_project()

# Once that's done, send a NotifyProjectCreate packet.
# If nothing needs to be changed from the RequestProjectCreate packet,
# you can use the packet's reply_to() method. This will create a packet that
# automatically has the proper type and a reference to the preceeding packet.
# The AMIE service will extrapolate the needed information from the
# RequestProjectCreate packet.

project_created = project_creation_request.reply_to()

psc_client.send_packet(project_created)

# You can also create a client as a context manager, if you want.
# This complete example would look like
with Client('psc') as client_too:
    transaction = client_too.get_transaction(transaction_id='12345')
    project_creation_request = transaction.packets[-1]
    # Do something...
    project_created = project_creation_request.reply_to()
    client_too.send_packet(project_created)
