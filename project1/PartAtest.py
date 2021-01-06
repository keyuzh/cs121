import unittest
import PartA

import io
import unittest.mock

class TestPrint(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, expected_input, expected_output, mock_stdout):
        test = PartA.WordFrequencies()
        test.print(expected_input)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_only_numbers(self):
        input_dict = {
            'in': 2, 'live': 2, 'mostly': 2, 'a': 1, 'africa': 1,
            'fact': 1, 'fun': 1, 'here': 1, 'india': 1
            }
        expected = """in\t2\nlive\t2\nmostly\t2\na\t1\nafrica\t1\nfact\t1\nfun\t1\nhere\t1\nindia\t1\n"""
        self.assert_stdout(input_dict, expected)

class PartATests(unittest.TestCase):
    def test_computeWordFrequencies_noDublicates(self):
        tokens = [
            'apple',
            'banana',
            'boo'
        ]
        expected = {
            'apple' : 1,
            'banana' : 1,
            'boo' : 1,
        }
        test = PartA.WordFrequencies()
        self.assertDictEqual(expected, test.computeWordFrequencies(tokens))

    def test_computeWordFrequencies_withDublicates(self):
        tokens = [
            'apple',
            'boo',
            'boo'
        ]
        expected = {
            'apple': 1,
            'boo': 2,
        }
        test = PartA.WordFrequencies()
        self.assertDictEqual(expected, test.computeWordFrequencies(tokens))


if __name__ == '__main__':
    unittest.main()
