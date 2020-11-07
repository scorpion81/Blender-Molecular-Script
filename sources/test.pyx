#cython: profile=False
#cython: boundscheck=False
#cython: cdivision=True

cimport cython
from libc.stdlib cimport malloc, free

cimport types, data, kd_tree


cdef testkdtree(int verbose = 0):
    if verbose >= 3:
        print("RootNode:", data.kdtree.root_node[0].index)
        for i in xrange(data.parnum):
            print(
                "Parent",
                data.kdtree.nodes[i].index,
                "Particle:",
                data.kdtree.nodes[i].particle[0].id
            )
            print("    Left", data.kdtree.nodes[i].left_child[0].index)
            print("    Right", data.kdtree.nodes[i].right_child[0].index)

    cdef float *a = [0, 0, 0]
    cdef types.Particle *b
    b = <types.Particle *>malloc(1 * cython.sizeof(types.Particle))
    if verbose >= 1:
        print("start searching")
    kd_tree.KDTree_rnn_query(data.kdtree, b, a, 2)
    output = []
    if verbose >= 2:
        print("Result")
        for i in xrange(b[0].neighboursnum):
            print(" Query Particle:", data.parlist[b[0].neighbours[i]].id)
    if verbose >= 1:
        print("number of particle find:", b[0].neighboursnum)
    free(b)


cdef void printdb(int linenumber, text = ""):
    cdef int dbactive = 1
    if dbactive == 1:
        print(linenumber)
