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
