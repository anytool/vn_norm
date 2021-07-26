import re
from os import path
import codecs


class BaseSimpleReplacer:
    # _dict = dict()
    # _flags = re.IGNORECASE

    def __init__(self, dict_path: str, split_text='|', flags=re.IGNORECASE):
        self._dict = dict()
        self._dict_path = dict_path
        self._split_text = split_text
        self._flags = flags
        self.load_replace_map()

    def load_replace_map(self, dict_path: str = None):
        file_path = dict_path or self._dict_path
        if path.isfile(file_path):
            with codecs.open(file_path, "r", "utf-8") as fid:
                if self._flags == re.IGNORECASE:
                    for line in fid.readlines():
                        s_index = line.find(self._split_text)
                        if(s_index > 0):
                            self._dict[line[:s_index].strip().lower()
                                       ] = line[s_index + 1:].strip()
                else:
                    for line in fid.readlines():
                        s_index = line.find(self._split_text)
                        if(s_index > 0):
                            self._dict[line[:s_index].strip()
                                       ] = line[s_index + 1:].strip()

    def __call__(self, text):
        # text is a word or word block
        if text in self._dict:
            return self._dict[text]
        return text
