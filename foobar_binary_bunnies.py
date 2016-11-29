
from permutation_generator import PermutationGenerator

memoize_binomial = {}

class BinaryTree():
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None
        
    def insert(self, value):
        if (value < self.value):
            if self.left is None:
                self.left = BinaryTree(value)
            else:
                self.left.insert(value)
        if (value > self.value):
            if self.right is None:
                self.right = BinaryTree(value)
            else:
                self.right.insert(value)
    
    def sort(self, seq):
        self.value = seq[0]
        for s in seq[1:]:
            self.insert(s)

    def tostring(self):
        value = self.value
        left = "()"
        if self.left is not None:
            left = self.left.tostring()
        right = "()"
        if self.right is not None:
            right = self.right.tostring()
            
        return "(%s, %s, %s)" % (value, left, right)

def answer(seq):
    """ takes an array of up to 50 integers and returns a string 
    representing the number (in base-10) of sequences that would result in the same tree as the given sequence    
    """

    # create a binary tree from the sequence    
    bt = BinaryTree()
    bt.sort(seq)
        
    #print bt.tostring()
    
    # tally nodes in binary tree to find equivalent sequences
    count, _ = tally(bt)
        
    # return as string 
    return "%s" % count;    

def tally(tree):
    """ tally the number of sequences at this node using recursion
    """
    
    # the node contributes size one and single length
    size_seq = 1
    num_seq = 1
    
    
    # tally right branch
    num_seq_right = 1
    size_seq_right = 0    
    if tree.right is not None:
        num_seq_right, size_seq_right = tally(tree.right)
        num_seq *= num_seq_right
    
    # tally left branch
    num_seq_left = 1
    size_seq_left = 0
    if tree.left is not None:
        num_seq_left, size_seq_left = tally(tree.left)
    
    #print "tally %s" % tree.tostring()
    #print "    Nleft=%d Nright=%d" % (num_seq_left, num_seq_right)
    
    # find combinations where left & right are interleaved / shuffled without changing order of each side
    num_seq = binomial(size_seq_left+size_seq_right, size_seq_left)
    
    # we get an overall factor from the number of sequences on each side
    num_seq *= num_seq_left * num_seq_right
    
    size_seq += size_seq_right + size_seq_left
    
    if tree.left is None and tree.right is None:
        num_seq = 1
        
    #print "    num=%d size=%d" % (num_seq, size_seq)
    
    return num_seq, size_seq

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

###############################################################################
###############################################################################

def answer2(seq):
    """ brute force    
    """
    n = len(seq)
    pg = PermutationGenerator(n)

    mastertree = BinaryTree()
    mastertree.sort(seq)        
    masterkey = mastertree.tostring()
    
    count = 1
    pg.getNext()
    while pg.hasmore():
        perm = pg.getNext()
        testseq = getperm(seq, perm)
        testtree = BinaryTree()
        testtree.sort(testseq)
        testkey = testtree.tostring()
        if testkey == masterkey:
            count += 1
            print testseq
        
    # return as string 
    return "%s" % count;    

def getperm(seq, perm):
    ret = []
    for i in perm:
        ret.append(seq[i])
    return ret

def test(seq, expected):
    print "TEST(%s)" % (seq)
    answer1 = answer(seq)
    status = "FAILED"
    if answer1 == expected:
        status = "PASSED"
    print "answer=%s\t%s" % (answer1, status)
    
if __name__ == "__main__":


    test([1,2,3], "1")
    test([2,3,1], "2")
    test([5, 9, 8, 2, 1], "6")
    test([5, 9, 8, 2, 1, 3, 10], "80")
    test([5, 9, 8, 2, 1, 3, 10, 11], "210")

    test([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "1")


