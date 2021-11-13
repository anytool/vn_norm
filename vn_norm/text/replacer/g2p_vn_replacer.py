from os import path
from vn_norm.text.replacer.base_simple_replacer import BaseSimpleReplacer
from montreal_forced_aligner.g2p.generator import PyniniDictionaryGenerator
from montreal_forced_aligner.models import G2PModel
import os
import codecs


class G2pVnReplacer(BaseSimpleReplacer):
    def __init__(self, dict_path=path.join(path.dirname(__file__), '../mapping/mfag2p.txt')):
        BaseSimpleReplacer.__init__(self, dict_path)
        self._model_path = os.path.join(
            os.getcwd(), 'dict/models/vietnamese_g2p.zip')
        self._new_words_path = os.path.join(os.getcwd(), 'new-words.txt')
        self._model = G2PModel(self._model_path)
        self.load_replace_map(self.load_replace_map(self._new_words_path))

    def __call__(self, text: str, try_other=None) -> str:
        if text in self._dict:
            return self._dict[text]
        elif try_other is not None:
            return ' '.join(list(filter(lambda x: x != ' ', try_other(text))))
        else:
            self.gen_new_words(text)
            if text in self._dict:
                return self._dict[text]
        return ''

    def gen_new_words(self, word):
        gen = PyniniDictionaryGenerator(self._model, [word])
        results = gen.generate()
        with codecs.open(self._new_words_path, 'a', 'utf-8') as f:
            for (word, pronunciation) in results.items():
                if not pronunciation:
                    continue
                if isinstance(pronunciation, list):
                    for p in pronunciation:
                        if not p:
                            continue
                        f.write(f"{word}|{p}\n")
                        self._dict[word] = p
                else:
                    f.write(f"{word}|{pronunciation}\n")
                    self._dict[word] = pronunciation
        # self.load_replace_map(self.load_replace_map(self._new_words_path))

    # def get_all_phonemes(self, ignores=['<unk>']):
    #     g2pen = G2p()
    #     dict = {}
    #     # vn symbols
    #     for x in self._dict:
    #         val = self._dict[x]
    #         val_split = val.strip().split()
    #         for symbol in val_split:
    #             if symbol in dict:
    #                 dict[symbol] += 1
    #             else:
    #                 dict[symbol] = 1
    #     # en symbols
    #     for symbol in g2pen.graphemes:
    #         if symbol in dict:
    #             dict[symbol] += 1
    #         else:
    #             dict[symbol] = 1
    #     for symbol in g2pen.phonemes:
    #         if symbol in dict:
    #             dict[symbol] += 1
    #         else:
    #             dict[symbol] = 1
    #     # remote ignores
    #     for ig_key in ignores:
    #         if ig_key in dict:
    #             del dict[ig_key]
    #     result = sorted(dict.keys())
    #     return result


if __name__ == '__main__':
    rep = G2pVnReplacer()
    # keys = rep.get_all_phonemes()
    # print(len(keys))
    # print('[' + ' '.join(keys) + ']')
    # g2p = G2p()
    # print(g2p("hello ball"))
    # print(eng_to_ipa.convert("hello ball"))
