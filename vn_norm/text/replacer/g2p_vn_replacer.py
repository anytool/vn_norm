from os import path
from vn_norm.text.replacer.base_simple_replacer import BaseSimpleReplacer


class G2pVnReplacer(BaseSimpleReplacer):
    def __init__(self, dict_path=path.join(path.dirname(__file__), '../mapping/kaldiphon.txt')):
        BaseSimpleReplacer.__init__(self, dict_path)

    def __call__(self, text: str, try_other=None) -> str:
        if text in self._dict:
            return self._dict[text]
        elif try_other is not None:
            return ' '.join(list(filter(lambda x: x != ' ', try_other(text))))
        return ''
