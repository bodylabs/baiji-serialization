from __future__ import absolute_import
import simplejson as json

EXTENSION = '.json'
ENCODE_PRIMITIVES_BY_DEFAULT = False

def dump(obj, f, *args, **kwargs):
    from baiji.serialization.util.openlib import ensure_file_open_and_call
    return ensure_file_open_and_call(f, _dump, 'w', obj, *args, **kwargs)

def dumps(*args, **kwargs):
    return json.dumps(*args, **_dump_args(kwargs))

def _dump(f, obj, *args, **kwargs):
    return json.dump(obj, f, *args, **_dump_args(kwargs))

def load(f, *args, **kwargs):
    from baiji.serialization.util.openlib import ensure_file_open_and_call
    return ensure_file_open_and_call(f, _load, 'r', *args, **kwargs)

def _load(f, *args, **kwargs):
    return json.load(f, *args, **_load_args(kwargs))

def loads(*args, **kwargs):
    return json.loads(*args, **_load_args(kwargs))

class MethodListCaller(object):
    '''
    This is an internal class that lets the JSON(En,De)coder classes
    and their subclasses easily register a list of methods to try, which
    will then be called in order until one of them succeeds.
    '''
    def register(self, method, index=-1):
        if not hasattr(self, 'method_list'):
            self.clear()
        if index == -1:
            index = len(self.method_list)
        self.method_list.insert(index, method)

    def clear(self):
        # be defensive if someone forgets to call super pylint: disable=attribute-defined-outside-init
        self.method_list = []

    def __call__(self, x):
        '''
        Call the methods in method_list until one of them returns something other than None
        and return that as the result of the call.
        '''
        from itertools import ifilter
        try:
            return next(ifilter(lambda x: x is not None, (f(x) for f in self.method_list)))
        except StopIteration:
            return self.default(x)

    def default(self, x):
        '''
        If none of the methods returned something, then return this default
        '''
        return x

class JSONDecoder(MethodListCaller):
    '''
    Instances may be passed to simplejson as object_hook to decode json objects.
    The decoders will be called in order. The first one to return something other
    than None wins. The decoders will be given a dict to parse, something like:

        {
            "__ndarray__": [
                    [859.0, 859.0],
                    [217.0, 106.0],
                    [302.0, 140.0]
                ],
            "dtype": "float32",
            "shape": [3, 2]
        }

    Note that for object_hook, if we want to do nothing, we return the dict unchanged
    and the json is decoded as a plain old dict; this behavior is the default of
    MethodListCaller.
    '''
    def __init__(self):
        self.register(self.decode_numpy)
        self.register(self.decode_scipy)
        self.register(self.decode)

    def decode(self, dct):
        '''
        In a subclass, either override this or add some decode functions and
        override __init__ to register them
        '''
        pass

    def decode_numpy(self, dct):
        if '__ndarray__' in dct:
            try:
                import numpy as np
            except ImportError:
                raise ImportError("JSON file contains numpy arrays; install numpy to load it")
            if 'dtype' in dct:
                dtype = np.dtype(dct['dtype'])
            else:
                dtype = np.float64
            return np.array(dct['__ndarray__'], dtype=dtype)

    def decode_scipy(self, dct):
        if '__scipy.sparse.sparsematrix__' in dct:
            if not 'dtype' in dct and 'shape' in dct and 'data' in dct and 'format' in dct and 'row' in dct and 'col' in dct:
                return dct
            try:
                import numpy as np
                import scipy.sparse as sp
            except ImportError:
                raise ImportError("JSON file contains scipy.sparse arrays; install numpy and scipy to load it")
            coo = sp.coo_matrix((dct['data'], (dct['row'], dct['col'])), shape=dct['shape'], dtype=np.dtype(dct['dtype']))
            return coo.asformat(dct['format'])


def _load_args(kwargs):
    if 'object_hook' in kwargs:
        raise ValueError("Instead of explicitly setting object_hook, subclass JSONDecoder and pass it as decoder")
    if 'decoder' in kwargs:
        kwargs['object_hook'] = kwargs['decoder']
        del kwargs['decoder']
    else:
        kwargs['object_hook'] = JSONDecoder()
    return kwargs


class JSONEncoder(MethodListCaller):
    '''
    Instances may be passed to simplejson as default to encode json objects.
    The encoders will be called in order. The first one to return something other
    than None wins. The encoders will be given an object to encore and should return
    a dict, something like:

        {
            "__ndarray__": [
                    [859.0, 859.0],
                    [217.0, 106.0],
                    [302.0, 140.0]
                ],
            "dtype": "float32",
            "shape": [3, 2]
        }

    Note that for default, if we want to do nothing, we return None and the object
    is encoded as best as simplejson can (which is often by throwing a TypeError).
    We override MethodListCaller.default to get this behavior.
    '''
    def __init__(self, primitive=ENCODE_PRIMITIVES_BY_DEFAULT):
        self.primitive = primitive
        self.register(self.encode_numpy)
        self.register(self.encode_scipy)
        self.register(self.encode)

    def default(self, x):
        return None

    def encode(self, obj):
        '''
        In a subclass, either override this or add some encode functions and
        override __init__ to register them
        '''
        pass

    def encode_numpy(self, obj):
        try:
            import numpy as np
            if isinstance(obj, np.ndarray):
                if self.primitive:
                    return obj.tolist()
                else:
                    return {
                        '__ndarray__': obj.tolist(),
                        'dtype': obj.dtype.name,
                        'shape': obj.shape,
                    }
            elif isinstance(obj, (np.bool8, np.bool_)):
                return bool(obj)
            elif isinstance(obj, (np.half, np.single, np.double, np.float_, np.longfloat, np.float16, np.float32, np.float64)) or (hasattr(np, 'float128') and isinstance(obj, np.float128)):
                return float(obj)
            elif isinstance(obj, (np.byte, np.short, np.intc, np.int_, np.longlong, np.intp, np.int8, np.int16, np.int32, np.int64, np.ubyte, np.ushort, np.uintc, np.uint, np.ulonglong, np.uintp, np.uint8, np.uint16, np.uint32, np.uint64)):
                return int(obj)
            else:
                return None
        except ImportError:
            # Clearly there won't be any numpy arrays to encode...
            return None

    def encode_scipy(self, obj):
        try:
            import scipy.sparse as sp
            if sp.isspmatrix(obj):
                coo = obj.tocoo()
                return {
                    '__scipy.sparse.sparsematrix__': True,
                    'format': obj.getformat(),
                    'dtype': obj.dtype.name,
                    'shape': obj.shape,
                    'data': coo.data,
                    'row': coo.row,
                    'col': coo.col,
                }
            else:
                return None
        except ImportError:
            # Clearly there won't be any scipy.sparse arrays to encode...
            return None


def _dump_args(kwargs):
    if 'default' in kwargs:
        raise ValueError("Instead of explicitly setting default, subclass JSONEncoder and pass it as encoder")
    if 'encoder' in kwargs:
        kwargs['default'] = kwargs['encoder']
        del kwargs['encoder']
    else:
        kwargs['default'] = JSONEncoder(primitive=kwargs.get('primitive', ENCODE_PRIMITIVES_BY_DEFAULT))
    if 'primitive' in kwargs:
        del kwargs['primitive']
    kwargs['for_json'] = True
    return kwargs
