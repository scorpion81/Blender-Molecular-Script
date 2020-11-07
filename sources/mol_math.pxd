cimport cython


cdef float fabs(float value)nogil
cdef float sq_number(float val)
cdef float square_dist(float point1[3], float point2[3], int k)nogil
cdef float dot_product(float u[3],float v[3])nogil
