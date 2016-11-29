import sys
import itertools
from itertools import count



# test1 = 2
# test2 = -1
# test3 = 50, N=15
# test4 = ?  N=even
# test5 = -1
def answer(matrix):
    return answer5(matrix)

def answer5(matrix):
    N = len(matrix)    
    
    b = matrix_to_vector(matrix)
    size = len(b)
    
    #print b
    if all(v == 0 for v in b):
        return 0
         
    A = get_toggles(N)        
    count = solve_gauss_jordan_elimination(A, b)
    
    # no solution
    if count==-1:
        return -1
    
    # even solution
    if N%2 == 0:
        result = get_even_solution(A, b)
        #print "result=%s" % result
        return count
    
    # looking for odd solution...
    assert(N%2!=0 and N<=15)
    
    #embed in N+1
    A1 = get_toggles(N+1)
    A1toggles = get_toggles_ids(A1)
    embed = []
    for m in matrix:
        embed.append(m + [0])
    embed.append([0]*(N+1))
    b1 = matrix_to_vector(embed)
    embed_size = len(b1)
    #print "b=%s" % b1
    result1 = get_even_solution(A1toggles, b1)
    
    #print "result1=%s\n\n" % result1
    
    # search 2^N completions to the embed
    bitmask = []
    for i in range(0,N+2):
        mask = 2**i
        #print bin(mask)
        bitmask.append(mask)
        
    result2 = size
    counter = 0
    last_row_offset = N*(N+1)
#    limit = 2 ** (N+1)
    limit = 2 ** N
    candidate = [0] * embed_size
    check_list = get_toggles_ids(A)
    while counter<limit:
        for i in range(0, N+1):
            candidate[last_row_offset+i] = (counter & bitmask[i]) >> i
        #print "COUNTER %d=%s" % (counter, candidate)
        counter += 1
        
        candidate_result = get_even_solution(A1toggles, candidate)
        #print "bottom flips: %s" % candidate_result
        
        for i in range(embed_size):
            candidate_result[i] =  candidate_result[i] ^ result1[i]
        #print "candidate result: %s" % candidate_result
        
        
        # flip RHS at once
#         tally = tally_subspace(candidate_result, N)
#         for row in range(N):
#             # get the row
#             for j in range(row*(N+1),(row+1)*(N+1)-1):
#                 candidate_result[j] =  candidate_result[j] ^ 1
#  
#         tally2 =  tally_subspace(candidate_result, N)
#          
#         if tally2 < tally:
#             tally = tally2

        # flip RHS individually
        for row in range(N):
            #print "check row %d flip: %s" % (row, candidate_result[row*(N+1):(row+1)*(N+1)-1])
            temp = sum(v==1 for v in candidate_result[row*(N+1):(row+1)*(N+1)-1])
            temp1 = N - temp
            if temp1 < temp:
                # let's flip the row
                index = row*(N+1) - 1
                    
                # get a flip vector
                for j in range(row*(N+1),(row+1)*(N+1)-1):
                    candidate_result[j] =  candidate_result[j] ^ 1
                      
                #print "***flip: %s" % candidate_result[row*(N+1):(row+1)*(N+1)-1]
 
  
        tally = tally_subspace(candidate_result, N)

        #print candidate_result
        #print "TALLY=%d" % tally
        
        # check if actually a solution
        check_result = []
        for row in range(N):
            for v in candidate_result[row*(N+1):(row+1)*(N+1)-1]:
                check_result.append(v)
        #print "check: %s" % check_result
        is_solution = check_strategy(check_list, b, check_result)
        #is_solution = True
        #print "SOLUTION: %s" % is_solution
        #print "\n\n"        
        
        
        if is_solution and tally < result2:
            result2 = tally
            
    return result2

def check_strategy(checklist, b, strategy):
    assert(len(checklist) == len(b) == len(strategy))
    N = len(b)
    result = list(b)
    for i in range(N):
        if strategy[i]==1:
            for id in checklist[i]:
                    result[id] = result[id] ^ 1
    return all(v==0 for v in result)
    
def tally_subspace(vector, N):
    tally = 0
    for row in range(N):
        offset = row*(N+1)
        tally += sum(v==1 for v in vector[offset:offset+N])
    
    return tally
    
def get_toggles(N):
    A = []
    for i in range(N):
        for j in range(N):
            t = generator(i, j, N)
            #print "T[%d][%d]=%s" % (i, j, t)
            v = matrix_to_vector(t)
            A.append(v)
    return A

def get_toggles_ids(A):
    toggles = []
    for i in range(len(A)):
        ids = []
        for j in range(len(A[i])):
            if A[i][j] == 1:
                ids.append(j)
        toggles.append(ids)
    return toggles
# 1111 
# 1001 + ? 
# 1001 
# 0100
def get_even_solution(A, b):
    size = len(b)
    result = [0]*size
    for i in range(size):
        if b[i] == 1:
            for id in A[i]:
                result[id] = result[id] ^ 1
#     for i in range(len(result)):
#         result[i] = result[i] % 2
    return result
    

def answer3(matrix):
    count = simplex(matrix)
    return count
    
def answer4(matrix):
    N = len(matrix)    
    
    b = matrix_to_vector(matrix)
    size = len(b)
    
    #print b
    if all(v == 0 for v in b):
        return 0
         
    A = []
    for i in range(N):
        for j in range(N):
            t = generator(i, j, N)
            #print "T[%d][%d]=%s" % (i, j, t)
            v = matrix_to_vector(t)
            A.append(v)
    
    return solve(A, 0, 0, b)

def solve(A, i, n, mask):
    #print "solve(%d, %d, %s)" % (i, n, mask)
    
    if all(v == 0 for v in mask):
        return n

    if i==len(A):
        return -1
    
    ret1 = solve(A, i+1, n, mask)
    
    if ret1 != -1:
        return ret1
    
    newmask = []
    for m in range(len(mask)):
        newmask.append(mask[m]^A[i][m])
    ret2 = solve(A, i+1, n+1, newmask)    
    
    return ret2
    

 
      

def solve_gauss_jordan_elimination(A, b):
    Ab = []
    for a in A:
        Ab.append(a)
    Ab.append(b)
    Ab = transpose(Ab)     
    
    basis = gauss_jordan_elimination(Ab)
    # check results
    count = 0
    for r in range(len(Ab)):
        row = Ab[r]
        if row[-1] == 1:
            count += 1
            
            # 
            if all(v == 0 for v in row[:-1]):
                count = -1
                break

            # see if it's a singular row
            for i in range(len(row)-1):
                if row[i] == 1:
                    if basis[i]==False:
                        count = -1
                    break
        

    return count
    
    
def gauss_jordan_elimination(matrix):
    
    nrows = len(matrix)
    ncols = len(matrix[0])
    assert(nrows + 1 == ncols)

    basis = [False]*nrows
    j=0
    i=0
    for j in range(nrows):
        reduced = False
        if matrix[i][j] == 0:
            swap_row(i, j, matrix)
        if matrix[i][j] == 1:
            reduced = True
            for ii in range(nrows):
                if ii==i:
                    continue
                if matrix[ii][j] == 1:
                    for jj in range(ncols):
                        matrix[ii][jj] = matrix[i][jj] ^ matrix[ii][jj]
            i += 1
        basis[j] = reduced
        #print "*****"
        #print_matrix(matrix)
    assert(len(basis)==nrows)
    return basis 
  
def gaussian_elimination(matrix):
    
    nrows = len(matrix)
    ncols = len(matrix[0])

    j=0
    i=0
    for j in range(nrows):
        if matrix[i][j] == 0:
            swap_row(i, j, matrix)
        if matrix[i][j] == 1:
            for ii in range(i+1, nrows):
                if matrix[ii][j] == 1:
                    for jj in range(ncols):
                        matrix[ii][jj] = matrix[i][jj] ^ matrix[ii][jj]
            i += 1
        #print "*****"
        #print_matrix(matrix)
        
def swap_row(i, j, matrix):
    row = i
    # find row to swap
    for r in range(i+1,len(matrix)):
        if matrix[r][j]==1:
            row = r
            break
    if row > i:
        matrix[i], matrix[row] = matrix[row], matrix[i]
        
    
def generator(i, j, N):
    m = []
    
    for r in range(N):
        row = []
        for c in range(N):
            if r==i or c==j:
                row.append(1)
            else:
                row.append(0)
        m.append(row)
    
    return m
        
def matrix_to_vector(matrix):
    v = []
    for row in matrix:
        for col in row:
            assert(col==0 or col==1)
            v.append(col)
            
    return v
    
def transpose(matrix):
    m = len(matrix)
    n = len(matrix[0])
    t = []
    for j in range(n):
        row = []
        for v in matrix:
            row.append(v[j])
        t.append(row)
            
    return t

        
        
###############################################################################
###############################################################################

def answer_brute(matrix):
    
    N = len(matrix)
    
    b = matrix_to_vector(matrix)
    
    size = len(b)
    
    assert(size==N*N)
    
    if all(v == 0 for v in b):
        return 0
         
    generators = []
    for i in range(N):
        for j in range(N):
            t = generator(i, j, N)
            #print "T[%d][%d]=%s" % (i, j, t)
            v = matrix_to_vector(t)
            generators.append(v)
    
    count = -1
    for m in range(1,size+1):
        for combo in itertools.combinations(range(size), m):
            result = [0] * size
            
            for g in combo:
                for i in range(size):
                    result[i] = result[i] ^ generators[g][i]
            if result == b:
                print combo
                if count==-1:
                    count = m
                    
    return count

def count_results(N):
    
    
    size =N*N
    
    assert(size==N*N)
    results = {}         
    generators = []
    for i in range(N):
        for j in range(N):
            t = generator(i, j, N)
            #print "T[%d][%d]=%s" % (i, j, t)
            v = matrix_to_vector(t)
            generators.append(v)
    
    for m in range(1,size+1):
        for combo in itertools.combinations(range(size), m):
            result = [0] * size
            
            for g in combo:
                for i in range(size):
                    result[i] = result[i] ^ generators[g][i]
            
            results["%s" % result] = True
                    
    return len(results)

def print_matrix(matrix):
    count = 0
    for row in matrix:
        print "Row %d: %s"% (count, row)
        count += 1


def test(seq, expected):
    print "TEST(%s)" % (seq)
    answer1 = answer(seq)
    status = "FAILED"
    if answer1 == expected:
        status = "PASSED"
    print "answer=%s\t%s\t expected=%s" % (answer1, status, expected)
    assert(answer1==expected)
    
if __name__ == "__main__":
#    test([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 0]], -100)
#     test([[1, 1, 0], [1, 1, 0], [0, 0, 0]], 2)
#     test([[1, 0, 0], [1, 0, 0], [1, 1, 1]], 1)
    test([[1, 1], [0, 0]], 2)
    test([[0, 0], [0, 0]], 0)
    test([[1, 1], [1, 1]], 4)
#     answer_brute([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
#     test([[1, 0, 0], [1, 0, 0], [1, 1, 1]], 1)
#     test([[1, 1, 0], [1, 1, 0], [0, 0, 0]], 2)
#     answer_brute([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
#     answer2([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
#     answer_brute([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
#     answer2([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    test([
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          ], 15)
#  
#      
#     test([[1, 1], [0, 0]], 2)
#     test([[0, 0], [0, 0]], 0)
#     test([[1, 1], [1, 1]], 4)
#      
#     test([[1, 1, 1], [1, 0, 0], [1, 0, 1]], -1)
#     test([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0)
#     test([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], 0)
#     test([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], 0)
    for N in range(3,4):
        size = N*N
        for m in range(size+1):
            for combo in itertools.combinations(range(size), m):
                result = [0] * size
                  
                for g in combo:
                    result[g] = 1
                  
                matrix = []
                b = []
                for v in result:
                    b.append(v)
                    if len(b) == N:
                        matrix.append(b)
                        b = []
                print "TEST: %s" % matrix
                answer1 = answer(matrix)
                answer2 = answer_brute(matrix)
                assert (answer1==answer2), "%s answer %d!= expected %d" % (matrix, answer1, answer2)
             
        
#     for N in range(2,16):
#         size = N*N
#         result = [1] * size
#         matrix = []
#         b = []
#         for v in result:
#             b.append(v)
#             if len(b) == N:
#                 matrix.append(b)
#                 b = []
#         print "TEST %d: %s" % (N, matrix)
#         answer1 = answer(matrix)
#         print answer1
            
 

