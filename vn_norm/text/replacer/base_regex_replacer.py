import re
from os import path
import codecs


class BaseRegexReplacer:

    def __init__(self, dict_path: str, split_text='|', flags=re.IGNORECASE):
        self._regex_replace_map = []
        self._flags = re.IGNORECASE
        self._dict_path = dict_path
        self._split_text = split_text
        self._flags = flags
        self.load_replace_map()

    def load_replace_map(self, dict_path: str = None):
        file_path = dict_path or self._dict_path
        if path.isfile(file_path):
            lines = []
            with codecs.open(file_path, "r", "utf-8") as fid:
                for line in fid.readlines():
                    s_index = line.find(self._split_text)
                    if(s_index > 0):
                        lines.append(
                            [line[:s_index].strip(), line[s_index + 1:].strip()])
            self._regex_replace_map = [
                (re.compile(x[0], flags=self._flags), x[1])
                for x in lines
            ]

    def __call__(self, text):
        # text is a paragraph or sentence
        # print(text)
        for regex, replacement in self._regex_replace_map:
            text = re.sub(regex, replacement, text, flags=self._flags)
        # print(text)
        return text
