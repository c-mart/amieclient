import json

from abc import ABC
from datetime import datetime

from dateutil.parser import parse as dtparse


class PacketInvalidData(Exception):
    """Raised when we try to build a packet with invalid data"""
    pass


class Packet(ABC):
    """
    Generic AMIE packet abstract base class

    Class parameters required:
    _packet_type: the type of the packet (string)
    _expected_reply: expected reply types (list[string] or list[Packet type])
    _data_keys_required: Data keys that are required for this packet type
    _data_keys_allowed: Data keys that are allowed for this packet type
    """
    def __init__(self, packet_id, packet_data, date=None):
        self.packet_id = packet_id
        self.data = packet_data
        if not date:
            self.date = datetime.now()

    @classmethod
    def from_json(cls, json_string):
        """
        Generates an instance of an AMIE packet of this type from provided JSON
        """
        data = json.loads(json_string)
        pkt_type = data['header']['type']
        # Get the subclass that matches this json input
        for subclass in cls.__subclasses__():
            if subclass.packet_type == pkt_type:
                pkt_cls = subclass
                break
        # Raise a NotImplementedError if we can't find a subclass
        else:
            raise NotImplementedError(f"No packet type matches provided '{pkt_type}'")

        # Return an instance of the proper subclass
        return pkt_cls(packet_id=data['header']['packet_id'],
                       packet_data=data['body'],
                       date=dtparse(data['header']['date']))

    @property
    def json(self):
        """
        The JSON representation of this AMIE packet
        """
        header = {
            'packet_id': self.packet_id,
            'date': self.date.isoformat(),
            'type': self.packet_type,
            'expected_reply_list': self._expected_reply
        }
        data_dict = {
            'DATA_TYPE': 'packet',
            'body': self.data,
            'header': header
        }
        return json.dumps(data_dict)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, input_data):
        # Make sure all keys are members of the valid_keys object
        for x in input_data.keys():
            if x not in (self._data_keys_allowed + self._data_keys_required):
                raise PacketInvalidData(f'Invalid data key "{x}" for packet type {self.packet_type}')
        for x in self._data_keys_required:
            if x not in input_data.keys():
                raise PacketInvalidData(f'Missing required data field: {x}')

        self._data = input_data

    @property
    def packet_type(self):
        return self._packet_type
