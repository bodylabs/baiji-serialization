from __future__ import absolute_import
import simplejson as json

EXTENSION = '.json'

def dump(obj, f, *args, **kwargs):
    from baiji.serialization.util.openlib import ensure_file_open_and_call
    return ensure_file_open_and_call(f, _dump, 'w', obj, *args, **kwargs)

def load(f, *args, **kwargs):
    from baiji.serialization.util.openlib import ensure_file_open_and_call
    return ensure_file_open_and_call(f, _load, 'r', *args, **kwargs)

def loads(*args, **kwargs):
    return json.loads(*args, **kwargs)

def dumps(*args, **kwargs):
    kwargs.update(for_json=True)
    return json.dumps(*args, **kwargs)

def _dump(f, obj, *args, **kwargs):
    kwargs.update(for_json=True)
    return json.dump(obj, f, *args, **kwargs)

def _load(f, *args, **kwargs):
    return json.load(f, *args, **kwargs)
