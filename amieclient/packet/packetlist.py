import json

from .base import Packet


class PacketList(object):
    """
    A list of packets.
    """
    def __init__(self, message=None, packets=None):
        self.message = message
        if packets is not None:
            self.packets = packets
        else:
            self.packets = []

    @classmethod
    def from_dict(cls, dict_in):
        pkt_list = cls(
            message=dict_in.get('message', ''),
            packets=[Packet.from_dict(d) for d in dict_in['result']]
        )
        return pkt_list

    @classmethod
    def from_json(cls, json_in):
        pkt_list_in = json.loads(json_in)
        return cls.from_dict(pkt_list_in)

    @property
    def as_dict(self):
        data_dict = {
            'message': self.message,
            'result': [pkt.as_dict for pkt in self.packets]
        }
        return data_dict

    @property
    def json(self):
        data_dict = self.as_dict
        return json.dumps(data_dict)
