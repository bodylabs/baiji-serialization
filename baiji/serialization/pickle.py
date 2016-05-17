from cPickle import UnpicklingError # We import this to expose it to our importers pylint: disable=unused-import

EXTENSION = '.pkl'

def dump(obj, f):
    from baiji.serialization.util.openlib import ensure_file_open_and_call
    return ensure_file_open_and_call(f, _dump, 'wb', obj)

def load(f, *args, **kwargs):
    from baiji.serialization.util.openlib import ensure_file_open_and_call
    return ensure_file_open_and_call(f, _load, 'rb', *args, **kwargs)

def loads(s, *args, **kwargs):
    import cPickle as pickle
    return pickle.loads(s, *args, **kwargs)

def dumps(obj):
    import cPickle as pickle
    return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)

def _dump(f, obj):
    import cPickle as pickle
    return pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def _load(f, constructors=None):
    '''
    constructors: A dictionary mapping strings to callables, which are
      consulted as additional constructors during unpickling. This is useful
      for interposing an alternative constructor, or for supporting class
      names which have been changed. This is implemented via the cPickle
      `Unpickler`'s `find_global` attribute, which is documented here,
      albeit quite densely:
      https://docs.python.org/2/library/pickle.html#subclassing-unpicklers
    '''
    import cPickle as pickle
    from baiji.serialization.util.importlib import class_from_str

    def unpickler_find_global(module_name, class_name):
        fully_qualified_name = '{}.{}'.format(module_name, class_name)
        try:
            return constructors[fully_qualified_name]
        except KeyError:
            # It would be tempting to delegate to the original `find_global`.
            # Unfortunately, `Unpickler` does not expose the default
            # implementation. Thanks, Obama.
            return class_from_str(fully_qualified_name)

    unpickler = pickle.Unpickler(f)
    if constructors:
        unpickler.find_global = unpickler_find_global
    return unpickler.load()
