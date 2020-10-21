import json
from .message import UsageMessage, UsageMessageError
from .record import UsageRecordError


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


class UsageStatusResource:
    def __init__(self, resource_name, loaded_record_count, failed_record_count,
                 errors=[]):
        self.resource_name = resource_name
        self.loaded_record_count = loaded_record_count
        self.failed_record_count = failed_record_count
        self.errors = errors

    @classmethod
    def from_dict(cls, input_dict):
        errors = [UsageMessageError.from_dict(d) for d in input_dict.get('Errors', [])]
        return cls(
            resource_name=input_dict['ResourceName'],
            loaded_record_count=input_dict['LoadedRecordCount'],
            failed_record_count=input_dict['FailedRecordCount'],
            errors=errors
        )

    @classmethod
    def from_json(cls, input_json):
        d = json.loads(input_json)
        return cls.from_dict(d)

    def as_dict(self):
        return {
            'ResourceName': self.resource_name,
            'LoadedRecordCount': self.loaded_record_count,
            'FailedRecordCount': self.failed_record_count,
            'Errors': [e.as_dict() for e in self.errors]
        }

    def json(self):
        return json.dumps(self.as_dict())


class UsageStatus:
    def __init__(self, resources):
        self.resources = resources

    @classmethod
    def from_dict(cls, input_dict):
        return cls(
            resources=[UsageStatusResource.from_dict(d)
                       for d in input_dict.get('Resources', [])]
            )

    @classmethod
    def from_json(cls, input_json):
        d = json.loads(input_json)
        return cls.from_dict(d)

    def as_dict(self):
        return {
            'Resources': [r.as_dict() for r in self.resources]
        }

    def json(self):
        return json.dumps(self.as_dict())
