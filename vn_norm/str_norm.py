import re
import numpy as np

# _unit_map = [
#     # unit
#     (re.compile("([\W0-9])(%s)(\\W)" %
#      x[0], re.IGNORECASE), r"\1 %s \3" % x[1])
#     for x in [
#         ("mm3/s", "mi li mét khối trên giây"),
#         ("cm3/s", "cen ti mét khối mỗi giây"),
#         ("l/min", "lít mỗi phút"),
#         ("km3/s", "kí lô mét khối trên giây"),
#         ("in3/s", "inch khối trên giây"),
#         ("in3/h", "inch khối một giờ"),
#         ("km/h", "kilômét trên giờ"),
#         ("ml/s", "ml mỗi giây"),
#         ("m3/s", "mét khối mỗi giây"),
#         ("m3/h", "mét khối một giờ"),
#         ("mm2", "mi li mét vuông"),
#         ("cm2", "cen ti mét vuông"),
#         ("km2", "kí lô mét vuông"),
#         ("mm3", "mi li mét khối"),
#         ("cm3", "xăng-ti-mét khối"),
#         ("km3", "kí lô mét khối"),
#         ("mwh", "mi li wat giờ"),
#         ("kwh", "kí lô wat giờ"),
#         ("mwh", "mega wat giờ"),
#         ("gwh", "gi ga wat giờ"),
#         ("khz", "kí lô hẹt"),
#         ("mm", "mi li mét"),
#         ("cm", "cen ti mét"),
#         ("km", "kí lô mét"),
#         ("m2", "mét vuông"),
#         ("ha", "héc ta"),
#         ("kg", "kí lô gram"),
#         ("oz", "ounce"),
#         ("lb", "pao"),
#         ("ml", "mi li lít"),
#         ("m3", "mét khối"),
#         ("kb", "kí lô bai"),
#         ("mb", "mê ga bai"),
#         ("gb", "gi ga bai"),
#         ("tb", "tê ra bai"),
#         ("mv", "mi li vôn"),
#         ("kv", "kí lô vôn"),
#         ("kw", "kí lô watt"),
#         ("gw", "gi ga wat"),
#         ("wh", "wat giờ"),
#     ]
# ]

_abbreviations = [
    (re.compile("\\b%s\\." % x[0], re.IGNORECASE), x[1])
    for x in [
        ("mrs", "misess"),
        ("mr", "mister"),
        ("dr", "doctor"),
        ("st", "saint"),
        ("co", "company"),
        ("jr", "junior"),
        ("maj", "major"),
        ("gen", "general"),
        ("drs", "doctors"),
        ("rev", "reverend"),
        ("lt", "lieutenant"),
        ("hon", "honorable"),
        ("sgt", "sergeant"),
        ("capt", "captain"),
        ("esq", "esquire"),
        ("ltd", "limited"),
        ("col", "colonel"),
        ("ft", "fort"),
    ]
]

_punc_map = [
    # unit
    (re.compile(x[0], re.IGNORECASE), x[1])
    for x in [
        ("\.\.\.", "."),
    ]
]

#  _unit_map
_alias_map = np.concatenate((_abbreviations, _punc_map))


def str_norm(text):
    for regex, replacement in _alias_map:
        text = re.sub(regex, replacement, text)
    return text


if __name__ == '__main__':
    # print(re.search(re.compile("(\\bkm/h)^(?!/)(\\W)"), "tốc độ 300 km/h "))
    print(str_norm("mr. peter ...đi xe đạp tốc độ 300 km/h "))
