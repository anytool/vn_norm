
__version__ = '0.0.1'

from vn_norm.chuan_hoa_dau_cau import chuan_hoa_dau_cau
from vn_norm.str_norm import str_norm
from vn_norm.char_norm import char_norm
from vn_norm.number_norm import number_norm


def vn_norm(text: str) -> str:
    text = ' ' + text.lower() + ' '
    text = chuan_hoa_dau_cau(text)
    text = char_norm(text)
    text = str_norm(text)
    text = number_norm(text)
    return text.strip()


if __name__ == '__main__':
    text = """
phần I, chương XIV, giới thiệu về  β.
mr. peter đi xe đạp tốc độ 300 km/h
    """
    print(vn_norm(text))
