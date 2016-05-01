def ensure_file_open_and_call(path_or_fp, fn, mode='r', *args, **kwargs):
    from baiji import s3

    if isinstance(path_or_fp, basestring):
        with s3.open(path_or_fp, mode) as f:
            return fn(f, *args, **kwargs)
    elif isinstance(path_or_fp, file) or (hasattr(path_or_fp, 'read') and hasattr(path_or_fp, 'seek')):
        result = fn(path_or_fp, *args, **kwargs)
        if hasattr(path_or_fp, 'flush'):
            path_or_fp.flush()
        return result
    else:
        raise ValueError('Object {} does not appear to be a path or a file like object'.format(path_or_fp))

def class_from_str(s):
    if not s:
        raise ValueError('Empty class name')
    mod_name = '.'.join(s.split('.')[0:-1])
    class_name = s.split('.')[-1]
    try:
        mod = module_from_str(mod_name)
        return getattr(mod, class_name)
    except ImportError:
        raise
    except AttributeError as e:
        raise ImportError("Unable to import %s from module '%s': %s " % (class_name, mod_name, e.args))
