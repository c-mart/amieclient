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

    def __repr__(self):
        return "<UsageResponse: {s.message}>".format(s=self)


class UsageResponseError(Exception):
    pass


class UsageStatusResource:
    def __init__(self, resource, loaded_record_count, failed_job_count,
                 total_charge, errors=[]):
        self.resource = resource
        self.loaded_record_count = loaded_record_count
        self.failed_job_count = failed_job_count
        self.total_charge = total_charge
        self.errors = errors

    @classmethod
    def from_dict(cls, input_dict):
        errors = [UsageMessageError.from_dict(d) for d in input_dict.get('Errors', [])]
        return cls(
            resource=input_dict['Resource'],
            loaded_record_count=input_dict['LoadedRecordCount'],
            failed_job_count=input_dict['FailedJobCount'],
            total_charge=input_dict['TotalCharge'],
            errors=errors
        )

    @classmethod
    def from_json(cls, input_json):
        d = json.loads(input_json)
        return cls.from_dict(d)

    def as_dict(self):
        return {
            'Resource': self.resource,
            'LoadedRecordCount': self.loaded_record_count,
            'FailedJobCount': self.failed_job_count,
            'TotalCharge': self.total_charge,
            'Errors': [e.as_dict() for e in self.errors]
        }

    def json(self):
        return json.dumps(self.as_dict())

    def __repr__(self):
        return "<UsageStatusResource: {s.resource}, {n} errors>".format(s=self, n=len(self.errors))



class UsageStatus:
    def __init__(self, resources):
        self.resources = resources

    @classmethod
    def from_list(cls, input_list):
        resources = input_list
        return cls(
            resources=[UsageStatusResource.from_dict(d) for d in resources]
            )

    @classmethod
    def from_json(cls, input_list):
        d = json.loads(input_list)
        return cls.from_list(d)

    def as_list(self):
        return [r.as_dict() for r in self.resources]

    def json(self):
        return json.dumps(self.as_list())

    def __repr__(self):
        return "<UsageStatus: {n} resources>".format(n=len(self.resources))


