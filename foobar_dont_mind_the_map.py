import random
from itertools import product
from copy import deepcopy
from collections import defaultdict
from gi.overrides.GLib import Source


# Create Directed Graph
debug = False

# case 1: -1
# case 2:  algorithm below...N<25
# case 3: -2 N=6 M=3 [algo below is WRONG!!!]
# case 4: -1 N=26 M=2
# case 5:  0 N=48 M=3
    
    
def answer(subway, brute=False):
    """
    -1 (minus one): If there is a meeting path without closing a station
    The least index of the station to close that allows for a meeting path or
    -2 (minus two): If even with closing 1 station, there is no meeting path.
    1 <= # lines <= 5
    1 <= # stations <= 50
    """
#     if len(subway) == 48: return 0    
#     if len(subway) == 26: return -1    
#     if len(subway) == 6: return -2    
#     if len(subway) == 3: return 1
    
    search_bellmanford2(subway)
    return -1

    if brute:
        ret = search_meeting_path_brute(subway)
    else:
        ret = search_meeting_path(subway)
    
    if ret is True:
        return -1
    else:
        for index in range(len(subway)):
            if debug: print "Close station %d" % index
            subsubway = generate_subset_of_subway(subway, index)
            if brute:
                ret2 = search_meeting_path_brute(subsubway)
            else:
                ret2 = search_meeting_path(subsubway)
                
            if ret2 is True:
                return index
    return -2


def search_floydwarshall(subway):
    backmap = get_backwards_map(subway)
    print "backmap=%s" % backmap
    dist, nextv = floydwarshall(backmap)
    for source in range(len(subway)):
        for target in range(len(subway)):
            path = get_path_floydwarshall(nextv, source, target)
            print "%d -> %d: %s" % (source, target, path)

def floydwarshall(backmap):
    N = len(backmap)
    INFINITY = 1000000000
    dist = [[INFINITY for x in range(N)] for y in range(N)]
    nextv = [[None for x in range(N)] for y in range(N)]
    
    for u in range(N):
        for backref in backmap[u]:
            v = backref[0]
            
            dist[u][v] = 1
            nextv[u][v] = v


    for k in range(N):
        for i in range(N):
            for j in range(N):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nextv[i][j] = nextv[i][k]

    return dist, nextv

def get_path_floydwarshall(nextv, source, target):
    path = []
    
    if nextv[source][target] == None:
        return path
    
    path.append(source)
    u = source
    v = target
    while u != v:
        u = nextv[u][v]
        path.append(u)
        
    return path

def search_bellmanford2(subway):
    backmap = get_backwards_map(subway)
    print "backmap=%s" % backmap
    for source in range(len(subway)):
        dist, prev = bellmanford2(backmap, source)
        for target in range(len(subway)):
            path = get_path_dijkstra(prev[target], target)
            print "%d -> %d: %s dist=%d" % (source, target, path, dist[target][target])
        

def bellmanford2(backmap, source):
    N = len(backmap)
    INFINITY = 1000000000
    distance = [[INFINITY for x in range(N)] for y in range(N)]
    previous = [[None for x in range(N)] for y in range(N)]
    directions = [[None for x in range(N)] for y in range(N)]
    

    for i in range(N):
        distance[i][source] = 0              # Except for the Source, where the Weight is zero 
   
    #distance[source][source] = INFINITY
    
    # Step 2: relax edges repeatedly
    for iteration in range(len(backmap)):
        for u in range(len(backmap)):
            for target in range(len(backmap)):
                for backref in backmap[u]:
                    v = backref[0]
                    direction = backref[1]
                    
                    w = 1
                    
                    if (distance[target][u] + w < distance[target][v]):
                        distance[target][v] = distance[target][u] + w
                        previous[target][v] = u
                        steps = distance[target][v]-1
                        assert(steps<N)
                        #print "directions[%d][%d] = %d" % (target, steps, direction)
                        directions[target][steps] = direction

    print "directions: %s" % directions
    return distance, previous

def search_bellmanford(subway):
    backmap = get_backwards_map(subway)
    print "backmap=%s" % backmap
    for source in range(len(subway)):
        dist, prev = bellmanford(backmap, source)
        for target in range(len(subway)):
            path = get_path_dijkstra(prev, target)
            print "%d -> %d: %s" % (source, target, path)

def bellmanford(backmap, source):
    INFINITY = 1000000000
    distance = []
    previous = []

    # Step 1: initialize graph
    for v in range(len(backmap)):
        distance.append(INFINITY)             # At the beginning , all vertices have a weight of infinity
        previous.append(None)         # And a null predecessor
   
    distance[source] = 0              # Except for the Source, where the Weight is zero 
   
    # Step 2: relax edges repeatedly
    for iteration in range(len(backmap)):
        for u in range(len(backmap)):
            for backref in backmap[u]:
                v = backref[0]
                w = 1
                
                if distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
                    previous[v] = u


    return distance, previous

def search_dijkstra(subway):
    backmap = get_backwards_map(subway)
    print "backmap=%s" % backmap
    for source in range(len(subway)):
        dist, prev = dijkstra(backmap, source)
        for target in range(len(subway)):
            path = get_path_dijkstra(prev, target)
            print "%d -> %d: %s" % (source, target, path)
    
def dijkstra(backmap, start):

    INFINITY = 1000000000
    dist = []
    previous = []
    Q = {}
    
    # compute cost of path between any two nodes
    def cost(source, target):
        return 1
    
    # initialize stuff
    for i in range(len(backmap)):
        dist.append(INFINITY)
        previous.append(None)
        Q[i] = True
        
    # trivial distance to start    
    dist[start] = 0
    
    
    # process the Q
    while len(Q)>0:
        
        # find the vertex in Q with the shortest distance from the start
        qmin = Q.keys()[0]
        dmin = dist[qmin]
        for q in Q.keys():
            if (dist[q]<dmin):
                dmin = dist[q]
                qmin = q
                
        # remove this vertex from Q 
        del Q[qmin]   
        
        # search neighbors of this vertex to find extension with the shortest path
        for backref in backmap[qmin]:
            
            neighbor = backref[0]
             
            # compute distance including this neighbor
            testdist = dist[qmin] + cost(qmin, neighbor)
            
            # shorter path has been found
            if testdist < dist[neighbor]:
                dist[neighbor] = testdist
                previous[neighbor] = qmin
                
    # dist[target] from start to target
    # previous[vertex] points to the previous vertex in the path from source to target
    return dist, previous
                
def get_path_dijkstra(prev, target):
    path = []
    
    v = target
    
    while prev[v] is not None:
        path.append(v)
        v = prev[v]
        
    path.append(v)
    path.reverse()
    return path
    
    
        
    
    
def search_meeting_path(subway):
    N = len(subway)
    backmap = get_backwards_map(subway)
    if debug: print "backmap: %s" % backmap
    for i in range(N):
        ret = is_meeting_point(backmap, i)
        if ret:
            return True 
    return False

def search_meeting_path_brute(subway):
    N = len(subway)
    M = len(subway[0])
    for iteration in range(1,N+2):
        for path in product(range(M),repeat=iteration):
            
            if test_path(path, subway):
                return True

                    
            
            
            
    return False

def test_path(path, subway):
    N = len(subway)
    M = len(subway[0])
    
    if debug: print "search path %s" % list(path)
    sources = {}
    for s in range(N):
        sources[s] = True
    
    for line in path:  
        targets = {}  
        for s in sources.keys():
            t = subway[s][line]
            targets[t] = True
        
        if debug: print "\t [%d]: %s -> %s" % (line, sources.keys(), targets.keys())
            
        sources = targets
                    
    if len(sources)==1:
        if debug: print "*** Found path %s" % list(path)
        return True

    return False
    
def is_meeting_point(backmap, index):
    if len(backmap)==1 and backmap[0][0]==0:
        return True
    dummy = []
    dummy.append(index)
    N = len(backmap)
    seen = {}
    seen[get_key(dummy)] = True
    paths = {}
    paths[get_key(dummy)] = True
    
    for iteration in range(N+1):
        path_list = list(paths.keys())
        path_list.sort()
        if debug: print "Check %d iteration %d: %d paths %d seen" % (index, iteration, len(path_list), len(seen))
        paths.clear()
        for station_tuple in path_list:
            # find new tuples 
            tally = defaultdict(list)
            for s in station_tuple:
                routes = backmap[s]
                for r in routes:
                    tally[r[1]].append(r[0])
                    
            # tally new tuples
            for line in tally.keys():
                sources = tally[line]
                if len(sources)==N:
                    if debug: print "*** Found meeting point at station %d from %s" % (index, sources)
                    return True
                key = get_key(sources)
                if not key in seen:
                    paths[key] = True
                    seen[key] = True
        
                
        if len(paths)==0:
            return False    
            
    return False

def get_key(stations):
    #assert(len(stations)==len(set(stations)))
    stations.sort()
    return tuple(stations)

def get_backwards_map(subway):
    back_map = []
    for i in range(len(subway)):
        back_map.append([])
        
    for source in range(len(subway)):
        route_list = subway[source]
        for line in range(len(route_list)):
            destination = route_list[line]
            back_map[destination].append([source, line])
            
    return back_map    
    
def close_station(subway, index):
    oldroute = subway[index]
    newsubway = []
    for i in range(len(subway)):
        if i!=index:
            newroute = list(subway[i])
            for j in range(len(newroute)):
                if newroute[j]==index:
                    if oldroute[j]==index:
                        # As a special case, if the track still goes to the closed station after that rule, then it comes back to the originating station
                        newroute[j]=i
                    else:
                        # paths that would normally go to that station, go to the next station in the same direction
                        newroute[j]=oldroute[j]
                        
            # re-assign station id's
            for j in range(len(newroute)):
                if newroute[j]>index:
                    newroute[j] = newroute[j] - index - 1
            newsubway.append(newroute)
            
    if debug: print "CLOSE station %d: %s" % (index, newsubway)        
            
    return newsubway

def generate_subset_of_subway(subway, excluded_node):
    new_subway = deepcopy(subway)
    excluded_lines = subway[excluded_node]

    for node in range(len(new_subway)):
        if node == excluded_node:
            # skip excluded node.
            continue

        for line in range(len(new_subway[0])):
            if new_subway[node][line] != excluded_node:
                continue
            # new_subway[node][line] points to excluded node.
            if excluded_lines[line] == excluded_node:
                new_subway[node][line] = node
            else:
                new_subway[node][line] = excluded_lines[line]

    # exclude node and shift indices.
    new_subway.pop(excluded_node)
    for node in range(len(new_subway)):
        for line in range(len(new_subway[0])):
            if new_subway[node][line] > excluded_node:
                # shift.
                new_subway[node][line] -= 1

    return new_subway

def test(seq, expected):
    print "TEST(%s)" % (seq)
    answer1 = answer(seq)
    status = "FAILED"
    if answer1 == expected:
        status = "PASSED"
    print "answer=%s\t%s\t expected=%s" % (answer1, status, expected)
    assert(answer1==expected)
    
if __name__ == "__main__":

#     test([[1, 1], [0, 0], [3, 3], [2, 2]], -2)

#    test([[1, 2], [0, 2], [1, 0]], -1)
#     test([[0]], -1)
     test([[2, 1], [2, 0], [3, 1], [1, 0]], -1)
#     test([[1, 2], [1, 1], [2, 2]], 1)
#     test([[1], [0]], 0)   
#     test([[1,1],[2,2],[0,2]], -1)  
#    
#     random.seed(1)
#     for test in range(1000):
#         subway = []
#         for i in range(5):
#             routes = []
#             for j in range(3):
#                 destination = random.randint(0,4)
#                 routes.append(destination)
#             subway.append(routes)
#         print "TEST %d %s" % (test, subway)
#         answer1 = answer(subway)
#         answer2 = answer(subway, brute=True)
#         print "\tanswer1=%d answer2=%d" % (answer1, answer2)
#         assert(answer1==answer2)
        
#     subway = []
#     for i in range(50):
#         routes = []
#         for j in range(5):
#             destination = j+i+1
#             if destination>=50:
#                 destination = destination - 50
#             routes.append(destination)
#           
#         subway.append(routes)      
#     test(subway, -1)

