import unittest

from indeed.utils.url_interpreter import URLInterpreter

class URLInterpreterTest(unittest.TestCase):

    def test_parse_url(self):
        expected = 'https://hk.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk=28708afee13b598b'
        actual = URLInterpreter.parse_url("https://proxy.scrapeops.io/v1/?api_key=YOUR_API_KEY&url=https%3A%2F%2Fhk.indeed.com%2Fm%2Fbasecamp%2Fviewjob%3Fviewtype%3Dembedded%26jk%3D28708afee13b598b")
        self.assertEqual(expected, actual)

        expected = None
        actual = URLInterpreter.parse_url(None)
        self.assertEqual(expected, actual)

        expected = ''
        actual = URLInterpreter.parse_url('')
        self.assertEqual(expected, actual)

        expected = 'https://hk.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk=28708afee13b598b'
        actual = URLInterpreter.parse_url("https://hk.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk=28708afee13b598b")
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
