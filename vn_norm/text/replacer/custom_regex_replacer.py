import os
from vn_norm.text.replacer.base_regex_replacer import BaseRegexReplacer


class CustomRegexReplacer(BaseRegexReplacer):
    def __init__(self, dict_path=f"{os.getcwd()}/configs/replace.txt"):
        BaseRegexReplacer.__init__(self, dict_path)
