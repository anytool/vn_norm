
# !/bin/bash
docker run --rm -it -v $PWD/dict:/work phonetisaurus/phonetisaurus "phonetisaurus-apply -m model.fst -wl in.list > out.txt"
