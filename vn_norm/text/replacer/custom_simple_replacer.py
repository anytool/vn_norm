import os
from vn_norm.text.replacer.base_simple_replacer import BaseSimpleReplacer


class CustomSimpleReplacer(BaseSimpleReplacer):
    def __init__(self, dict_path=f"{os.getcwd()}/configs/replace.txt"):
        BaseSimpleReplacer.__init__(self, dict_path)
