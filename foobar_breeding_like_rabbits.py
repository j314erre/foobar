
memoize_r = {}

def answer(str_S):
    """ given the base-10 string representation of an integer S, returns the largest n such that R(n) = S. 
    Return the answer as a string in base-10 representation. 
    If there is no such n, return "None". 
    S will be a positive integer no greater than 10^25
        R(0) = 1
        R(1) = 1
        R(2) = 2
        R(2n) = R(n) + R(n + 1) + n (for n > 1)
        R(2n + 1) = R(n - 1) + R(n) + 1 (for n >= 1)    
    """
    S = long(str_S)
    if S==1:
        return "1"
    if S==2:
        return "2"
    if S==3:
        return "3"
    
    max = 10000000000000000000000000
    
     
    # search odd first will give the biggest n
    upper = max
    lower = 0
    last = 0
    while upper >= lower:
        middle = (upper + lower + 1) // 2
        if middle == last:
            break
        last = middle
        test = R(2*middle+1)
        #print "odd middle=%d" % middle
        if test>S:
            upper = middle
        elif test<S:
            lower = middle
        else:
            return "%s" % (2*middle+1)
    
    # search even which is always bigger
    upper = max
    lower = 0
    last = 0
    while upper >= lower:
        middle = (upper + lower + 1) // 2
        if middle == last:
            break
        last = middle
        test = R(2*middle)
        #print "even middle=%d upper=%d lower=%d test=%d" % (middle, upper, lower, test)
        if test>S:
            upper = middle
        elif test<S:
            lower = middle
        else:
            return "%s" % (2*middle)


    return "None"

def R(n):
    """ Use recursive formula with memoization to compute for very large values
        
    """
    key = "%s" % n
    if key in memoize_r:
        return memoize_r[key]

    ret = 1
    if n == 0:
        ret = 1
    elif n == 1:
        ret = 1
    elif n == 2:
        ret = 2
    elif n % 2 == 0:
        halfn = n/2
        ret = R(halfn) + R(halfn + 1) + halfn
    else:
        halfn = n//2
        ret = R(halfn-1) + R(halfn) + 1
        
    memoize_r[key] = ret
    return ret
    
def answer_brute(str_S):
    """ given the base-10 string representation of an integer S, returns the largest n such that R(n) = S. 
    Return the answer as a string in base-10 representation. 
    If there is no such n, return "None". 
    S will be a positive integer no greater than 10^25
        R(0) = 1
        R(1) = 1
        R(2) = 2
        R(2n) = R(n) + R(n + 1) + n (for n > 1)
        R(2n + 1) = R(n - 1) + R(n) + 1 (for n >= 1)    
    """
    
    S = long(str_S)


    if S==1:
        return "1"
    if S==2:
        return "2"
    if S==3:
        return "3"
        
    R = [-1000000 for i in range(100000)]

    R[0] = 1
    R[1] = 1
    R[2] = 2
    n = 1
    R[2*n+1] = R[n-1] + R[n] + 1
    
    
    ret = "None"
    for n in range(2,len(R)/2):
        R[2*n] = R[n] + R[n+1] + n
        R[2*n+1] = R[n-1] + R[n] + 1
        #print "R[%d]=%d" % (2*n, R[2*n])
        #print "R[%d]=%d" % (2*n+1, R[2*n+1])
        
        if R[2*n] == S:
            ret = "%s" % (2*n)
        if R[2*n+1] == S:
            return "%s" % (2*n+1)
        if R[2*n+1] > S:
            return ret
        
    # return as string 
    return "ERROR R[%d]=%d" % (2*n, R[2*n]);    

###############################################################################
###############################################################################



def test(seq, expected):
    print "TEST(%s)" % (seq)
    answer1 = answer(seq)
    status = "FAILED"
    if answer1 == expected:
        status = "PASSED"
    print "answer=%s\t%s" % (answer1, status)
    
if __name__ == "__main__":

    for n in range(1000):
        s = "%s" % n
        answer1 = answer(s)
        answer2 = answer_brute(s)
        print "R(%d)=%s %s" % (n, answer1, answer2)
        if answer1 != answer2:
            break

    test("7", "4")
    test("100", "None")
    test("210", "80")
    test("10000000000000000000000000", "None")
 

