import unittest
from baiji.serialization import yaml

class UnsafeToDump(object):
    """Python classes should not by default be YAML dumpable in safe mode"""
    pass

unsafe_to_load = "!!python/name:baiji.serialization.test_yaml.UnsafeToDump ''\n"

class TestYAML(unittest.TestCase):

    def test_yaml_unsafe_dumps(self):
        self.assertEqual(yaml.dumps(UnsafeToDump), unsafe_to_load)

    def test_yaml_unsafe_loads_uses_load(self):
        self.assertEqual(yaml.loads(unsafe_to_load), UnsafeToDump)

    def test_yaml_safe_dump_raises_on_unsafe(self):
        self.assertRaises(
            yaml.SerializationSafetyError,
            yaml.dumps, UnsafeToDump, safe=True)

    def test_yaml_safe_load_raises_on_unsafe(self):
        self.assertRaises(
            yaml.SerializationSafetyError,
            yaml.loads, unsafe_to_load, safe=True)
