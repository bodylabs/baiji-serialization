baiji-serialization
===================

Read and write common file formats to Amazon S3 and local files.


Features
--------

- Reads and writes Pickle, CSV, JSON, and YAML
- Works without an S3 connection (with local files)
- Supports Python 2.7 and uses boto2
- Supports OS X, Linux, and Windows
- Tested and production-hardened


Examples
--------

```py
from baiji.serialization import json
with open(filename, 'w') as f:
    json.dump(foo, f)
with open(filename, 'r') as f:
    foo = json.load(f)
```

```py
from baiji.serialization import json
foo = json.load(filename)
```

```py
from baiji.serialization import csv
with open(filename, 'w') as f:
    csv.dump(foo, f)
with open(filename, 'r') as f:
    foo = csv.load(f)
```

```py
from baiji.serialization import csv
foo = csv.load(filename)
```

Development
-----------

```sh
pip install -r requirements_dev.txt
rake test
rake lint
```


Contribute
----------

- Issue Tracker: github.com/bodylabs/baiji-serialization/issues
- Source Code: github.com/bodylabs/baiji-serialization

Pull requests welcome!


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the Apache license, version 2.0.
