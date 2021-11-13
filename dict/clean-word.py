from vn_norm import vn_norm
import argparse
import codecs
import os
from vn_norm import vn_norm
from underthesea import word_tokenize, sent_tokenize

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-input", type=str, help="input path", required=True)
    parser.add_argument("-output", type=str, help="out path", required=True)
    args = parser.parse_args()
    file_path = os.path.join(os.getcwd(), args.input)
    dictMap = dict()
    with codecs.open(file_path, "r", "utf-8") as fid:
        lines = fid.readlines()
        for idx, line in enumerate(lines):
            if idx % 1000 == 0:
                print([idx, line])
            sents = sent_tokenize(line)
            for sent in sents:
                depends = word_tokenize(sent)
                for depend in depends:
                    depend = depend.lower()
                    sent = vn_norm(depend)
                    words = depend.split()
                    for word in words:
                        if word not in dictMap:
                            dictMap[word] = word
    out_path = os.path.join(os.getcwd(), args.output)
    with codecs.open(out_path, 'w', 'utf-8') as f_scp:
        for key in dictMap:
            f_scp.write(f"{dictMap[key]}\n")
        print(['write', out_path, 'file done'])
