import unittest

from jobsdb.utils.json_utils import JSONUtils

class JSONUtilsTest(unittest.TestCase):

    def test_load_keywords_json_file(self):
        expected = [
            ['Software developer', 'Digital Payment'],
            ['Software engineer', 'Digital Payment'],
            ['Programmer', 'Digital Payment'],
            ['Software developer', 'Electronic Wallet'],
            ['Software engineer', 'Electronic Wallet'],
            ['Programmer', 'Electronic Wallet']
        ]
        actual = JSONUtils.load_keywords_json()
        self.assertEqual(expected, actual)

    def test_get_dict_from(self):
        expected = dict({
            'id': 'any',
            'title': 'any',
            'name': 'any',
        })
        actual = JSONUtils.get_dict_from(json_string='{"id":"any","title":"any","name":"any"}')
        self.assertDictEqual(expected, actual)

    def test_get_dict_from_error(self):
        expected = dict({})
        actual = JSONUtils.get_dict_from(json_string=None)
        self.assertDictEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
