


def answer(intervals):
    """ find union of potentially overlapping set of intervals
    """
    
    for i in intervals:
        print i
    
    # sort intervals based on start time, then by stop time
    sorted_list = sorted(intervals, key = lambda x : (x[0], x[1]))
    
    # keep track of total time as we walk the sorted list
    total_time = 0
    
    # keep track of state
    current_start = 0
    current_end = 0
    for i in sorted_list:
        start = i[0]
        end = i[1]
        
        # first interval initialize start and stop
        if total_time==0:
            total_time += end - start
            current_start = start
            current_end = end
            
        # interval does not overlap previous    
        elif start >= current_end:
            total_time += end -start
            current_start = start
            current_end = end
            
        # interval overlaps, so just extend the end    
        elif end > current_end:
            total_time += end - current_end
            current_end = end
        
    return total_time;    

def main(intervals):
    print "TEST"
    print intervals
    answer1 = answer(intervals)
    print answer1
    
if __name__ == "__main__":


    main([[1, 3], [3, 6]])


    main([[10, 14], [4, 18], [19, 20], [19, 20], [13, 20]])


    main([[1, 11], [1, 2], [3, 4], [5, 6], [7, 9]])
    
    main([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
