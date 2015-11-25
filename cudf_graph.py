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
    usage  = 'usage: %prog [options] [files]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--no_preprocessing', dest='preprocessing',
                      action='store_false', help='Deactivate simple preprocessing', default=True)
    parser.add_option('--no_colors', dest='colors',
                      action='store_false', help="Do not color output graph", default=True)
    parser.add_option('--no_gml', dest='write_gml',
                      action='store_false', help='Do not write gml output file', default=True)
    parser.add_option('--gml_output', dest='gml_filename',
                      type='string', help='GML output filename',
                      default='filename.gml')
    opts, files = parser.parse_args(sys.argv[1:])
    return opts, files

from cudf_parse import *
from cudf_dep_graph import *

def parse_and_run(f,gml_filename,preprocessing, colors,write_gml):
    logging.info('Parsing starts')
    p   = Parser()
    try:
        records = p.parse(f)
        logging.info('Parsing done')
        logging.info('Starting graph generation...')
        G=generate_dep_graph(records, filename=gml_filename,
                             preprocessing=preprocessing, colors=colors,
                             write_gml=write_gml)
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
        if opts.gml_filename == 'filename.gml':
            opts.gml_filename='%s.gml' %f
        #sin = fileinput.input(f)
        #TODO commandline parameters
        parse_and_run(f,
                      gml_filename=opts.gml_filename,preprocessing=opts.preprocessing,
                      colors=opts.colors,write_gml=opts.write_gml)
    exit(0)
