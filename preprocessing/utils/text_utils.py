import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class TextUtils:

    CHARACTER_AND_EMPTY_SPACE_REGEX = re.compile('[^\w\s]')

    STOP_WORDS_SET = set(stopwords.words('english'))

    @classmethod
    def remove_punctuation_and_symbols(cls, text:str) -> str:
        '''
        Remove all punctuation and symbols for the given text

        Parameters:
        - text:str - The text which contains punctuation and symbols

        Returns:
        - text:str - The text which has been removed all punctuation and symbols
        '''
        if text is None or len(text) == 0:
            return text
        
        return re.sub(TextUtils.CHARACTER_AND_EMPTY_SPACE_REGEX, ' ', text)

    @classmethod
    def remove_stop_words(cls, text:str) -> str:
        '''
        Remove all stop words for the given text

        Parameters:
        - text:str - The text which contains stop words

        Returns:
        - text:str - The text which has been removed all stop words
        '''
        if text is None or len(text) == 0:
            return text
        
        word_tokens = word_tokenize(text)
        filtered_sentence_word_list = [w for w in word_tokens if not w.lower() in TextUtils.STOP_WORDS_SET]
        return ' '.join(filtered_sentence_word_list)

    @classmethod
    def perform_lemmatization(cls, text:str) -> str:
        '''
        Perform the Lemmatization algorithm to reduce inflected words to their root word

        Parameters:
        - text:str - The text which has not been converted to their root word

        Returns:
        - text:str - The text which has been converted to their root word
        '''
        if text is None or len(text) == 0:
            return text
        
        sentence_without_punctuation = TextUtils.remove_punctuation_and_symbols(text=text)
        word_tokens = word_tokenize(sentence_without_punctuation)

        wnl = WordNetLemmatizer()
        converted_words = [wnl.lemmatize(w, pos='v') for w in word_tokens]
        return ' '.join(converted_words)

    @classmethod
    def tokenize(cls, text:str) -> list[str]:
        '''
        Tokenize the given string into a bag of words

        Parameters:
        - text:str - The text to be tokenized

        Returns:
        - test:str - The text has been tokenized
        '''
        if text is None or len(text) == 0:
            return text
        
        return word_tokenize(text)
