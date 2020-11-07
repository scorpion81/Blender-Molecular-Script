#cython: profile=False
#cython: boundscheck=False
#cython: cdivision=True

cimport types


cdef void quick_sort(types.SParticle *a, int n, int axis)nogil:
    if (n < 2):
        return
    cdef types.SParticle t
    cdef float p = a[n / 2].loc[axis]
    cdef types.SParticle *l = a
    cdef types.SParticle *r = a + n - 1
    while l <= r:
        if l[0].loc[axis] < p:
            l += 1
            continue
        
        if r[0].loc[axis] > p:
            r -= 1
            # // we need to check the condition (l <= r) every time
            #  we change the value of l or r
            continue

        t = l[0]
        l[0] = r[0]
        # suggested by stephan to remove temp variable t but slower
        # l[0], r[0] = r[0], l[0]
        l += 1
        r[0] = t
        r -= 1

    quick_sort(a, r - a + 1, axis)
    quick_sort(l, a + n - l, axis)


cdef int compare_x (const void *u, const void *v)nogil:
    cdef float w = (<types.SParticle*>u).loc[0] - (<types.SParticle*>v).loc[0]
    if w < 0:
        return -1
    if w > 0:
        return 1
    return 0


cdef int compare_y (const void *u, const void *v)nogil:
    cdef float w = (<types.SParticle*>u).loc[1] - (<types.SParticle*>v).loc[1]
    if w < 0:
        return -1
    if w > 0:
        return 1
    return 0


cdef int compare_z (const void *u, const void *v)nogil:
    cdef float w = (<types.SParticle*>u).loc[2] - (<types.SParticle*>v).loc[2]
    if w < 0:
        return -1
    if w > 0:
        return 1
    return 0


cdef int compare_id (const void *u, const void *v)nogil:
    cdef float w = (<types.SParticle*>u).id - (<types.SParticle*>v).id
    if w < 0:
        return -1
    if w > 0:
        return 1
    return 0   


cdef int arraysearch(int element, int *array, int len)nogil:
    cdef int i = 0
    for i in xrange(len):
        if element == array[i]:
            return i
    return -1
