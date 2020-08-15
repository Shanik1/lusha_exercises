import json


def iterate_records(resource_file):
    """
    Iterate over the records in the resource file.
    Yield the record as a dict.
    """
    with open(resource_file, 'r') as fd:
        row = fd.readline()
        while row:
            yield json.loads(row)
            row = fd.readline()
