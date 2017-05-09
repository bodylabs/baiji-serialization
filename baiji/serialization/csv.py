from __future__ import absolute_import

__all__ = ['load', 'dump', 'dumps', 'EXTENSION']

EXTENSION = '.csv'


def load(f, *args, **kwargs):
    from baiji.serialization.util.openlib import ensure_file_open_and_call
    return ensure_file_open_and_call(f, _load, mode='rb', *args, **kwargs)


def dump(obj, f):
    from baiji.serialization.util.openlib import ensure_file_open_and_call
    return ensure_file_open_and_call(f, _dump, mode='wb', obj=obj)

def dumps(obj):
    import StringIO
    output = StringIO.StringIO()
    _dump(output, obj)
    out_string = output.getvalue()
    output.close()
    return out_string

def _load(f, header_row=True, header_row_transformer=lambda x: x):
    '''
    header_row_transformer: Give the caller a chance to rewrite the header row.
      Accepts one argument, a sequence of field names, and should return a
      modified sequence.

    '''
    import csv

    reader = csv.reader(f)
    line_number = 1
    result = []

    if header_row:
        field_names = next(reader)
        field_names = header_row_transformer(field_names)
        line_number += 1

        for row_values in reader:
            if len(row_values) != len(field_names):
                raise ValueError("Header row contains %s items but line %s contains %s" % \
                    (len(field_names), line_number, len(row_values)))

            result.append({k: v for k, v in zip(field_names, row_values)})
            line_number += 1

    else:
        for row_values in reader:
            result.append({i: v for i, v in enumerate(row_values)})
            line_number += 1

    return result


def _dump(f, obj):
    '''
    Per the docs for csv module, use this with binary mode on platforms
    where it matters:

        from baiji.serialization import csv
        with open(file, 'wb') as f:
            csv.dump(obj, f)

        or

        csv.dump(file, obj)

    '''
    import csv
    if not isinstance(obj, list):
        raise ValueError('obj should be a list of lists or tuples')
    if not all([isinstance(x, tuple) or isinstance(x, list) for x in obj]):
        raise ValueError('obj should be a list of lists or tuples')
    writer = csv.writer(f)
    for item in obj:
        writer.writerow(item)


class CSVSerializer(object):
    '''
    Simple CSV serializer. Subclasses can support serializing arrays of
    arbitrary objects, using their own serialization format. Subclasses
    may also set header to an array of tuples which will be used as the
    header content.

    '''
    header = []
    def __init__(self, data):
        self._data = data
    @property
    def body(self):
        if hasattr(self, 'format'):
            return self.format(self._data)
        else:
            return self._data
    def render(self):
        return self.header + self.body
    def dump(self, f):
        # Delegate to baiji.serialization.csv.dump()
        dump(self.render(), f)


class CSVCollectionSerializer(CSVSerializer):
    '''
    Serialize to CSV from a collection of dicts. Dicts should have the
    same keys, which become the column headings.

    '''
    def __init__(self, collection, row_ordering=None):
        '''
        row_ordering: When collection is a dictionary, an optional array
          of keys specifying the order in which to emit the items.

        '''
        super(CSVCollectionSerializer, self).__init__(collection)
        self.keys = self.compute_keys(collection)
        if isinstance(collection, dict):
            self.header = [[''] + self.keys]
        else:
            self.header = [self.keys]
        self.row_ordering = row_ordering

    @classmethod
    def compute_keys(cls, collection):
        if isinstance(collection, dict):
            first_value = next(collection.itervalues())
        else:
            first_value = collection[0]
        result = sorted(first_value.keys())

        # Make sure the keys are consistent.
        if isinstance(collection, dict):
            keyed_collection = collection
        else:
            keyed_collection = {index: value for index, value in enumerate(collection)}

        expected = set(result)
        for key, item in keyed_collection.iteritems():
            if set(item.keys()) != expected:
                message = 'Item %s had different keys (got %s, expected %s)' % \
                    (key, ' '.join(item.keys()), ' '.join(expected))
                raise ValueError(message)

        return result

    def format(self, collection):
        if isinstance(collection, dict):
            if self.row_ordering is not None:
                row_ordering = self.row_ordering
            else:
                row_ordering = collection.keys()
            row_heads = [[key] for key in row_ordering]
            rows = [collection[key] for key in row_ordering]
        else:
            row_heads = [[] for _ in range(len(collection))]
            rows = collection

        return [
            row_head +
            [
                row[k]
                for k in self.keys
            ]
            for row_head, row in zip(row_heads, rows)
        ]
