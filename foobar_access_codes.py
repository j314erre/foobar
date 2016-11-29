
 
def answer(x):
    """ find number of unique access codes given that forward/backward codes are equivalent
    """
    
    unique = {}
    
    # examine each of the codes
    for key in x:
        
        # backwards string
        reversed = key[::-1]
        
        # put forwards/backwards in sort order
        sorted_keys = sorted([key,reversed])
        
        # this key will match forwards and backwards
        newkey = "\t".join(sorted_keys)
        
        # put key in dictionary
        unique[newkey] = 1
    
    # return number of unique forward/backward keys    
    return len(unique)

def main(x):
    print "TEST"
    print x
    answer1 = answer(x)
    print answer1
    
if __name__ == "__main__":

    
    main(["abc", "cba", "bac"])
    
    main(["foo", "bar", "oof", "bar"])

    main(["x", "y", "xy", "yy", "", "yx"])