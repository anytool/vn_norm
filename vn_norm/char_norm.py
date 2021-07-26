
from unidecode import unidecode
import re

_char_map = {
    # The Greek Alphabet
    'α': 'an pha',
    'β': 'bê ta',
    'γ': 'gam ma',
    'δ': 'đen ta',
    'ε': 'ép si lon',
    'ζ': 'dê ta',
    'η': 'ê ta',
    'θ': 'tê ta',
    'ι': 'i ô ta',
    'κ': 'kap pa',
    'λ': 'lam đa',
    'μ': 'muy',
    'ν': 'nuy',
    'ξ': 'xi',
    'ο': 'ô mic rôn',
    'π': 'pi',
    'ρ': 'rô',
    'ς': 'xích ma',
    'τ': 'tô',
    'υ': 'úp si lon',
    'φ': 'phi',
    'χ': 'si',
    'ψ': 'pờ si',
    'ω': 'ô mê ga',
}

_except = 'ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴĐÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸàáạảãâầấậẩẫăằắặẳẵđèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹ'

def punctuation_norm(text):
    text = re.sub(r'[\?\.!,\-:;\'"]+[\ ]{0,1}(?=[\?\.!,\-:;\'"])', '', text)
    return text

def char_norm(text):
    text = unidecode(text, excepts=_except, override=_char_map)
    return text
