from vn_norm.text.g2p_vn import G2pVn
# import g2p_en
# import re


class G2p:
    def __init__(self, delimit=' '):
        self._delimit = delimit
        # self._g2pen = g2p_en.G2p()
        self._g2pvn = G2pVn(try_other=None)

    def g2p_vi(self, text: str, join_str=None, vi_priority=False):
        if join_str is not None:
            return self._g2pvn.parseAndJoinSents(text, join_str=join_str, vi_priority=vi_priority)
        return self._g2pvn(text)

    # def g2p_en(self, text: str):
    #     text = self._g2pvn.punctuation_norm(text)
    #     result = self._g2pen(text)
    #     result = map(lambda x: '_' if x == ' ' else x, result)
    #     return self._delimit.join(result)


if __name__ == '__main__':
    text = 'The phosphates which the process of “bolting” removes to a large extent from white flour, go directly to the manufacture of bone,'
    g2p = G2p()
    # t = g2p.g2p_en(text)
    # print(t)
    t = g2p.g2p_vi(text, join_str=' ')
    print(t)
