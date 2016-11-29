
from __future__ import division
import copy
import random
from permutation_generator import PermutationGenerator
 
def answer(minions):
    """find optimal ordering of minions to minimize expected time
    """
    
    #pack into new tuple to keep track of id counter
    newlist = []
    counter = 0;
    for m in minions:
        time = m[0]
        prob = float(m[1])/float(m[2])
        newlist.append([counter, time, prob])
        counter += 1
        
    # define an ordering based on expected times:
    # t1 + (1 - p1)*t2 < t2 + (1 - p2)*t1
    # t1 - (1 - p2)*t1 < t2 - (1 - p1)*t2
    #            t1*p2 < t2*p1
    #            t1/p1 < t2/p2
    # ordering based on time/prob
    def sortkey(data):
        return data[1]/(data[2])

    # sort based on the sort key, preserves lexical order if sort order is the same
    sorted_minions = sorted(newlist, key = sortkey)
    
    # return order based on original id counter
    output = []
    for m in sorted_minions:
        output.append(m[0])
    return output


def answer2(minions):
    # create a better data structure: id, time, prob
    newlist = []
    counter = 0;
    for m in minions:
        time = m[0]
        prob = 1 - float(m[1])/float(m[2])
        newlist.append([counter, time, prob])
        counter += 1
    #print newlist  
    data = copy.copy(newlist)
    output = order(data)
    return output

def order(data):
    """ do an insertion sort based on expected time 
    """
    
    n = len(data)  
    mysorted = []
    while len(mysorted)<n:
        # choose next and remove from data set
        choice = data.pop(0)
        #choice = choose_max_savings(data)
        if len(mysorted)==0:
            mysorted.append(choice)
        else:
            # find where to insert into sorted
            bestsort = []
            minscore = 0.0
            for insert in range(0,len(mysorted)+1):
                tempsorted = copy.copy(mysorted)
                tempsorted.insert(insert, choice)
                tempscore = score(tempsorted)
                if minscore==0.0 or tempscore<=minscore:
                    minscore = tempscore
                    bestsort = copy.copy(tempsorted)
            # choose best sorted list        
            mysorted = copy.copy(bestsort)
        
        #print "mysorted: %s" % mysorted
        
    output = []
    for s in mysorted:
        output.append(s[0])
        
    return output

def score(data):
    """Compute expected time given a data array (id, time, probablity)
    """
    
    score = 0.0
    prob = 1.0
    for x in data:
        time = x[1]
        score += time*prob
        prob *= x[2]
            
    return score


    

###############################################################################
###############################################################################
  

def test(minions):
    pg = PermutationGenerator(len(minions))
    
    minscore = 0.0
    best = range(0,len(minions))
    while pg.hasmore():
        permutation = pg.getNext()
        #print "perm=%s" % permutation
        score = 0.0
        prob = 1.0
        for i in permutation:
            time = minions[i][0]
            score += time * prob
            prob *= 1.0 - float(minions[i][1])/float(minions[i][2])
            #prob = 1.0 - float(minions[i][1])/float(minions[i][2])
        
        if minscore==0.0 or score<minscore:
            best = copy.copy(permutation)   
            minscore = score 
            
    return best
    
def main(x):
    print "input: %s" % x
    answer1 = answer(x)
    print "answer: %s" % answer1
    test1 = test(x)
    print "test: %s" % test1
    if answer1 != test1:
        print "FAIL"
        return 1
    print "###########################" 
    return 0
    
if __name__ == "__main__":

    
    main([[10, 1, 2], [5, 1, 5]])
  
    main([[5, 1, 5], [10, 1, 2]])
      
    main([[390, 185, 624], [686, 351, 947], [276, 1023, 1024], [199, 148, 250]])
  
    main([[80, 1, 8], [10, 1, 2], [10, 1, 2], [10, 1, 2]])
    main([[10, 1, 2], [80, 1, 8], [10, 1, 2], [10, 1, 2]])
    main([[10, 1, 2], [10, 1, 2], [10, 1, 2], [80, 1, 8]])

    #main([[10, 1, 4], [30, 1, 8], [20, 1, 2]])
    #main([[30, 1, 8], [10, 1, 4], [20, 1, 2]])
    #main([[10, 1, 4], [20, 1, 2], [30, 1, 8]])
    
    
    
    fails = 0 
    for n in range(0, 1000):
        print "TEST %d" % n
        minions = []
        for i in range(0,7):
            time = random.randint(1,1024)
            numer = random.randint(1,1023)
            denom = random.randint(numer+1, 1024)
            minions.append([time, numer, denom])
        fails += main(minions)
    print "ERRORS: %d" % fails 
    
  
