# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from torchtext.data.example import Example
from torchtext.data import Dataset


class ReorderingBilingualDataset(Dataset):

    def __init__(self, src_path, tgt_path, reorder_path,
                 src_field, tgt_field, reorder_field, **kwargs):
        fields = {
            "src": ("src", src_field),
            "tgt": ("tgt", tgt_field),
            "order": ("order", reorder_field)
        }
        examples = []
        for src, tgt, reorder in zip(open(src_path, encoding="utf-8"), open(tgt_path, encoding="utf-8"),
                                     open(reorder_path, encoding="utf-8")):
            example = Example.fromdict(
                {"src": src.strip(), "tgt": tgt.strip(), "order": reorder.strip()},
                fields
            )
            examples.append(example)

        if isinstance(fields, dict):
            fields, field_dict = [], fields
            for field in field_dict.values():
                if isinstance(field, list):
                    fields.extend(field)
                else:
                    fields.append(field)

        super(ReorderingBilingualDataset, self).__init__(examples, fields, **kwargs)
