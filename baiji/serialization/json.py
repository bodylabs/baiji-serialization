from __future__ import absolute_import
import simplejson as json

EXTENSION = '.json'

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

def _load_args(kwargs):
    kwargs.update(object_hook=_json_decode)
    return kwargs

def _dump_args(kwargs):
    if kwargs.get('primitive', False):
        kwargs.update(default=_json_encode_primitive)
    else:
        kwargs.update(default=_json_encode)
    if 'primitive' in kwargs:
        del kwargs['primitive']
    kwargs.update(for_json=True)
    return kwargs

def _json_decode(dct):
    '''
    Handle Custom json decoding and internal double underscore annotated Direct object deserialization
    '''
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
    elif '__scipy.sparse.sparsematrix__' in dct:
        if not 'dtype' in dct and 'shape' in dct and 'data' in dct and 'format' in dct and 'row' in dct and 'col' in dct:
            return dct
        try:
            import numpy as np
            import scipy.sparse as sp
        except ImportError:
            raise ImportError("JSON file contains scipy.sparse arrays; install numpy and scipy to load it")
        coo = sp.coo_matrix((dct['data'], (dct['row'], dct['col'])), shape=dct['shape'], dtype=np.dtype(dct['dtype']))
        return coo.asformat(dct['format'])
    else:
        return dct

def _json_encode_primitive(obj):
    try:
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist()
    except ImportError:
        # Clearly there won't be any numpy arrays to encode...
        pass
    return None

def _json_encode(obj):
    try:
        import numpy as np
        if isinstance(obj, np.ndarray):
            return {
                '__ndarray__': obj.tolist(),
                'dtype': obj.dtype.name,
                'shape': obj.shape,
            }
    except ImportError:
        # Clearly there won't be any numpy arrays to encode...
        pass
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
    except ImportError:
        # Clearly there won't be any scipy.sparse arrays to encode...
        pass
    return None
