from os import path
from g2p_en import G2p
from vn_norm.text.replacer.base_simple_replacer import BaseSimpleReplacer


class G2pVnReplacer(BaseSimpleReplacer):
    def __init__(self, dict_path=path.join(path.dirname(__file__), '../mapping/vinphon.txt')):
        BaseSimpleReplacer.__init__(self, dict_path)

    def __call__(self, text: str, try_other=None) -> str:
        if text in self._dict:
            return self._dict[text]
        elif try_other is not None:
            return ' '.join(list(filter(lambda x: x != ' ', try_other(text))))
        return ''
    
    def get_all_phonemes(self, ignores=['<unk>']):
        g2pen = G2p()
        dict = {}
        # vn symbols
        for x in self._dict:
            val = self._dict[x]
            val_split = val.strip().split()
            for symbol in val_split:
                if symbol in dict:
                    dict[symbol] += 1
                else:
                    dict[symbol] = 1
        # en symbols
        for symbol in g2pen.graphemes:
            if symbol in dict:
                dict[symbol] += 1
            else:
                dict[symbol] = 1
        for symbol in g2pen.phonemes:
            if symbol in dict:
                dict[symbol] += 1
            else:
                dict[symbol] = 1
        # remote ignores
        for ig_key in ignores:
            if ig_key in dict:
                del dict[ig_key]
        result = sorted(dict.keys())
        return result


if __name__ == '__main__':
    rep = G2pVnReplacer()
    keys = rep.get_all_phonemes()
    print(len(keys))
    print('[' + ' '.join(keys) + ']')
    # g2p = G2p()
    # print(g2p("hello ball"))
    # print(eng_to_ipa.convert("hello ball"))