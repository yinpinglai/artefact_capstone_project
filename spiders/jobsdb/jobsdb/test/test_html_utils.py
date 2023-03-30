import unittest

from jobsdb.utils.html_utils import HTMLUtils

class HTMLUtilsTest(unittest.TestCase):

    def test_remove_html_tags(self):
        expected = "TitleA long text........  a link"
        actual = HTMLUtils.remove_html_tags(
            html="<div><h1>Title</h1><p>A long text........ </p><a href=""> a link </a></div>")
        self.assertEqual(expected, actual)

        self.assertIsNone(HTMLUtils.remove_html_tags(html=None))
        self.assertEqual('', HTMLUtils.remove_html_tags(html=''))
        self.assertEqual('Title ~~', HTMLUtils.remove_html_tags(html='Title ~~'))

if __name__ == '__main__':
    unittest.main()
