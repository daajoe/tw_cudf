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

from collections import defaultdict
from itertools import chain, ifilter
#combinations,compress,imap, ifilter,izip
import networkx as nx
import matplotlib.pyplot as plt
import re
from verlib import suggest_normalized_version, NormalizedVersion
from distutils.version import LooseVersion

cudf_properties=('conflicts', 'depends', 'provides', 'recommends')
colors={'conflicts': 'red', 'depends': 'blue', 'provides': 'green', 'recommends': 'yellow'}

import operator
class Operators(object):
    str2op = {'': lambda x, y: True, '!=': operator.ne, '<':
              operator.lt, '<=': operator.le, '=': operator.eq, '>=':
              operator.ge, '>': operator.gt}
    
    @staticmethod
    def factory(s):
        return Operators.str2op[s]

regex=re.compile('(\w+)([=<>]*)(\d+)?')
def extract_operator_from_string(e):
    ret = regex.findall(e.replace(' ', ''))[0]
    return ret[0], Operators.factory(ret[1]), ret[2]

def matching_versions(op2,versions, version1):
    return ifilter(lambda x: x is None or op2(LooseVersion(version1),
                                              LooseVersion(x)), versions)

def tuple2str(*t):
    return ','.join(ifilter(lambda x: x is not None, t))

def add(G,e,p,versions):
    try:
        for d in chain.from_iterable(e[p]):
            name2,op2,version2=extract_operator_from_string(d)
            for version2 in matching_versions(op2,versions[name2], e['version']):
                G.add_edge(tuple2str(e['package'],e['version']),tuple2str(name2,version2),property=p, color=colors[p])
    except KeyError:
        pass

def collect_versions(l):
    ret = defaultdict(set)
    for r in l:
        ret[r['package']].add(r['version'])
        if r.has_key('provides'):
            for e in chain.from_iterable(r['provides']):
                #TODO: check with real cudf
                #no versions here
                ret[e].add(None)
    return ret


def generate_dep_graph(l):
    #We ignore upgrade/install tags for now
    p=filter(lambda x: x.has_key('package'), l)
    u=filter(lambda x: x.has_key('request'), l)[0]['upgrade'].split(',')

    G=nx.Graph()
    versions=collect_versions(p)
    for r in p:
        v=(r['package'], r['version'])
        for p in cudf_properties:
            add(G,r,p,versions)
    
    #we try the latest version
    versions={}
    for e in u:
        print e
    #desc = 
    plt.savefig('test.png')
    return G
