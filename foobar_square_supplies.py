


def answer(n):
    """ Find optimal tiling using perfect squares
    """

    number = 0
    
    coins_remaining = n
    
    while coins_remaining>0:
        
        # find the biggest perfect square <= remaining number
        cost = biggest_square_cost(coins_remaining)
       
        # deduct from the number remaining        
        coins_remaining -= cost
        
        # increment the number of tiles used
        number += 1
        
        
    return number
    

def biggest_square_cost(n):
    """ find perfect square less than or equal to n
    """
    
    # we know square size is less than 100 so brute force works fine
    for i in range(100, 0, -1):
        test = i*i
        if test <= n:
            return test
    raise ValueError('Out of bounds')


    
if __name__ == "__main__":
    #print "ANSWER: %d" % answer(160)
    for n in range(1,10000):
        a = answer(n)
        print "%s\t%s" % (n, a)
