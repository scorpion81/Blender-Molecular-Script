#cython: profile=False
#cython: boundscheck=False
#cython: cdivision=True

cimport cython


cdef float fabs(float value)nogil:
    if value >= 0:
        return value
    if value < 0:
        return -value


cdef float sq_number(float val):
    cdef float nearsq = 8
    while val > nearsq or val < nearsq / 2:
        if val > nearsq:
            nearsq = nearsq * 2
        elif val < nearsq / 2:
            nearsq = nearsq / 2
    return nearsq


#@cython.cdivision(True)
cdef float square_dist(float point1[3], float point2[3], int k)nogil:
    cdef float sq_dist = 0
    for i in xrange(k):
        sq_dist += (point1[i] - point2[i]) * (point1[i] - point2[i])
    return sq_dist


cdef float dot_product(float u[3],float v[3])nogil:
    cdef float dot = 0
    dot = (u[0] * v[0]) + (u[1] * v[1]) + (u[2] * v[2])
    return dot
