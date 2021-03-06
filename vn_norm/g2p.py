from vn_norm.text.g2p_vn import G2pVn
# import g2p_en
# import re


class G2p:
    def __init__(self, delimit=' '):
        self._delimit = delimit
        # self._g2pen = g2p_en.G2p()
        self._g2pvn = G2pVn(try_other=None)

    def g2p_vi(self, text: str, join_str=None, vi_priority=False, force_en=False):
        if join_str is not None:
            return self._g2pvn.parseAndJoinSents(text, join_str=join_str, vi_priority=vi_priority, force_en=force_en)
        return self._g2pvn(text)

    # def g2p_en(self, text: str):
    #     text = self._g2pvn.punctuation_norm(text)
    #     result = self._g2pen(text)
    #     result = map(lambda x: '_' if x == ' ' else x, result)
    #     return self._delimit.join(result)


if __name__ == '__main__':
    text = 'à tan có áo'
    g2p = G2p()
    # t = g2p.g2p_en(text)
    # print(t)
    t = g2p.g2p_vi(text, join_str=' ', force_en=True)
    print(t)
