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

#TODOS:
#testcase versions, minus, etc.
#check for special caracters in real world examples


import logging
logging.config.fileConfig('logging.conf')

from collections import defaultdict
from itertools import chain, ifilter, imap
import networkx as nx
#import matplotlib.pyplot as plt
import re
from verlib import suggest_normalized_version, NormalizedVersion
from distutils.version import LooseVersion

cudf_properties=('conflicts', 'depends', 'provides', 'recommends')
dc={'red': '#993300', 'blue': '#0000ff', 'green': '#00ff00', 'black':
    '#000000', 'yellow': '#ffff00', 'dark_yellow': '#FFCC00', 'gray':
    '#c0c0c0', 'orange': '#ffcc99', 'mint': '#ccffff'}
edge_colors={'conflicts': 'red', 'depends': 'blue', 'provides': 'green',
        'recommends': 'yellow', 'implicit': 'black'}
node_colors={'default': 'dark_yellow', 'installed': 'gray', 'goal':
             'orange', 'relevant': 'mint'}


import operator
class Operators(object):
    str2op = {'': operator.is_, '!=': operator.ne, '<':
              operator.lt, '<=': operator.le, '=': operator.eq, '>=':
              operator.ge, '>': operator.gt}
    
    @staticmethod
    def factory(s):
        return Operators.str2op[s]

regex=re.compile('([\w\-_]+)([=<>]*)(\d+)?')
def extract_operator_from_string(e):
    ret = regex.findall(e.replace(' ', ''))[0]
    return ret[0], Operators.factory(ret[1]), ret[2] if ret[2] else None

def matching_versions(op2,versions, version1):
    return ifilter(lambda x: x is None or op2(LooseVersion(version1),
                                              LooseVersion(x)), versions)

def tuple2str(*t):
    return ','.join(ifilter(lambda x: x is not None, t))

def direction(u,v,p):
    return (u,v) if p != 'provides' else (v,u)

def gml_edge_graphics(x):
    return [{'fill': dc[edge_colors[x]], 'targetArrow': 'standard'}]

def gml_node_graphics(x):
    return [{'w': 120.0, 'type': 'rectangle', 'fill': dc[node_colors[x]], 'outline': '#000000'}]

def add(G,e,p,versions):
    try:
        for d in chain.from_iterable(e[p]):
            name2,op2,version2=extract_operator_from_string(d)
            for version2 in matching_versions(op2,versions[name2], version2):
                u, v = direction(tuple2str(e['package'],e['version']),tuple2str(name2,version2),p)
                G.add_edge(u,v,property=p, graphics=gml_edge_graphics(p), color=edge_colors[p])
    except KeyError:
        pass

def collect_versions(l):
    ret = defaultdict(lambda: set([None]))
    for r in l:
        ret[r['package']].add(r['version'])
        #TODO
        if r.has_key('provides'):
            for e in chain.from_iterable(r['provides']):
                #TODO: check with real cudf
                #no versions here
                ret[e].add(None)
    return ret

def installed_iter(l):
    return ifilter(lambda x: x.has_key('installed'),l)

def color_nodes(G,p,u,r):
    for e in G.nodes_iter():
        G.node[e]['graphics']=gml_node_graphics('default')
    for e in r:
        G.node[e]['graphics']=gml_node_graphics('relevant')
    for e in imap(lambda x: tuple2str(x['package'], x['version']),installed_iter(p)):
        G.node[e]['graphics']=gml_node_graphics('installed')
    for e in u:
        G.node[e]['graphics']=gml_node_graphics('goal')

def generate_dep_graph(l,filename, preprocessing=True, colors=True, write_gml=True):
    p=filter(lambda x: x.has_key('package'), l)
    #TODO: handling of install tags
    u=map(lambda x: x.strip(), filter(lambda x: x.has_key('request'), l)[0]['upgrade'].split(','))

    G=nx.DiGraph()
    versions=collect_versions(p)

    #****************************************************************************************
    #ADD DEPENDENCIES
    #****************************************************************************************
    #implicit
    for e in versions:
        if len(versions[e])>1:
            for v in ifilter(lambda x: x is not None, versions[e]):
                G.add_edge(tuple2str(e,None),tuple2str(e,v),property='implict',
                           graphics=gml_edge_graphics('implicit'))
    #explicit
    for r in p:
        v=(r['package'], r['version'])
        for cudf_property in cudf_properties:
            add(G,r,cudf_property,versions)

    if preprocessing:
        #****************************************************************************************
        #COLLECT RELEVANT VERSIONS
        #****************************************************************************************
        relevant_versions=[]
        for e in u:
            e=e.strip()
            if versions[e]:
                #TODO
                #tuple2str(e,reduce(lambda x,y: x if LooseVersion(x)>
                #         LooseVersion(y) else y, versions[e]))
                relevant_versions.append(e)
            else:
                relevant_versions.append(tuple2str(e,versions[e]))

        successors=set()
        for v in relevant_versions:
            ret = []
            for e,k in nx.dfs_successors(G,v).iteritems():
                ret.append(e)
                ret.extend(k)
            successors.update(ret)
        G=G.subgraph(list(successors)).copy()

        if colors:
            color_nodes(G,p,u,successors)
    if write_gml:
        nx.write_gml(G,filename)
    return G
