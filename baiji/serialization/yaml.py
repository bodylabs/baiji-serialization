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
    return _load(s, *args, **kwargs)


def dumps(obj, *args, **kwargs):
    import yaml
    import warnings
    safe_mode = kwargs.pop('safe', None)
    try:
        return yaml.safe_dump(obj, *args, **kwargs)
    except yaml.representer.RepresenterError as e:
        if safe_mode:
            raise SerializationSafetyError(*e.args)
        if safe_mode is None:
            warnings.warn(
                ('Unsafe YAML serialization. This will generate an error in the '
                 'future. Call with `safe=False` if you really want unsafe serialization.'),
                DeprecationWarning, stacklevel=2
            )
        # if safe_mode is None (not given) or False (explicitly set), fall back to unsafe behavior
        return yaml.dump(obj, *args, **kwargs)



def _dump(f, obj, *args, **kwargs):
    import yaml
    import warnings
    safe_mode = kwargs.pop('safe', None)
    try:
        return yaml.safe_dump(obj, f, *args, **kwargs)
    except yaml.representer.RepresenterError as e:
        if safe_mode:
            raise SerializationSafetyError(*e.args)
        if safe_mode is None:
            warnings.warn(
                ('Unsafe YAML serialization. This will generate an error in the '
                 'future. Call with `safe=False` if you really want unsafe serialization.'),
                DeprecationWarning, stacklevel=2
            )
        # if safe_mode is None (not given) or False (explicitly set), fall back to unsafe behavior
        return yaml.dump(obj, f, *args, **kwargs)


def _load(f, *args, **kwargs):
    import yaml
    import warnings
    safe_mode = kwargs.pop('safe', None)
    try:
        return yaml.safe_load(f, *args, **kwargs)
    except yaml.constructor.ConstructorError as e:
        if safe_mode:
            raise SerializationSafetyError(*e.args)
        if safe_mode is None:
            warnings.warn(
                ('Unsafe YAML serialization. This will generate an error in the '
                 'future. Call with `safe=False` if you really want unsafe serialization.'),
                DeprecationWarning, stacklevel=2
            )
        # if safe_mode is None (not given) or False (explicitly set), fall back to unsafe behavior
        return yaml.load(f, *args, **kwargs)
