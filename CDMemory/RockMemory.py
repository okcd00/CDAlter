# coding: utf-8
# ==========================================================================
#   Copyright (C) 2020 All rights reserved.
#
#   filename : RockMemory.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-06-19
#   desc     : Utils for Rocksdb
#              Used as a key-value store.
# ==========================================================================
import rocksdb
import itertools
from collections import OrderedDict


class DynamicPrefix(rocksdb.interfaces.SliceTransform):
    def __init__(self, n_gram=None):
        if n_gram is None:
            self.n_gram = 7
        else:
            self.n_gram = n_gram

    def name(self):
        return b'dynamic'

    def transform(self, src):
        return 0, src.split('\x01')[0].__len__()

    def in_domain(self, src):
        return src.split('\x01')[0]

    def in_range(self, dst):
        return len(dst) >= self.n_gram - 1


class AssocCounter(rocksdb.interfaces.AssociativeMergeOperator):
    def __init__(self, n_gram=None):
        if n_gram is None:
            self.n_gram = 7
        else:
            self.n_gram = n_gram

    def merge(self, key, existing_value, value):
        if existing_value:
            s = int(existing_value) + int(value)
            return True, str(s).encode('ascii')
        return True, value

    def name(self):
        return b'AssocCounter'


class NgramDatabase(object):
    # An example for restoring n-gram tokens
    def __init__(self, path=None, n_gram=None, opts=None):
        if path is None:
            path = './cd_rocks.db'
        if n_gram is None:
            n_gram = 7
        if opts is None:
            opts = rocksdb.Options()
            opts.create_if_missing = True
            opts.prefix_extractor = DynamicPrefix(n_gram=n_gram)
            opts.merge_operator = AssocCounter(n_gram=n_gram)

        self.path = path
        self.opts = opts
        self.n_gram = n_gram
        self.db = rocksdb.DB(path, self.opts)

    def put(self, key, value):
        self.db.put(key, value)

    def get(self, key):
        return self.db.get(key)

    def multi_get(self, keys):
        return self.db.multi_get(keys)

    def delete(self, key):
        self.db.delete(key)

    def merge(self, key, value):
        self.db.merge(key, value)

    def iter(self, method='i'):
        # iter can be used as seek[,_to_first, _to_last]
        if method.startswith('k'):
            return self.db.iterkeys()
        elif method.startswith('v'):
            return self.db.itervalues()
        else:  # method.startswith('i'):
            return self.db.iteritems()

    def snapshot(self):
        return self.db.snapshot()

    def backup(self, path):
        # "test.db"
        backup = rocksdb.BackupEngine(path + '/backups')
        backup.create_backup(self.db, flush_before_backup=True)

    def restore(self, path):
        # "test.db"
        backup = rocksdb.BackupEngine(path + '/backups')
        backup.restore_latest_backup(path, path)

    def write(self, batch):
        if isinstance(batch, rocksdb._rocksdb.WriteBatch):
            self.db.write(batch)
        else:
            print("[Error] input is not a valid batch.")
            print("please use rocksdb.WriteBatch().")

    def find_by_context(self, text, n_gram):
        context, target = n_gram.split('\x01')
        it = self.iter('i')
        it.seek(context)

        _case = dict(itertools.takewhile(
            lambda item: item[0].startswith(context), it))
        return OrderedDict(sorted(_case.items(), key=lambda _item: -_item[1]))


if __name__ == '__main__':
    db = NgramDatabase('cd_rocks.db', n_gram=7)
    db.merge('天气不错', '1')
    print(db.get('天气不错'))

