from vn_norm import vn_norm
import argparse
import codecs
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-input", type=str, help="input path", required=True)
    parser.add_argument("-output", type=str, help="out path", required=True)
    args = parser.parse_args()
    file_path = os.path.join(os.getcwd(), args.input)
    content = []
    with codecs.open(file_path, "r", "utf-8") as fid:
        lines = fid.readlines()
        for idx, line in enumerate(lines):
            fix_line = vn_norm(line)
            content.append(fix_line)
            # print(content)
            if idx % 1000 == 0:
                print([idx, fix_line])
    out_path = os.path.join(os.getcwd(), args.output)
    with codecs.open(out_path, 'w', 'utf-8') as f_scp:
        f_scp.write("\n".join(content) + "\n")
        print(['write', out_path, 'file done'])
