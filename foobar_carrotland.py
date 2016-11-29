from fractions import gcd

def answer(vertices):
    """ given a list of three vertices, returns the maximum number 
    points with integer coordinates on the 2-D plane, which lie within but not on the boundaries.
    All coordinates will have absolute value no greater than 1,000,000,000
    
    strategy:
    1. Brute force is to compute lattice points contained within the boundary along a lattice dimension...but doesn't scale to values 10^9
    2. We could apply Pick's Theorem directly but this would not be very fun
    3. Any triangle can be comprised of a bounding rectangle containing one or more Right triangles and zero or one Rectangles
        * Rectangles are easy to compute
        * Right triangles are easy to compute using a bounding rectangle
        * Therefore we can compute any triangle by breaking it down into components
    
    """
    
    # return as string 
    return triangle_lattice_points(vertices);    


def triangle_lattice_points(vertices):
    """ Check find lattice points contained within any triangle 
    """
    assert len(vertices) == 3, "not a triangle: %s" % vertices
    
    # get a bounding box for the triangle
    bounding_box = bounding_rectangle(vertices)
    
    corners = corner_points(vertices, bounding_box)
    
    ret = 0
    
    # case: 3 corners on the bounding box
    if len(corners) == 3:
        # take bounding points, subtract bisecting line points, divide by two
        ret = rectangle_lattice_points(bounding_box)
        ret -= line_lattice_points([bounding_box[0], bounding_box[3]])
        ret /= 2
        
    # case: 1 corner on the bounding box
    if len(corners) == 1:
        # take bounding points, subtract 3 right triangle lattice points, and original triangle boundaries
        ret = rectangle_lattice_points(bounding_box)
        
        # do each of 3 sides of original triangle
        ret -= line_lattice_points([vertices[0], vertices[1]])
        ret -= line_lattice_points([vertices[1], vertices[2]])
        ret -= line_lattice_points([vertices[2], vertices[0]])
        
        # do each of the 3 right triangles in the bounding box
        for corner in bounding_box:
            if corner not in corners:
                selected = [corner]
                for v in vertices:
                    if v[0] == corner[0] or v[1] == corner[1]:
                        selected.append(v)
                assert len(selected)==3
                ret -= triangle_lattice_points(selected)
        
    # case: 2 corners match on bounding box        
    if len(corners) == 2:
        
        # 3rd corner is on the bounding box
        if is_on_boundary(vertices, bounding_box):
            # take bounding points, subtract 2 right triangles and 2 original triangle boundaries
            ret = rectangle_lattice_points(bounding_box)
            
            # do 2 sides of original triangle not on the bounding box
            if not is_on_same_boundary([vertices[0], vertices[1]], bounding_box):
                ret -= line_lattice_points([vertices[0], vertices[1]])
            if not is_on_same_boundary([vertices[1], vertices[2]], bounding_box):
                ret -= line_lattice_points([vertices[1], vertices[2]])
            if not is_on_same_boundary([vertices[2], vertices[0]], bounding_box):
                ret -= line_lattice_points([vertices[2], vertices[0]])
                
            # do 2 right triangles in bounding box
            for corner in bounding_box:
                if corner not in corners:
                    xmin = abs(bounding_box[0][0]-bounding_box[3][0])+1
                    ymin = abs(bounding_box[0][1]-bounding_box[3][1])+1
                    xv = None
                    yv = None
                    for v in vertices:
                        if v[0]==corner[0]:
                            ytest = abs(v[1]-corner[1])
                            if ytest<ymin:
                                ymin = ytest
                                yv = v
                        if v[1]==corner[1]:
                            xtest = abs(v[0]-corner[0])
                            if xtest<xmin:
                                xmin = xtest
                                xv = v                
                    ret -= triangle_lattice_points([corner, xv, yv])
        
        # 3rd corner is inside the bounding box        
        else:
            # take bounding box points, subtract 3 original triangle boundaries, 3 boundary triangles, on rectangle
            ret = rectangle_lattice_points(bounding_box)
            
            # subtract the vertex inside the bounding box
            ret -= 1
            
            # do each of 3 sides of original triangle
            ret -= line_lattice_points([vertices[0], vertices[1]])
            ret -= line_lattice_points([vertices[1], vertices[2]])
            ret -= line_lattice_points([vertices[2], vertices[0]])
            
            # do smaller rectangle and 2 small triangles
            small_rect = None
            small_rect_corner = None
            
            for v in vertices:
                if v not in corners:
                    xmin = v[0]
                    xmax = v[0]
                    ymin = v[1]
                    ymax = v[1]
                    
                    minarea = abs(bounding_box[0][0] - bounding_box[3][0])*abs(bounding_box[0][1] - bounding_box[3][1])+1
                    for b in bounding_box:
                        if b not in corners:
                            area = abs(b[0] - v[0])*abs(b[1] - v[1])
                            if area < minarea:
                                minarea = area
                                small_rect_corner = b
                    
                    if small_rect_corner[0] < xmin:
                        xmin = small_rect_corner[0]
                    if small_rect_corner[0] > xmax:
                        xmax = small_rect_corner[0]
                    if small_rect_corner[1] < ymin:
                        ymin = small_rect_corner[1]
                    if small_rect_corner[1] > ymax:
                        ymax = small_rect_corner[1]
                        
                    # subtract points inside rectangle
                    small_rect = [[xmin, ymin], [xmax, ymin], [xmin, ymax], [xmax, ymax]]
                    ret -= rectangle_lattice_points(small_rect)
            
                    # subtract points on small rectangle edges
                    if not is_on_same_boundary([[xmin, ymin], [xmax, ymin]], bounding_box):
                        ret -= line_lattice_points([[xmin, ymin], [xmax, ymin]])
                        
                    if not is_on_same_boundary([[xmin, ymax], [xmax, ymax]], bounding_box):
                        ret -= line_lattice_points([[xmin, ymax], [xmax, ymax]])
                        
                    if not is_on_same_boundary([[xmin, ymin], [xmin, ymax]], bounding_box):
                        ret -= line_lattice_points([[xmin, ymin], [xmin, ymax]])
                        
                    if not is_on_same_boundary([[xmax, ymin], [xmax, ymax]], bounding_box):
                        ret -= line_lattice_points([[xmax, ymin], [xmax, ymax]])
                        
                        
                        
                    # small triangles
                    for corner in corners:
                        for rc in small_rect:
                            if (rc[0]==v[0] or rc[1]==v[1]) and (rc[0]==corner[0] or rc[1]==corner[1]):
                                ret -= triangle_lattice_points([corner, v, rc])
                
            # larger triangle
            for b in bounding_box:
                if b not in corners:
                    ret -= triangle_lattice_points([corners[0], corners[1], b])
                    break
    
    print "triangle_lattice_points %s=%d" % (vertices, ret)    
    return ret

def corner_points(vertices, rectangle):
    """ Count points on corners of rectangle
    """
    assert len(rectangle)==4, "not a rectangle: %s" % rectangle
    
    corners = []
    for v in vertices:
        for p in rectangle:
            if p[0]==v[0] and p[1]==v[1]:
                corners.append(p)
                break
        
    return corners

def is_on_boundary(vertices, rectangle):
    assert len(rectangle)==4, "not a rectangle: %s" % rectangle
    xmin = rectangle[0][0]
    ymin = rectangle[0][1]
    xmax = rectangle[3][0]
    ymax = rectangle[3][1]
    
    
    for v in vertices:
        if v[0]!=xmin and v[0]!=xmax and v[1]!=ymin and v[1]!=ymax:
            return False
        
    return True

def is_on_same_boundary(vertices, rectangle):
    assert len(rectangle)==4, "not a rectangle: %s" % rectangle
    xmin = rectangle[0][0]
    ymin = rectangle[0][1]
    xmax = rectangle[3][0]
    ymax = rectangle[3][1]
    
    xsame = True
    ysame = True
    xtest = vertices[0][0]
    ytest = vertices[0][1]
    for v in vertices:
        if v[0]!=xtest:
            xsame = False
        if v[1]!=ytest:
            ysame = False
    
    if xsame and (xtest==xmin or xtest==xmax):
        return True
    if ysame and (ytest==ymin or ytest==ymax):
        return True
    
    return False
    
    
def bounding_rectangle(vertices):
    """ Get bounding rectangle...works for any polygon
    """
    xmin = vertices[0][0]
    ymin = vertices[0][1]
    xmax = vertices[0][0]
    ymax = vertices[0][1]
    for v in vertices:
        if v[0] < xmin:
            xmin = v[0]
        if v[0] > xmax:
            xmax = v[0]
        if v[1] < ymin:
            ymin = v[1]
        if v[1] > ymax:
            ymax = v[1]
    
    # always do this order
    return [[xmin, ymin], [xmax, ymin], [xmin, ymax], [xmax, ymax]] 

def is_right_triangle(vertices):
    """ Check if a right triangle with two sides on the lattice 
    """
    assert len(vertices) == 3, "not a triangle: %s" % vertices
    xaxis = 0
    yaxis = 0
    # see how many pairs share a yaxis
    if vertices[0][0] - vertices[1][0] == 0:
        yaxis += 1
    if vertices[1][0] - vertices[2][0] == 0:
        yaxis += 1
    if vertices[2][0] - vertices[0][0] == 0:
        yaxis += 1
    # see how many pairs share a xaxis
    if vertices[0][1] - vertices[1][1] == 0:
        xaxis += 1
    if vertices[1][1] - vertices[2][1] == 0:
        xaxis += 1
    if vertices[2][1] - vertices[0][1] == 0:
        xaxis += 1
    
    # iff there is one pair on the same xaxis and one pair on the same yaxis    
    return xaxis==1 and yaxis==1
    
def rectangle_lattice_points(vertices):
    """ Return number of enclosed lattice points in bounding rectangle
    """
    assert len(vertices)==4, "not a rectangle: %s" % vertices
    smallest = vertices[0]
    largest = vertices[0]
    for vertex in vertices:
        if vertex[0] <= smallest[0] and vertex[1] <= smallest[1]:
            smallest = vertex
        if vertex[0] >= largest[0] and vertex[1] >= largest[1]:
            largest = vertex
            
    xspan = abs(largest[0] - smallest[0])
    yspan = abs(largest[1] - smallest[1])
    
    ret = 0
    if xspan >1 and yspan>1:
        ret = (xspan - 1)*(yspan - 1)
    
    print "rectangle_lattice_points %s=%d" % (vertices, ret)    
    return ret
    
def line_lattice_points(vertices):
    """ Return number of points on boundary line not including vertices
    """
    assert len(vertices)==2, "not a line: %s" % vertices
    xspan = abs(vertices[0][0] - vertices[1][0])
    yspan = abs(vertices[0][1] - vertices[1][1])
    ret = 0
    if xspan == 0 and yspan == 0:
        ret = 0
    elif xspan == 0:
        ret = yspan - 1
    elif yspan == 0:
        ret = xspan - 1
    elif xspan == yspan:
        ret = xspan - 1
    elif yspan > xspan:
        ret = gcd(yspan, xspan) - 1
    elif xspan > yspan:
        ret = gcd(xspan, yspan) - 1
    
    print "line_lattice_points %s=%d" % (vertices, ret)    
    return ret

    
def test(vertices, expected):
    print "TEST(%s)" % (vertices)
    answer1 = answer(vertices)
    status = "FAILED"
    if answer1 == expected:
        status = "PASSED"
    print "answer=%s\t%s" % (answer1, status)
    
    
if __name__ == "__main__":

    
    # 1 corner
    test([[0, 2], [2, 0], [4, 4]], 4)

    # 2 corners opposite, 3rd inside box
    test([[0, 0], [4, 2], [6, 6]], 2)
    
    # 2 corners opposite 3rd on boundary
    test([[0, 0], [2, 0], [4, 4]], 1)    
    
    # 2 corners adjacent
    test([[0, 0], [2, 2], [4, 0]], 1)    

    # 3 corners right triangle
    test([[0, 0], [0, 2], [4, 0]], 1)


    test([[2, 3], [6, 9], [10, 160]], 289)

    test([[91207, 89566], [-88690, -83026], [67100, 47194]], 1730960165)


