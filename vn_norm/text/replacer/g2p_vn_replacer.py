from os import path
import re
from vn_norm.text.replacer.base_simple_replacer import BaseSimpleReplacer
from montreal_forced_aligner.g2p.generator import PyniniDictionaryGenerator
from montreal_forced_aligner.models import G2PModel
import os
import codecs

# hot fix en. refactor later.


class G2pVnReplacer(BaseSimpleReplacer):
    vns_chars_rx = r"[àáạảãâầấậẩẫăằắặẳẵđèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹ]+"

    def __init__(self, dict_path=path.join(path.dirname(__file__), '../mapping/mfag2pvi.txt'), en_dict_path=path.join(path.dirname(__file__), '../mapping/mfag2pen.txt')):
        BaseSimpleReplacer.__init__(self, dict_path)
        self._vn_model_path = os.path.join(
            os.getcwd(), 'dict/models/vietnamese_g2p.zip')
        self._en_model_path = os.path.join(
            os.getcwd(), 'dict/models/english_g2p.zip')
        self._new_words_path = os.path.join(os.getcwd(), 'new-words.txt')
        self._new_en_words_path = os.path.join(os.getcwd(), 'new-words-en.txt')
        self._vn_model = G2PModel(self._vn_model_path)
        self._en_model = G2PModel(self._en_model_path)
        self.load_replace_map(self._new_words_path)

        self._en_replace = BaseSimpleReplacer(en_dict_path)
        self.load_replace_map(self._new_en_words_path,
                              target_dict=self._en_replace._dict)

    def __call__(self, text: str, try_other=None, vi_priority=False, force_en=False) -> str:
        if force_en:
            if text in self._en_replace._dict:
                return self._en_replace._dict[text]
        elif text in self._dict:
            return self._dict[text]
        if text in self._en_replace._dict:
            return self._en_replace._dict[text]
        if try_other is not None:
            return ' '.join(list(filter(lambda x: x != ' ', try_other(text))))
        else:
            print(['new text', text])
            self.gen_new_words(
                text, vi_priority=vi_priority, force_en=force_en)
            if force_en and text in self._en_replace._dict:
                return self._en_replace._dict[text]
            if text in self._dict:
                return self._dict[text]
            if text in self._en_replace._dict:
                return self._en_replace._dict[text]
        return ''

    def fix_pronunciation(self, word, pronunciation):
        pSplit = pronunciation.split()
        if word.find('tr') == 0:
            pSplit[0] = 'tr'
        elif word.find('d') == 0:
            pSplit[0] = 'd1'
        elif word.find('v') == 0:
            pSplit[0] = 'v'
        return ' '.join(pSplit)

    def get_language(self, word):
        check_vi = re.search(self.vns_chars_rx, word)
        if check_vi is not None:
            return 'vi'
        return 'en'

    def gen_new_words(self, word, vi_priority=False, force_en=False):
        lang = 'en'
        if force_en == False:
            lang = 'vi' if vi_priority else self.get_language(word)
        # print(f"init lang: {lang}")
        model_select = self._vn_model if lang == 'vi' else self._en_model
        gen = PyniniDictionaryGenerator(model_select, [word])
        results = gen.generate()
        fix_pronunc = lang == 'vi'
        gen_lang = lang
        tg_dict = self._dict if gen_lang == 'vi' else self._en_replace._dict
        new_words_path = self._new_words_path if gen_lang == 'vi' else self._new_en_words_path
        if results is None or word not in results or results[word] == [''] or len(results) == 0:
            if lang == 'vi':
                fix_pronunc = False
                gen_lang = 'en'
                gen = PyniniDictionaryGenerator(self._en_model, [word])
                results = gen.generate()
        if results is None or word not in results or results[word] == [''] or len(results) == 0:
            return
        with codecs.open(new_words_path, 'a', 'utf-8') as f:
            for (word, pronunciation) in results.items():
                if not pronunciation:
                    continue
                if isinstance(pronunciation, list):
                    for p in pronunciation:
                        if not p:
                            continue
                        if fix_pronunc:
                            p = self.fix_pronunciation(word, p)
                        print(f"{gen_lang}|{word}|{p}")
                        f.write(f"{word}|{p}|{gen_lang}\n")
                        tg_dict[word] = p
                else:
                    pronunciation = self.fix_pronunciation(word, pronunciation)
                    print(f"{gen_lang}|{word}|{pronunciation}")
                    f.write(f"{word}|{pronunciation}|{gen_lang}\n")
                    tg_dict[word] = pronunciation
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
