cimport cython
from libc.stdlib cimport malloc, realloc, free

cimport types, data, utils, mol_math


#@cython.cdivision(True)
cdef void KDTree_rnn_search(
        types.KDTree *kdtree,
        types.Particle *par,
        types.Node node,
        float point[3],
        float dist,
        float sqdist,
        int k,
        int depth
        )nogil


cdef int KDTree_rnn_query(
        types.KDTree *kdtree,
        types.Particle *par,
        float point[3],
        float dist
        )nogil


cdef types.Node KDTree_create_tree(
        types.KDTree *kdtree,
        types.SParticle *kdparlist,
        int start,
        int end,
        int name,
        int parent,
        int depth,
        int initiate
        )nogil


cdef void KDTree_create_nodes(types.KDTree *kdtree,int parnum)
