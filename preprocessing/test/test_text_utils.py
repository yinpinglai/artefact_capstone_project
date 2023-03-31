import unittest

from utils.text_utils import TextUtils

class TextUtilsTest(unittest.TestCase):

    def test_remove_punctuation_and_symbols(self):
        expected = " This sentence has a lot of punctuation and symbols such as        etc"
        actual = TextUtils.remove_punctuation_and_symbols(text="- This sentence has a lot of punctuation and symbols, such as $ % @ ! . <> [], etc")
        self.assertEqual(expected, actual)

        self.assertIsNone(TextUtils.remove_punctuation_and_symbols(text=None))
        self.assertEqual('', TextUtils.remove_punctuation_and_symbols(text=''))
        self.assertEqual('This sentence dose not have any punctuation or symbol', 
            TextUtils.remove_punctuation_and_symbols(text='This sentence dose not have any punctuation or symbol'))

    def test_remove_stop_words(self):
        expected = "sample sentence , showing stop words filtration ."
        actual = TextUtils.remove_stop_words(text="This is a sample sentence, showing off the stop words filtration.")
        self.assertEqual(expected, actual)

        self.assertIsNone(TextUtils.remove_stop_words(text=None))
        self.assertEqual('', TextUtils.remove_stop_words(text=''))
        self.assertEqual('showing stop words filtration', TextUtils.remove_stop_words(text='showing stop words filtration'))

    def test_perform_lemmatization(self):
        expected = 'program programmer program'
        actual = TextUtils.perform_lemmatization(text='programs programmer programming')
        self.assertEqual(expected, actual)

        self.assertIsNone(TextUtils.perform_lemmatization(text=None))
        self.assertEqual('', TextUtils.perform_lemmatization(text=''))
        self.assertEqual('program programmer', TextUtils.perform_lemmatization(text='program programmer'))
    