#!/usr/bin/env python
#
# Copyright 2015
# Johannes K. Fichte, Vienna University of Technology, Austria
#
# cudf_incidence_graph.py is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# cudf_incidence_graph.py is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.  You should have received a
# copy of the GNU General Public License along with
# cudf_incidence_graph.py.  If not, see
# <http://www.gnu.org/licenses/>.
#

import logging
logging.config.fileConfig('logging.conf')

from itertools import combinations,compress,imap, ifilter,izip
import networkx as nx

def generate_incidence_graph(l):
    G=nx.Graph()
    i=0
    raise NotImplemented
    for r in l:
        print r

    for r in l.statements:
        if isinstance(r,Rule):
            for a in r.head:
                G.add_edge(a,i)
            for a in imap(lambda x: abs(x), r.body):
                G.add_edge(a,i)
        elif isinstance(r,Constraint):
            G.add_edge(r.head,i)
            for x in imap(lambda x: abs(x), r.body):
                G.add_edge(x,i)
            for x,y in combinations(imap(lambda x: abs(x), r.body),2):
                G.add_edge(x,y)
        elif isinstance(r,Minimize):
            logging.warning('Minimization rule at line %i ignored' %i)
        else:
            raise TypeError('Not handled yet. Line %i' %i)
        i+=1
    return G
    

