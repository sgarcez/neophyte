import json
from collections import defaultdict

from .decorators import ensure_graph


@ensure_graph
def neighbours(graph, entities):
    '''
    :returns: a dict where each item is: `id0: [id1, id2, id3]`
    denoting the ids that are 1 hop away from id0.
    the relationships are mapped both ways.
    '''
    Q = '''
    MATCH (l:`http://sme.sh/ontology/Node`)--(r:`http://sme.sh/ontology/Node`)
    WHERE l.id IN {entities}
    AND r.id IN {entities}
    RETURN l.id, r.id
    '''
    jentities = json.dumps(entities)
    query = Q.format(entities=jentities)
    record_list = graph.cypher.execute(query).records
    results = defaultdict(list)
    for record in record_list:
        results[record['l.id']].append(record['r.id'])
    return results


@ensure_graph
def distances(graph, entities, max_hops=5):
    Q = '''
    MATCH
    (l:`http://sme.sh/ontology/Node`{{id: "{left}"}}),
    (r:`http://sme.sh/ontology/Node`{{id: "{right}"}}),
    p = shortestPath((l)-[*..{max_hops}]-(r))
    RETURN length(p)
    '''
    results = defaultdict(dict)
    for l in entities:
        for r in entities:
            if l == r:
                continue
            query = Q.format(left=l, right=r, max_hops=max_hops)
            res = graph.cypher.execute(query)
            results[l][r] = results[r][l] = res.one
    return results


@ensure_graph
def out_degrees(graph, entities):
    Q = '''
    MATCH (l:`http://sme.sh/ontology/Node`)-->()
    WHERE l.id IN {entities}
    RETURN l.id, COUNT(r)
    '''
    jentities = json.dumps(entities)
    query = Q.format(entities=jentities)
    record_list = graph.cypher.execute(query).records
    results = {}
    for record in record_list:
        results[record[0]] = record[1]
    return results


@ensure_graph
def in_degrees(graph, entities):
    Q = '''
    MATCH (l:`http://sme.sh/ontology/Node`)<--()
    WHERE l.id IN {entities}
    RETURN l.id, COUNT(r)
    '''
    jentities = json.dumps(entities)
    query = Q.format(entities=jentities)
    record_list = graph.cypher.execute(query).records
    results = {}
    for record in record_list:
        results[record[0]] = record[1]
    return results
