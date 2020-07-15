import json

from abc import ABC
from datetime import datetime

from dateutil.parser import parse as dtparse


class PacketInvalidData(Exception):
    """Raised when we try to build a packet with invalid data"""
    pass


class MetaPacket(type):
    """Metaclass for packets.

    Looks at the _data_keys_allowed and _data_keys_required attributes
    when a subclass is declared, then adds class properties that
    stores the information in two separate dictionaries on the object.
    """
    def __new__(cls, name, base, attrs):
        required_data = {}
        allowed_data = {}
        required_fields = attrs.pop('_data_keys_required', [])
        allowed_fields = attrs.pop('_data_keys_allowed', [])
        for k in required_fields:
            required_data[k] = None

            def get_req(obj):
                return obj._required_data[k]

            def set_req(obj, val):
                obj._required_data[k] = val

            def del_req(obj):
                obj._required_data[k] = None
            attrs[k] = property(get_req, set_req, del_req)

        for k in allowed_fields:
            allowed_data[k] = None

            def get_allowed(obj):
                return obj._allowed_data[k]

            def set_allowed(obj, val):
                obj._allowed_data[k] = val

            def del_allowed(obj):
                obj._allowed_data[k] = None
            attrs[k] = property(get_allowed, set_allowed, del_allowed)

        attrs['_required_data'] = required_data
        attrs['_allowed_data'] = allowed_data
        return type.__new__(cls, name, base, attrs)


class Packet(object, metaclass=MetaPacket):
    """
    Generic AMIE packet base class

    Class parameters required:
    _packet_type: the type of the packet (string)
    _expected_reply: expected reply types (list[string] or list[Packet type])
    _data_keys_required: Data keys that are required for this packet type
    _data_keys_allowed: Data keys that are allowed for this packet type

    """
    def __init__(self, packet_id, date=None, additional_data={}, in_reply_to=None):
        self.packet_id = packet_id
        self.additional_data = additional_data
        if not date:
            self.date = datetime.now()

        if hasattr(in_reply_to, 'packet_id'):
            # If we're given a packet object, get the ID
            self.in_reply_to_id = in_reply_to.packet_id
        elif in_reply_to.get('header', {}).get('packet_id'):
            # If we're given a dict-like object, get the ID from the header
            self.in_reply_to_id = in_reply_to['header']['packet_id']
        elif type(in_reply_to) == int:
            # If it's a int, make it a string
            self.in_reply_to_id = "{}".format(in_reply_to)
        else:
            # String or None, at this point
            self.in_reply_to_id = in_reply_to

    @classmethod
    def from_dict(cls, data):
        pkt_type = data['type']
        # Get the subclass that matches this json input
        for subclass in cls.__subclasses__():
            if subclass._packet_type == pkt_type:
                pkt_cls = subclass
                break
        # Raise a NotImplementedError if we can't find a subclass
        else:
            error_str = "No packet type matches provided '{}'".format(pkt_type)
            raise NotImplementedError(error_str)

        obj = pkt_class(packet_id=data['header']['packet_id'])

        for k, v in data['body']:
            if k in obj._required_data or k in obj._allowed_data:
                obj.setattr(k, v)
            else:
                obj.additional_data[k] = v

        # Return an instance of the proper subclass
        return obj

    @classmethod
    def from_json(cls, json_string):
        """
        Generates an instance of an AMIE packet of this type from provided JSON
        """
        data = json.loads(json_string)
        return cls.from_dict(data)

    @property
    def as_dict(self):
        data_body = {}
        # Filter out non-defined items from our data collections
        for d in [self._required_data, self._allowed_data, self.additional_data]:
            for k, v in d.items():
                if v is not None:
                    data_body[k] = v

        header = {
            'packet_id': self.packet_id,
            'date': self.date.isoformat(),
            'type': self.packet_type,
            'expected_reply_list': self._expected_reply
        }
        data_dict = {
            'DATA_TYPE': 'packet',
            'body': data_body,
            'header': header
        }

        return data_dict

    @property
    def json(self):
        """
        The JSON representation of this AMIE packet
        """
        data_dict = self.as_dict
        return json.dumps(data_dict)

    def validate_data(self):
        """
        By default, checks to see that all required data items have a
        defined value
        """
        for k, v in self._required_data.items():
            if v is None:
                raise PacketInvalidData('Missing required data field: "{}"'.format(k))
        return True

    @property
    def packet_type(self):
        return self._packet_type


class PacketList(object):
    """
    A list of packets.
    """
    def __init__(self, length, limit, offset, total, packets=None):
        self.length = length
        self.limit = limit
        self.offset = offset
        self.total = total
        if packets is not None:
            self.packets = packets
        else:
            self.packets = []

    @classmethod
    def from_dict(cls, dict_in):
        pkt_list = cls(
            length=dict_in['length'],
            limit=dict_in['limit'],
            offset=dict_in['offset'],
            total=dict_in['total'],
            packets=[Packet.from_dict(d) for d in dict_in['DATA']]
        )
        return pkt_list

    @classmethod
    def from_json(cls, json_in):
        pkt_list_in = json.loads(json_in)
        return cls.from_dict(pkt_list_in)

    @property
    def as_dict(self):
        data_dict = {
            'DATA_TYPE': 'packet_list',
            'length':  self.legth,
            'limit': self.limit,
            'offset': self.offset,
            'total': self.total,
            'DATA': [pkt.as_dict for pkt in self.packets]
        }
        return data_dict

    @property
    def json(self):
        data_dict = self.as_dict
        return json.dumps(data_dict)



class InformTransactionComplete(Packet):
    _packet_type = 'inform_transaction_complete'
    _expected_reply = []
    _data_keys_required = ['DetailCode', 'Message', 'StatusCode']
    _data_keys_allowed = []
