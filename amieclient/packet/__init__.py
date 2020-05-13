import json

from abc import ABC
from datetime import datetime


class PacketInvalidData(Exception):
    """Raised when we try to build a packet with invalid data"""
    pass


class Packet(ABC):
    """
    Generic AMIE packet abstract base class

    For now, we just accept any old data. Model it more properly later.
    probably want a hidden parameter that contains a list of valid data keys

    Class parameters required:
    _packet_type: the type of the packet (string)
    _expected_reply: expected reply types (list[string] or list[Packet type])
    _valid_data_keys: Data keys that are valid for this packet type
    """
    def __init__(self, packet_id, packet_data, date=None):
        self._id = packet_id
        self._data = packet_data
        if not date:
            self.date = datetime.now()

    @classmethod
    def from_json(cls, json_string):
        """
        Generates an instance of an AMIE packet of this type from provided JSON
        """
        raise NotImplementedError()

    @property
    def json(self):
        """
        The JSON representation of this AMIE packet
        """
        header = {
            'packet_id': self.id,
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
        # Validate and make sure all keys are members of the valid_keys object
        for x in input_data.keys():
            if x not in self._valid_data_keys:
                raise PacketInvalidData(
                    f'Invalid data key "{x}" for packet type {self.packet_type}'
                )
        self._data = input_data

    @property
    def packet_type(self):
        return self._packet_type

