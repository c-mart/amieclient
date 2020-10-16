import json
from collections import namedtuple
from abc import ABC, abstractmethod

ComputeUsageAttributes = namedtuple('ComputeUsageAttributes',
                                    ['node_count', 'cpu_core_count',
                                     'job_name', 'memory', 'queue'],
                                    # for named tuples, defaults start with the
                                    # right, so 4 Nones here means that the
                                    # last 4 fields above have a default value
                                    # of None
                                    defaults=[None] * 4
                                    )

StorageUsageAttributes = namedtuple('StorageUsageAttributes',
                                    ['BytesRead', 'BytesStored',
                                     'BytesWritten', 'CollectionInterval',
                                     'FileCount', 'FilesRead', 'FilesWritten',
                                     'MediaType', 'SystemCopies',
                                     'UserCopies'],
                                    defaults=[None] * 10
                                    )


class UsageRecord(ABC):
    """
    Abstract base class for a usage record
    """
    @abstractmethod
    @classmethod
    def from_dict(cls, input_dict):
        pass

    @abstractmethod
    def as_dict(self):
        pass

    @classmethod
    def from_json(cls, input_json):
        """
        Returns an UsageRecord from a provided JSON string
        """
        input_dict = json.loads(input_json)
        return cls.from_dict(input_dict)

    @abstractmethod
    def json(self):
        """
        Returns a json version of this record
        """
        return json.dumps(self.as_dict())


class ComputeUsageRecord(UsageRecord):
    """
    A ComputeUsageRecord. A Record of Compute Usage.

    (TODO: a better description)
    """
    record_type = 'compute'

    def __init__(self, *,
                 parent_record_id=None, queue=None, cpu_core_count=None,
                 job_name=None, memory=None, charge, end_time,
                 local_project_id, local_record_id, resource, start_time,
                 submit_time, username, node_count):
        """
        Creates a new compute usage record.

        Args:
            parent_record_id (str): Job ID of parent job if this record is a sub job.  Typically a slurm job id
            queue (str): Scheduler queue name the job was submitted to
            cpu_core_count (str): Number of cores used by the job
            job_name (str): Job name
            memory (str): ??? Max memory for a node?  Bytes?
            charge (str): The amount of allocation units that should be deducted from the project allocation for this job
            end_time (str): Job End Time
            local_project_id (str): The Site Project ID for the job.  This must match the ProjectID provided by the site for the project with AMIE
            local_record_id (str): Site Job ID.  Typically a slurm job id
            resource (str): Resource the job ran on.  Must match the resource name used in AMIE
            start_time (str): Start Time of the job
            submit_time (str): Start Time of the job
            username (str): The local username of the user who ran the job.  Must match the username used in AMIE
            node_count (str): Number of nodes the job ran on

        Returns:
            ComputeUsageRecord
        """

        self.attributes = ComputeUsageAttributes(node_count, cpu_core_count,
                                                 job_name, memory, queue)

        self.parent_record_id = parent_record_id,
        self.charge = charge
        self.end_time = end_time
        self.local_project_id = local_project_id
        self.local_record_id = local_record_id
        self.resource = resource
        self.start_time = start_time
        self.submit_time = submit_time
        self.username = username

    @classmethod
    def from_dict(cls, input_dict):
        """
        Returns a ComputeUsageRecord from a provided dictionary
        """

        return cls(
            username=input_dict['Username'],
            local_project_id=input_dict['LocalProjectID'],
            local_record_id=input_dict['LocalRecordID'],
            resource=input_dict['Resource'],
            submit_time=input_dict['SubmitTime'],
            start_time=input_dict['StartTime'],
            end_time=input_dict['EndTime'],
            charge=input_dict['Charge'],
            node_count=input_dict['Attributes']['NodeCount'],
            cpu_core_count=input_dict['Attributes'].get('CpuCoreCount'),
            job_name=input_dict['Attributes'].get('JobName'),
            memory=input_dict['Attributes'].get('Memory'),
            queue=input_dict['Attributes'].get('Queue'),
            parent_record_id=input_dict.get('ParentRecordID'),
        )

    def as_dict(self):
        """
        Returns a dictionary version of this record
        """

        # Get the attributes, skip over anything not specified
        attributes = {}
        for k, v in self.attributes._asdict().items():
            if v is not None:
                attributes[k] = v

        d = {
            'Username': self.username,
            'LocalProjectID': self.local_project_id,
            'LocalRecordID': self.local_record_id,
            'Resource': self.resource,
            'SubmitTime': self.submit_time,
            'StartTime': self.start_time,
            'EndTime': self.end_time,
            'Charge': self.charge,
            'Attributes': attributes
        }

        if self.parent_record_id is not None:
            d['ParentRecordID'] = self.parent_record_id

        return d


class StorageUsageRecord(UsageRecord):
    record_type = 'storage'
    """
    A usage record for storage usage.

    Args:
        charge (str): The amount of allocation units that should be deducted
                      from the project allocation for this job.  For storage
                      this is usually gigabytes stored
        collection_time (str): Time the storage use was collected
        local_project_id (str): The Site Project ID for the job.  This must
                                match the ProjectID provided by the site for
                                the project with AMIE
        local_record_id (str): Site Record ID.  Use to make the record
                               identifiable to you locally
        resource (str): Resource the job ran on.  Must match the resource name
                        used in AMIE
        username (str): The local username of the user who ran the job. Must
                        match the username used in AMIE
        bytes_read (str): Number of bytes Read
        bytes_stored (str): Number of bytes stored
        bytes_written (str): Number of bytes written
        collection_interval (str): How often the storage use will be calculated
                                   in days
        file_count (str): Number of files stored
        files_read (str): Number of files read
        files_written (str): Number of files written
        media_type (str): Type of the storage (Tape, Disk, SSD, etc)
        system_copies (str): Number of copies of the data the system keeps
        user_copies (str): Number of copies of the data the user has chosen
                           to keep
    """
    def __init__(self, charge, collection_time, local_project_id,
                 local_record_id, resource, username,
                 bytes_read=None, bytes_stored=None, bytes_written=None,
                 collection_interval=None, file_count=None, files_read=None,
                 files_written=None, media_type=None, system_copies=None,
                 user_copies=None):
        self.attributes = StorageUsageAttributes(bytes_read, bytes_stored,
                                                 bytes_written, collection_interval,
                                                 file_count, files_read,
                                                 files_written, media_type,
                                                 system_copies, user_copies)
        self.charge = charge
        self.collection_time = collection_time
        self.local_project_id = local_project_id
        self.local_record_id = local_record_id
        self.resource = resource
        self.username = username

    @classmethod
    def from_dict(cls, input_dict):
        attributes = input_dict.get('Attributes', {})
        return cls(
            charge=input_dict['Charge'],
            collection_time=input_dict['CollectionTime'],
            local_project_id=input_dict['LocalProjectID'],
            local_record_id=input_dict['LocalRecordID'],
            record=input_dict['Resource'],
            username=input_dict['Username'],
            bytes_read=attributes.get('BytesRead'),
            bytes_stored=attributes.get('BytesStored'),
            bytes_writen=attributes.get('BytesWritten'),
            collection_interval=attributes.get('CollectionInterval'),
            file_count=attributes.get('FileCount'),
            files_read=attributes.get('FilesRead'),
            files_written=attributes.get('FilesWritten'),
            media_type=attributes.get('MediaType'),
            system_copies=attributes.get('SystemCopies'),
            user_copies=attributes.get('UserCopies'),
        )

    def as_dict(self):
        # Get the attributes, skip over anything not specified
        attributes = {}
        for k, v in self.attributes._asdict().items():
            if v is not None:
                attributes[k] = v

        d = {
            'Charge': self.charge,
            'CollectionTime': self.submit_time,
            'LocalProjectID': self.local_project_id,
            'LocalRecordID': self.local_record_id,
            'Resource': self.resource,
            'Username': self.username,
            'Attributes': attributes
        }

        return d


class AdjustmentUsageRecord(UsageRecord):
    """
    Usage record for an Adjustment
    Args:
        adjustment_type (str): Which type of allocation adjustment is this?
                               Valid values are 'credit', 'refund',
                               'storage-credit', 'debit', 'reservation',
                               'storage-debit'
        charge (str): The amount of allocation units that should be deducted
                      from the project allocation for this job.  For storage
                      this is usually gigabytes stored.
        start_time (str): Time for which this adjustment should be applied.
                          For example a the time for a job refund should be
                          the same as the job submit time to ensure the correct
                          allocation is credited.
        local_project_id (str): The Site Project ID for the job. This must
                                match the ProjectID provided by the site for
                                the project with.
        local_record_id (str): AMIE Site Record ID. Use to make this record
                               identifiable to you locally. Must be unique
                               for the resource.
        resource (str): Resource the job ran on.  Must match the resource name
                        used in AMIE
        username (str): The local username of the user who ran the job.  Must
                        match the username used in AMIE
        comment (str): Comment to explain reason for adjustment
    """

    VALID_ADJUSTMENT_TYPES = ['credit', 'refund', 'storage-credit', 'debit',
                              'reservation', 'storage-debit']

    def __init__(self, adjustment_type, charge, start_time, local_project_id,
                 local_record_id, resource, username, comment=None):
        at = adjustment_type.lower()
        if at not in self.VALID_ADJUSTMENT_TYPES:
            raise ValueError('Adjustment type "{}" invalid, must be one of {}'
                             .format(at, self.VALID_ADJUSTMENT_TYPES))
        self.adjustment_type = at
        self.charge = charge
        self.start_time = start_time
        self.local_project_id = local_project_id
        self.local_record_id = local_record_id
        self.resource = resource
        self.username = username
        self.comment = comment

    @classmethod
    def from_dict(cls, input_dict):
        return cls(
            adjustment_type=input_dict['AdjustmentType'],
            charge=input_dict['Charge'],
            start_time=input_dict['StartTime'],
            local_project_id=input_dict['LocalProjectID'],
            local_record_id=input_dict['LocalRecordID'],
            resource=input_dict['Resource'],
            username=input_dict['Username'],
            comment=input_dict.get('Comment')
        )

    def as_dict(self):
        d = {
            'AdjustmentType': self.adjustment_type,
            'Charge': self.charge,
            'StartTime': self.start_time,
            'LocalProjectID': self.local_project_id,
            'LocalRecordID': self.local_record_id,
            'Resource': self.resource,
            'Username': self.username
        }
        if self.comment is not None:
            d['Comment'] = self.comment

        return d


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
                                        .format(item._record_type, self._record_type))
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
        if ut == 'Compute':
            ur_class = ComputeUsageRecord
        elif ut == 'Storage':
            ur_class = StorageUsageRecord
        elif ut == 'Adjustment':
            ur_class = AdjustmentUsageRecord
        else:
            raise UsageMessageException('Invalid usage type {}'.format(ut))
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

    def as_json(self):
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

