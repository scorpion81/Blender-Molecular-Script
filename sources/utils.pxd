cimport types


cdef void quick_sort(types.SParticle *a, int n, int axis)nogil
cdef int compare_x (const void *u, const void *v)nogil
cdef int compare_y (const void *u, const void *v)nogil
cdef int compare_z (const void *u, const void *v)nogil
cdef int compare_id (const void *u, const void *v)nogil
cdef int arraysearch(int element, int *array, int len)nogil
