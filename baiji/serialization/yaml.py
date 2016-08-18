from __future__ import absolute_import

EXTENSION = '.yaml'

class SerializationSafetyError(Exception):
    pass

def dump(obj, f, *args, **kwargs):
    from baiji.serialization.util.openlib import ensure_file_open_and_call
    return ensure_file_open_and_call(f, _dump, 'w', obj, *args, **kwargs)


def load(f, *args, **kwargs):
    from baiji.serialization.util.openlib import ensure_file_open_and_call
    return ensure_file_open_and_call(f, _load, 'r', *args, **kwargs)


def loads(s, *args, **kwargs):
    import yaml
    safe_load = kwargs.pop('safe_load', False) # Perhaps default should be True?
    if safe_load:
        try:
            return yaml.safe_load(s, *args, **kwargs)
        except yaml.representer.RepresenterError as e:
            raise SerializationSafetyError(*e.args)
    return yaml.load(s, *args, **kwargs)


def dumps(obj, *args, **kwargs):
    import yaml
    safe_dump = kwargs.pop('safe_dump', False) # Perhaps default should be True?
    if safe_dump:
        try:
            return yaml.safe_dump(obj, *args, **kwargs)
        except yaml.representer.RepresenterError as e:
            raise SerializationSafetyError(*e.args)
    return yaml.dump(obj, *args, **kwargs)


def _dump(f, obj, *args, **kwargs):
    import yaml
    safe_dump = kwargs.pop('safe_dump', False) # Perhaps default should be True?
    if safe_dump:
        try:
            return yaml.safe_dump(obj, f, *args, **kwargs)
        except yaml.representer.RepresenterError as e:
            raise SerializationSafetyError(*e.args)
    return yaml.dump(obj, f, *args, **kwargs)


def _load(f, *args, **kwargs):
    import yaml
    safe_load = kwargs.pop('safe_load', False) # Perhaps default should be True?
    if safe_load:
        try:
            return yaml.safe_load(f, *args, **kwargs)
        except yaml.representer.RepresenterError as e:
            raise SerializationSafetyError(*e.args)
    return yaml.load(f, *args, **kwargs)
