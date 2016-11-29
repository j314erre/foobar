import random

 
def answer(food, grid):
    """ Find optimize monotonic path through a grid
    """
    
    # see if there is enough food to get through from top left cell to bottom right
    # return -1 if not
    cheapest = mincost(0, 0, grid)
    if food<cheapest:
        return -1
    
    # compute min savings given the food budget
    savings = minsavings(food, grid)
    assert (savings >=0 and savings<food)
    return savings

# use dynamic programming to find min cost path from cell (r,c) to bottom right
def mincost(r, c, cost):
    
    # figure out how many steps in each direction
    n = len(cost)
    nr = n - r
    nc = n - c
    
    # keep an array for dynamic programming results
    q = [[0 for i in range(nc)] for j in range(nr)]
    
    # initialize starting point
    q[0][0] = cost[r][c]

    # apply dynamic programming for each possible cell moving towards bottom right
    for i in range(nr):
        for j in range(nc):
            if i==0 and j==0:
                continue
            
            # find the minimum cost path coming from possible incoming cells
            first = True
            minimum = 0
            if i>0:
                # coming from row above
                minimum = q[i-1][j]
                first = False
            if j>0:
                # coming from column to the left
                test = q[i][j-1]
                if first or test<minimum:
                    minimum = test 
                    
            # store resulting minimum path plus the cost of current cell        
            value = minimum + cost[i+r][j+c]
            q[i][j] = value
     
    return q[nr-1][nc-1]   

# use dynamic programming to find min savings from top left to bottom right
def minsavings(bank, cost):
    n = len(cost)
    q = [[0 for i in range(n)] for j in range(n)]
    
    # start with savings in the bank at top left
    q[0][0] = bank
    
    # use a very big number that will never qualify as a possible minimum
    infinity = 1000000
    
    # work out all cells in grid
    for i in range(n):
        for j in range(n):
            if i==0 and j==0:
                continue
            
            # figure out how minimum savings needed to get from here to the bottom right
            savings_needed = mincost(i, j, cost)
            
            # computing minimum savings from incoming cells...except don't run out of savings
            minimum = infinity
            if i>0:
                # coming from row above
                test1 = q[i-1][j]
                
                # look for minimum but not less than savings need to to the end
                if test1 < minimum and test1>=savings_needed:
                    minimum = test1
            if j>0:
                # coming from column to the left
                test2 = q[i][j-1]
                
                
                # look for minimum but not less than savings need to to the end
                if test2 < minimum and test2>=savings_needed:
                    minimum = test2
                    
            # subtract the cost of the current cell from the optimal incoming path
            savings = minimum - cost[i][j]
            
            
            if savings < 0:
                # should never happen based on the tests above
                q[i][j] = infinity
            else:
                q[i][j] = savings
    return q[n-1][n-1]   

    

###############################################################################
###############################################################################

    
def main(food, grid):
    print "N: %d" % len(grid)
    print "food: %s" % food
    print "grid:"
    for g in grid:
        print g
    answer1 = answer(food, grid)
    print "answer: %s" % answer1
    print "###########################" 
    return 0
    
if __name__ == "__main__":

    
    main(30, [[0, 14, 18],[4, 8, 17],[17, 11, 7]])

    main(7, [[0, 2, 5], [1, 1, 3], [2, 1, 1]])
    
    main(12, [[0, 2, 5], [1, 1, 3], [2, 1, 1]])
  
    main(1, [[0, 1, 1], [1, 1, 1], [1, 1, 1]])
      
     
     
    grid = []
    for i in range(20):
        cell = []
        for j in range(20):
            cell.append(1)
        grid.append(cell)
    grid[0][0] = 0
          
    main(100, grid)
     
    for x in range(1000):
        n = 3
        grid = []
        for i in range(n):
            cell = []
            for j in range(n):
                cell.append(random.randint(1,20))
            grid.append(cell)
                 
        grid[0][0] = 0         
        main(random.randint(1,200), grid)
       
  

    
  
