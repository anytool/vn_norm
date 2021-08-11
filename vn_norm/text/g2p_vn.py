from vn_norm.text.replacer.g2p_vn_replacer import G2pVnReplacer
from vn_norm.text.replacer.teen_code_replacer import TeenCodeReplacer
from vn_norm.text.replacer.acronym_replacer import AcronymReplacer
from vn_norm.text.replacer.custom_simple_replacer import CustomSimpleReplacer
from vn_norm.text.replacer.custom_regex_replacer import CustomRegexReplacer
from vn_norm.text.symbols import punctuations
from vn_norm import vn_norm
from underthesea import word_tokenize, sent_tokenize
from vietnamese_cleaner.vietnameseNormUniStd import UniStd

from g2p_en import G2p
import re


class G2pVn:
    def __init__(self,
                 try_other=G2p(),
                 pre_processes: list = [],
                 custom_regex_replacer=CustomRegexReplacer(),
                 custom_simple_replacer=CustomSimpleReplacer(),
                 acronym_replacer=AcronymReplacer(),
                 teen_code_replacer=TeenCodeReplacer(),
                 g2p_vn_replacer=G2pVnReplacer(),
                 end_punctuation=True,
                 delimit = '_'
                 ):
        self._pre_processes = pre_processes
        self._try_other = try_other
        self._custom_regex_replacer = custom_regex_replacer
        self._custom_simple_replacer = custom_simple_replacer
        self._acronym_replacer = acronym_replacer
        self._teen_code_replacer = teen_code_replacer
        self._g2p_vn_replacer = g2p_vn_replacer
        self._end_punctuation = end_punctuation
        self._delimit = delimit

    def punctuation_norm(self, text):
        text = re.sub(r'[\?\.!,\-:;\']+[\ ]{0,1}(?=[\?\.!,\-:;\'])', '', text)
        return text

    def __call__(self, text: str):
        # print(text)
        text = UniStd(text)
        for pre_process in self._pre_processes:
            text = pre_process(text)
        # custom regex
        text = self._custom_regex_replacer(text)
        # text = vn_norm(text)
        result = []
        sents = sent_tokenize(text)
        for sent in sents:
            # '"' symbol
            quote_count = 0
            last_quote_index = -1
            while True:
                quote_index = sent.find('"', last_quote_index + 1)
                if quote_index >= 0:
                    last_quote_index = quote_index
                    quote_count +=1
                else:
                    break
            if quote_count % 2 == 1 and last_quote_index + 1 < len(sent):
                sent += '"'
            sent_result = []
            space_flag = False
            depends = word_tokenize(sent)
            if self._end_punctuation and depends[len(depends) - 1] not in punctuations:
                depends.append('.')
                # depends.append(('.', 9, 'punct'))
            for words in depends:
                words = self.punctuation_norm(words)
                # words, _, word_type = depend
                if len(words) == 1 and words in punctuations:
                    sent_result.append(words)
                    space_flag = False
                else:
                    words = self._custom_simple_replacer(words)
                    words = self._acronym_replacer(words)
                    words = self._teen_code_replacer(words)
                    words = vn_norm(words)
                    word_split = words.split()
                    for word in word_split:
                        word = self._custom_simple_replacer(word)
                        word = self._acronym_replacer(word)
                        word = self._teen_code_replacer(word)
                        word = self._g2p_vn_replacer(word.lower(), try_other=self._try_other)
                        if space_flag:
                            sent_result.append(self._delimit)
                        sent_result.append(word)
                        space_flag = True
            sent_result = ' '.join(sent_result)
            result.append(sent_result)
        return result
    
    def parseAndJoinSents(self, text:str, join_str = '\n'):
        return join_str.join(self.__call__(text))


if __name__ == '__main__':
    text = "campuchia. philippin và indonesia"
    g = G2pVn()
    res = g(text)
    print(res)
    # g2p = G2p()
    # print(g2p("hello ball"))
    # print(eng_to_ipa.convert("hello ball"))
