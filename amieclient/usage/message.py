import json

from .record import _type_lookup, UsageRecord, UsageRecordError


class UsageMessageException(Exception):
    """
    Exception for invalid data in a UsageMessage
    """
    pass


class _UsageRecordList:
    def __init__(self, in_list=[]):
        self._list = in_list
        self._record_type = None
        if not self._check_usage_type():
            self._list = []
            raise UsageMessageException('Cannot create a UsageMessage with mixed types')

    def _check_usage_type(self):
        if self._record_type is None and len(self._list) > 0:
            rt = self._list[0].record_type.lower().capitalize()
            if rt not in ['Compute', 'Storage', 'Adjustment']:
                raise UsageMessageException('Invalid usage type {}'
                                            .format(rt))
            self._record_type = rt
        # iterate over list records and check against stored type
        return all([x.record_type == self._record_type for x in self._list])

    def append(self, item):
        if not isinstance(item, UsageRecord):
            raise UsageMessageException("Can't add something that isn't a UsageRecord")
        if (self._record_type is not None and
                item.record_type != self._record_type):
            raise UsageMessageException("Can't add a {} record to a {} message"
                                        .format(item.record_type, self._record_type))
        self._list.append(item)
        if not self._check_usage_type():
            self._list.pop()
            raise UsageMessageException('Cannot create a UsageMessage with mixed types')

    def extend(self, items):
        for item in items:
            self.append(item)

    def __getitem__(self, i):
        return self._list.__getitem__(i)

    def __len__(self):
        return len(self._list)


class UsageMessage:
    def __init__(self, records):
        self.records = _UsageRecordList(records)

    @classmethod
    def from_dict(cls, input_dict):
        """
        Returns a UsageMessage from a provided dictionary
        """
        ut = input_dict['UsageType']
        ur_class = _type_lookup(ut)
        records = [ur_class.from_dict(d) for d in input_dict['Records']]
        return cls(records)

    @classmethod
    def from_json(cls, input_json):
        input_dict = json.loads(input_json)
        return cls.from_dict(input_dict)

    def as_dict(self):
        """
        Returns a dictionary version of this record
        """
        d = {
            'UsageType': self.records._record_type,
            'Records': [r.as_dict() for r in self.records]
        }
        return d

    def json(self):
        """
        Returns a json version of this message
        """
        return json.dumps(self.as_dict())

    def _chunked(self, chunk_size=1000):
        """
        Generator that yields UsageMessages with a maximum of chunk_size number
        UsageRecords. Useful for not going over the 256kb POST limit
        """
        for i in range(0, len(self.records), chunk_size):
            r = self.records[i:i+chunk_size]
            yield self.__class__(r)


class UsageResponse:
    def __init__(self, message, records_failed, ):
        self.message = message
        self.records_failed = records_failed

    @classmethod
    def from_dict(cls, input_dict):
        records = [UsageRecordError.from_dict(d) for d in
                   input_dict.get('ValidationFailedRecords', [])]
        message = input_dict['Message']
        return cls(message=message, records_failed=records)

    @classmethod
    def from_json(cls, input_json):
        d = json.loads(input_json)
        return cls.from_dict(d)

    def as_dict(self):
        d = {
            'Message': self.message,
            'ValidationFailedRecords': [r.as_dict() for r in self.records_failed]
        }
        return d

    def json(self):
        return json.dumps(self.as_dict())


class UsageResponseError(Exception):
    pass
