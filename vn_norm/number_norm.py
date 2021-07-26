import re
from roman import fromRoman
from num2words import num2words

_roman_number_re = re.compile(
    r"((phần|tập|chương|mục|bài|phụ lục|kỷ)\W+)([ivxlcdm]+)(\W)")
_vn_number_re = re.compile(r"([0-9][0-9\.]+[0-9\,]+[0-9])")
_vn_dot_number_re = re.compile(r"([0-9][0-9\.]+[0-9])")
_comma_number_re = re.compile(r"([0-9][0-9\,]+[0-9])")
_decimal_number_re = re.compile(r"([0-9]+\.[0-9]+)")
_pounds_re = re.compile(r"£([0-9\,]*[0-9]+)")
_dollars_re = re.compile(r"\$([0-9\.\,]*[0-9]+)")
# _ordinal_re = re.compile(r"[0-9]+(st|nd|rd|th)")
_number_re = re.compile(r"[0-9]+")


def _remove_commas(m):
    return m.group(1).replace(",", "")


def _remove_dot(m):
    return m.group(1).replace(".", "").replace(",", ".")


def _expand_decimal_point(m):
    try:
        num = float(m.group(1))
        return num2words(num, lang='vi')
    except KeyError:
        return m.group(1)


def _expand_dollars(m):
    match = m.group(1)
    parts = match.split(".")
    if len(parts) > 2:
        return match + " đô mỹ"  # Unexpected format
    dollars = int(parts[0]) if parts[0] else 0
    cents = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    if dollars and cents:
        dollar_unit = "đô mỹ" if dollars == 1 else "đô mỹ"
        cent_unit = "sen" if cents == 1 else "sen"
        return "%s %s, %s %s" % (dollars, dollar_unit, cents, cent_unit)
    elif dollars:
        dollar_unit = "đô mỹ" if dollars == 1 else "đô mỹ"
        return "%s %s" % (dollars, dollar_unit)
    elif cents:
        cent_unit = "sen" if cents == 1 else "sen"
        return "%s %s" % (cents, cent_unit)
    else:
        return "không đô"


def _expand_ordinal(m):
    return num2words(m.group(0), lang='vi')


def _expand_number(m):
    num = int(m.group(0))
    return num2words(num, lang='vi')


def _roman_to_int(m):
    try:
        num = fromRoman(m.group(3).upper())
        return m.group(1) + str(num) + m.group(4)
    except:
        return m.group(1) + m.group(3) + m.group(4)

def number_norm(text):
    text = re.sub(_roman_number_re, _roman_to_int, text)
    text = re.sub(_vn_dot_number_re, _remove_dot, text)
    text = re.sub(_vn_number_re, _remove_dot, text)
    text = re.sub(_comma_number_re, _remove_commas, text)
    text = re.sub(_pounds_re, r"\1 pao", text)
    text = re.sub(_dollars_re, _expand_dollars, text)
    text = re.sub(_decimal_number_re, _expand_decimal_point, text)
    # text = re.sub(_ordinal_re, _expand_ordinal, text)
    text = re.sub(_number_re, _expand_number, text)
    return text


if __name__ == '__main__':
    print(number_norm(' phần 6 Lão chương im lặng dịch đến gần Mai Nguyệt, bước ra sau lưng cô.'))
