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

    def load_replace_map(self, dict_path: str = None, target_dict=None):
        tg_dict = target_dict if target_dict is not None else self._dict
        file_path = dict_path or self._dict_path
        if path.isfile(file_path):
            with codecs.open(file_path, "r", "utf-8") as fid:
                for line in fid.readlines():
                    line_split = line.split('|')
                    if(len(line_split) >= 2):
                        word = line_split[0].strip()
                        if self._flags == re.IGNORECASE:
                            word = word.lower()
                        tg_dict[word] = line_split[1].strip()

    def __call__(self, text, empty_on_unmap=False):
        # text is a word or word block
        if text in self._dict:
            return self._dict[text]
        if empty_on_unmap:
            return ''
        return text
