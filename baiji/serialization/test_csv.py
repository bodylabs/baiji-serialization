import unittest

class TestCSV(unittest.TestCase):

    def test_collection_csv_serializer_renders_correct_rows(self):
        from baiji.serialization.csv import CSVCollectionSerializer

        example_data = {
            'one': {'foo': 'baz1', 'bar': 'inga1'},
            'three': {'foo': 'baz3', 'bar': 'inga3'},
            'two': {'foo': 'baz2', 'bar': 'inga2'},
        }
        ordering = ['one', 'two', 'three']

        serializer = CSVCollectionSerializer(
            collection=example_data,
            row_ordering=ordering
        )

        expected = [
            ['', 'bar', 'foo'],
            ['one', 'inga1', 'baz1'],
            ['two', 'inga2', 'baz2'],
            ['three', 'inga3', 'baz3'],
        ]

        self.assertEqual(serializer.render(), expected)

    def test_collection_csv_serializer_works_with_row_ordering_np_array(self):
        import numpy as np
        from baiji.serialization.csv import CSVCollectionSerializer

        example_data = {
            'one': {'foo': 'baz1', 'bar': 'inga1'},
            'three': {'foo': 'baz3', 'bar': 'inga3'},
            'two': {'foo': 'baz2', 'bar': 'inga2'},
        }
        ordering = np.array(['one', 'two', 'three'])

        serializer = CSVCollectionSerializer(
            collection=example_data,
            row_ordering=ordering
        )

        expected = [
            ['', 'bar', 'foo'],
            ['one', 'inga1', 'baz1'],
            ['two', 'inga2', 'baz2'],
            ['three', 'inga3', 'baz3'],
        ]

        self.assertEqual(serializer.render(), expected)
