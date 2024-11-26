import re

import nltk
from nltk.corpus import stopwords


class Preprocessing(object):
    def __init__(self):
        nltk.download('stopwords')
        self.__stopword = stopwords.words('english')

    def _stopword_removal(self, text: str):
        """
        Remove stopword from text

        :return:
        """
        stopword_to_remove = self.__stopword

        compiled_str = r''
        for i, word in enumerate(stopword_to_remove):
            if i == len(stopword_to_remove) - 1:
                compiled_str = compiled_str + r'\b' + word + r'\b'
            else:
                compiled_str = compiled_str + r'\b' + word + r'\b | '
        regex = re.compile(compiled_str, flags=re.I | re.X)
        clean_text = regex.sub('', text)
        return clean_text

    def _clean_special_characters(self, text: str) -> str:
        text = re.compile("&#39;").sub('', text)
        text = re.compile('[_[\]{}~\':;"’‘()–\n\r<>@&*+!?•°.,\\\/%=^$|#“”]+').sub('', text)
        return ' '.join(text.split())

    def clean_text(self, text: str) -> str:
        text = self._stopword_removal(text)
        return self._clean_special_characters(text)
