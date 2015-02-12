#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# Copyright 2014 Andrés Mantecon Ribeiro Martano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
# ----------------------------------------------------------------------------

import os
import sys
from datetime import datetime as dt
import hashlib



def sha1sum(filename):
    h = hashlib.sha1()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * h.block_size), b''):
            h.update(chunk)
    return h.hexdigest()


def modification_date(filename):
    t = os.path.getmtime(filename)
    return dt.fromtimestamp(t)


class Hasher(object):

    def __init__(self, dirpath, hashes_filename="hashes.txt"):
        self.date_format = "%d/%m/%Y-%H:%M:%S"

        self.dirpath = dirpath
        self.hashes_filename = hashes_filename
        self.hashes_filepath = os.path.join(self.dirpath, hashes_filename)

        self.prev_date = None
        self.this_date = None
        self.hashes = {}

    def set_current_date(self):
        self.this_date = dt.now()

    def modified_file(self, filepath):
        if (not self.prev_date) \
           or (self.prev_date < modification_date(filepath)):
            return True
        else:
            return False

    def parse_hashes_file(self):
        with open(self.hashes_filepath, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            items = lines[:-3]
            self.prev_date = dt.strptime(lines[-2], self.date_format)
            for item in items:
                hashe, _, filename = [i.strip() for i in item.partition(' ')]
                self.hashes[filename] = hashe

    def write_hashes_file(self):
        with open(self.hashes_filepath, 'w') as f:
            for filename, hashe in sorted(self.hashes.items()):
                line = "{hashe}  {filename}\n"\
                    .format(hashe=hashe, filename=filename)
                f.write(line)
            footer = "\n{date}\nSHA1\n"\
                     .format(date=self.this_date.strftime(self.date_format))
            f.write(footer)

    def process_dir(self):
        try:
            self.parse_hashes_file()
        except IOError:
            pass
        self.set_current_date()
        for item in os.listdir(self.dirpath):
            filepath = os.path.join(self.dirpath, item)
            if os.path.isfile(filepath)\
               and item != self.hashes_filename\
               and (self.modified_file(filepath)
                    or item not in self.hashes):
                    print("Hashing: %s" % item)
                    self.hashes[item] = sha1sum(filepath)
        self.write_hashes_file()


dirpath = sys.argv[1]
Hasher(dirpath).process_dir()
