from os import path
from vn_norm.text.replacer.base_simple_replacer import BaseSimpleReplacer


class TeenCodeReplacer(BaseSimpleReplacer):
    def __init__(self, dict_path=path.join(path.dirname(__file__), '../mapping/teen_codes.txt')):
        BaseSimpleReplacer.__init__(self, dict_path)
