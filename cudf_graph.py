#!/usr/bin/env python
#
# Copyright 2015
# Johannes K. Fichte, Vienna University of Technology, Austria
#
# cudf_graph.py is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.  cudf_graph.py is
# distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.  You should have received a copy of the
# GNU General Public License along with cudf_graph.py.  If not, see
# <http://www.gnu.org/licenses/>.
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

from cudf_parse import *
from cudf_dep_graph import *

def parse_and_run(f):
    logging.info('Parsing starts')
    p   = Parser()
    try:
        records = p.parse(f)
        logging.info('Parsing done')
        logging.info('Starting graph generation...')
        #G=generate_incidence_graph(records)
        G=generate_dep_graph(records)
        nx.write_gml(G,'test.gml')
        logging.warning('='*80)

        #with transparent_stdout(output) as fh:
        #    for e in horn_backdoor:
        #        fh.write('%s\n' %e)
        #    fh.flush()

    except IOError:
        sys.stderr.write("error reading from: {0}\n".format(f))
        sys.stderr.flush()
        raise IOError


if __name__ == '__main__':
    opts,files=options()
    #if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
    #    parse_and_run(sys.stdin,opts.out,opts.clasp,opts.threads)
    for f in files:
        #sin = fileinput.input(f)
        parse_and_run(f)
    exit(1)
