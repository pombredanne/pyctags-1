#!/usr/bin/env python
## Copyright (C) 2008 Ben Smith <benjamin.coder.smith@gmail.com>

##    This file is part of pyctags.

##    pyctags is free software: you can redistribute it and/or modify
##    it under the terms of the GNU Lesser General Public License as published
##    by the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.

##    pyctags is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.

##    You should have received a copy of the GNU Lesser General Public License
##    and the GNU Lesser General Public Licens along with pyctags.  If not, 
##    see <http://www.gnu.org/licenses/>.


import sys

from pyctags import exuberant_ctags, ctags_file
from pyctags.harvesters import name_lookup_harvester, by_name_harvester
import os

source_files = list()

for (dirpath, dirs, files) in os.walk("../"):
    for f in files:
        if f[-3:] == '.py':
            source_files.append(os.path.join(dirpath, f))

generator = exuberant_ctags(files=source_files)
list_o_tags = generator.generate_tags(generator_options={'--fields' : '+n'})

names = name_lookup_harvester()
by_name = by_name_harvester()
tagfile = ctags_file(list_o_tags, harvests=[names, by_name])

print ("Found %d tags in %d source files." % (len(tagfile.tags), len(source_files)))

# this fetches unique names
letter_tags = names.starts_with('c')
print ("%d individual names start with the letter c." % (len(letter_tags)))
by_name_tags = by_name.retrieve_data()

for t in letter_tags:
    # there can be more than one occurance of a particular name
    for t2 in by_name_tags[t]:
        print ("\t%s is in %s on line %s." % (t2.name, t2.file, t2.line_number))
