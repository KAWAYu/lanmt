#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gzip
import re
from functools import reduce
from argparse import ArgumentParser


def parse():
    parser = ArgumentParser()
    parser.add_argument("--filepath", "-f", required=True,
                        help="Alignment file path")
    parser.add_argument("--output", "-o", required=True,
                        help="output file path")
    parser.add_argument("--mode", "-m", default="post", choices=["post", "ante", "remove"])
    return parser.parse_args()


def main():
    # M, S, D-L, D-R labeling model
    args = parse()
    gexp = re.compile("\(\{|\}\)")
    with gzip.open(args.filepath, 'rb') as fin, open(args.output, 'w', encoding='utf-8') as fout:
        for line in fin:
            source_word = fin.readline().strip().decode("utf-8").split(' ')
            target_word_align = fin.readline().strip().decode("utf-8")
            target_word_align = re.split(gexp, target_word_align)[:-1]
            null_align = list(map(int, target_word_align[1].strip().split()))
            target_word = target_word_align[2::2]
            target_align = list(map(lambda x: list(map(int, x.strip().split())), target_word_align[3::2]))
            for i in range(len(target_align)):
                if args.mode == 'ante':
                    for na in sorted(null_align):
                        if na - 1 in target_align[i]:  # 求めているアライメント先のindexがあるなら
                            # その後ろにくっつける
                            target_align[i].insert(target_align[i].index(na - 1) + 1, na)
                            break
                elif args.mode == 'post':
                    for na in reversed(sorted(null_align)):
                        if na + 1 in target_align[i]:
                            # その前にくっつける
                            target_align[i].insert(target_align[i].index(na + 1), na)
                            break
                elif args.mode == 'remove':
                    pass  # Null Alignmentに対する処理は何もしなくていい

            source_to_target_indices = [-1 for _ in range(len(source_word))]
            for i, tword_align in enumerate(target_align):
                for ta in tword_align:
                    source_to_target_indices[ta - 1] = i

            prei = 0
            source_to_target_label = ["" for _ in range(len(source_word))]
            for i, si in enumerate(source_to_target_indices):
                if prei == si or prei + 1 == si:
                    source_to_target_label[i] = "M"
                elif prei - 1 == si:
                    source_to_target_label[i] = "S"
                elif prei < si:
                    source_to_target_label[i] = "DR"
                else:
                    source_to_target_label[i] = "DL"
                prei = si

            print(*source_to_target_label, file=fout)


if __name__ == '__main__':
    main()
