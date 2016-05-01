import unittest
import os
from baiji.serialization import json

class TestJson(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.tmp_dir = tempfile.mkdtemp('baiji-serialization-json')

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_json_dumps(self):
        '''Examples from json docs'''
        self.assertEqual(
            json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]),
            r'["foo", {"bar": ["baz", null, 1.0, 2]}]')
        self.assertEqual(json.dumps("\"foo\bar"), r'"\"foo\bar"')
        self.assertEqual(json.dumps(u'\u1234'), r'"\u1234"')
        self.assertEqual(json.dumps('\\'), r'"\\"')
        self.assertEqual(
            json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True),
            r'{"a": 0, "b": 0, "c": 0}')
        self.assertEqual(
            json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':')),
            r'[1,2,3,{"4":5,"6":7}]')
        self.assertEqual(
            json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4, separators=(',', ': ')),
            '{\n    "4": 5,\n    "6": 7\n}')

    def test_json_dump_stringio(self):
        from StringIO import StringIO
        io = StringIO()
        json.dump(['streaming API'], io)
        self.assertEqual(io.getvalue(), r'["streaming API"]')

    def test_json_dump_file(self):
        path = os.path.join(self.tmp_dir, "test_json_dump_file.json")
        with open(path, 'w') as f:
            json.dump(['File Test'], f)
        with open(path, 'r') as f:
            self.assertEqual(f.read(), r'["File Test"]')

    def test_json_dump_path(self):
        path = os.path.join(self.tmp_dir, "test_json_dump_path.json")
        json.dump(['File Test'], path)
        with open(path, 'r') as f:
            self.assertEqual(f.read(), r'["File Test"]')

    def test_json_loads(self):
        self.assertEqual(
            json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]'),
            [u'foo', {u'bar': [u'baz', None, 1.0, 2]}])
        self.assertEqual(
            json.loads('"\\"foo\\bar"'),
            u'"foo\x08ar')

    def test_json_load_stringio(self):
        from StringIO import StringIO
        io = StringIO('["streaming API"]')
        self.assertEqual(json.load(io), [u'streaming API'])

    def test_json_load_file(self):
        path = os.path.join(self.tmp_dir, "test_json_load_file.json")
        with open(path, 'w') as f:
            f.write(r'["File Test"]')
        with open(path, 'r') as f:
            self.assertEqual(json.load(f), [u'File Test'])

    def test_json_load_path(self):
        path = os.path.join(self.tmp_dir, "test_json_load_path.json")
        with open(path, 'w') as f:
            f.write(r'["File Test"]')
        self.assertEqual(json.load(path), [u'File Test'])
