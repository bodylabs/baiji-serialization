def module_from_str(s):
    if not s:
        raise ValueError('Empty module name')
    from_name = s.split('.')[-1]
    try:
        mod = __import__(s, fromlist=str(from_name))
        return mod
    except:
        import traceback
        tb = traceback.format_exc()
        raise ImportError("Unable to import %s with exception : \n[\n%s]" % (s, tb))

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
