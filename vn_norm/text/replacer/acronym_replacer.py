from os import path
from vn_norm.text.replacer.base_simple_replacer import BaseSimpleReplacer


class AcronymReplacer(BaseSimpleReplacer):
    def __init__(self, dict_path=path.join(path.dirname(__file__), '../mapping/acronyms.txt'), flags=0):
        BaseSimpleReplacer.__init__(self, dict_path=dict_path, flags=flags)
