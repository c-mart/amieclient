amieclient API
==============

The main client itself
----------------------

To communicate with the AMIE REST API, create a client object. You'll need to provide your
site name and your API key.

.. autoclass:: amieclient.client.AMIEClient
   :members:


Packets
-------
The REST version of AMIE focuses more on individual packets more than transactions.
The amieclient library has a generic Packet class, but in general, as a user of the
library, you'll be using the specific child classes for creating and handling packets.

If you need it, the parent Packet class has an internal classmethod, `_find_packet_type`,
that takes the AMIE name of a packet and returns the corresponding amieclient packet
class.

.. autoclass:: amieclient.packet.base.Packet
   :members:


Account packets
,,,,,,,,,,,,,,,

.. automodule:: amieclient.packet.account
  :members:

Project packets
,,,,,,,,,,,,,,,

.. automodule:: amieclient.packet.project
  :members:

Person packets
,,,,,,,,,,,,,,

.. automodule:: amieclient.packet.person
  :members:

User packets
,,,,,,,,,,,,

.. automodule:: amieclient.packet.user
  :members:

Informational packets
,,,,,,,,,,,,,,,,,,,,,

.. automodule:: amieclient.packet.inform
  :members:

