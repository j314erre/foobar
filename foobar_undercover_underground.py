
memoize_binomial = {}
memoize_q = {}

def answer(N, K):
    """ returns the number of ways to connect N distinctly Nodes with exactly K edges
    http://oeis.org/A123527
    http://oeis.org/A062734 Triangular array T(n,k) giving number of connected graphs with n labeled nodes and k edges (n >= 1, n-1 <= k <= n(n-1)/2)
    """
    T_n_k = q(N, K)
    
    # return as string 
    return "%s" % T_n_k;    

def q(n,k):
    """ Use recursion with memoization
        http://math.stackexchange.com/questions/689526/how-many-connected-graphs-over-v-vertices-and-e-edges
    """
    key = "q(%d,%d)" % (n, k)
    if key in memoize_q:
        return memoize_q[key]
    
    cutoff = binomial(n-1, 2) 
    ret = 0
    if k<n-1 or k>n*(n-1)/2:
        ret = 0
    elif k == n - 1:
        x = 1
        for i in range(n-2):
            x *= n
        ret = x
    elif k > cutoff:
        combos = binomial(n, 2)
        x = binomial(combos, k)
        ret = x
    else:
        x = binomial(n*(n-1)/2, k)
        for m in range(n-2+1):
            x1 = 0
            for p in range(k+1):
                x1 += binomial((n-1-m)*(n-2-m)/2, p)*q(m+1, k-p)
            x1 *= binomial(n-1, m)
            x -= x1
        ret = x
    memoize_q[key] = ret
    return ret
    
def binomial(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    """
    key = "binomial(%d,%d)" % (n, k)
    if key in memoize_binomial:
        return memoize_binomial[key]

    ret = 0
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        ret = ntok // ktok
    
    memoize_binomial[key] = ret
    return ret
    
def main(N, K):
    print "TEST(%d, %d)" % (N,K)
    answer1 = answer(N, K)
    print answer1
    
if __name__ == "__main__":


    main(2,1)

    main(3,2)

    main(4,3)
    main(4,4)
    main(4,5)
    main(4,6)

    main(20,19)
    
    main(20, 100)
    
    main(20,190)
