#!/usr/bin/env python
#
# Copyright 2015
# Johannes K. Fichte, Vienna University of Technology, Austria
#
# cudf_parse.py is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.  cudf_parse.py is
# distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.  You should have received a copy of the
# GNU General Public License along with cudf_parse.py.  If not, see
# <http://www.gnu.org/licenses/>.
#
# Uses sippets by 
# Pietro Abate <http://mancoosi.org/~abate/easy-cudf-parsing-python>
#
import logging
import select
import logging.config
logging.config.fileConfig('logging.conf')

from signal_handling import *

import sys
import optparse
import fileinput
from StringIO import StringIO

def options():
    usage  = "usage: %prog [options] [files]"
    parser = optparse.OptionParser(usage=usage)
    #parser.add_option("-o", "--output", dest="out", type="string", help="Output file", default=None)
    opts, files = parser.parse_args(sys.argv[1:])
    return opts, files


from itertools import groupby

class Parser:
    cnf_fields = ['conflicts','depends','provides','recommends']

    @staticmethod
    def cnf(k,s) :
        if k in Parser.cnf_fields:
            l = s.split(',')
            ll = map(lambda s : s.split('|'), l)
            return ll
        else:
            return s


    def parse(self,filename):
        records = []
        request = []
        with open(filename) as f:
            for empty, record in groupby(f, key=str.isspace):
                if not empty:
                    l = map(lambda s : s.split(': '), record)
                    # we ignore the preamble here ...
                    if 'preamble' not in l[0]:
                        pairs = ([k, Parser.cnf(k,v.strip())] for k,v in l)
                        records.append(dict(pairs))
        #print records
        return records

class Application:
    def run(self):
        opts, files = options()

        p   = Parser()
        #sin = fileinput.input(files)
        try:
            #TODO
            l = p.parse(files[0])
            for i in l:
                print i
        except IOError:
            sys.stderr.write("error reading from: {0}\n".format(sin.filename()))
            sys.stderr.flush()
            return 1

if __name__ == "__main__":
	sys.exit(Application().run())
