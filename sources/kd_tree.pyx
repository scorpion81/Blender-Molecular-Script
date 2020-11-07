#cython: profile=False
#cython: boundscheck=False
#cython: cdivision=True

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
        )nogil:

    cdef int axis = 0
    cdef float realsqdist = 0

    if node.index == -1:
        return

    cdef types.SParticle tparticle = node.particle[0]

    axis = kdtree.axis[depth] 

    if (mol_math.fabs(point[axis] - tparticle.loc[axis])) <= dist:
        realsqdist = mol_math.square_dist(point, tparticle.loc, 3)

        if realsqdist <= sqdist:

            par.neighbours[par.neighboursnum] = node.particle[0].id
            par.neighboursnum += 1
            if (par.neighboursnum) >= par.neighboursmax:
                par.neighboursmax = par.neighboursmax * 2
                par.neighbours = <int *>realloc(
                    par.neighbours,
                    (par.neighboursmax) * cython.sizeof(int)
                )

        KDTree_rnn_search(
            kdtree,
            &par[0],
            node.left_child[0],
            point,
            dist,
            sqdist,
            3,
            depth + 1
        )

        KDTree_rnn_search(
            kdtree,
            &par[0],
            node.right_child[0],
            point,
            dist,
            sqdist,
            3,
            depth + 1
        )

    else:
        if point[axis] <= tparticle.loc[axis]:
            KDTree_rnn_search(
                kdtree,
                &par[0],
                node.left_child[0],
                point,
                dist,
                sqdist,
                3,
                depth + 1
            )

        if point[axis] >= tparticle.loc[axis]:
            KDTree_rnn_search(
                kdtree,
                &par[0],
                node.right_child[0],
                point,
                dist,
                sqdist,
                3,
                depth + 1
            )


cdef int KDTree_rnn_query(
        types.KDTree *kdtree,
        types.Particle *par,
        float point[3],
        float dist
        )nogil:

    cdef float sqdist  = 0
    cdef int k  = 0
    cdef int i = 0
    par.neighboursnum = 0
    # free(par.neighbours)
    par.neighbours[0] = -1

    if kdtree.root_node[0].index != kdtree.nodes[0].index:
        par.neighbours[0] = -1
        par.neighboursnum = 0
        return -1
    else:
        sqdist = dist * dist
        KDTree_rnn_search(
            kdtree, &par[0],
            kdtree.root_node[0],
            point,
            dist,
            sqdist,
            3,
            0
        )


cdef types.Node KDTree_create_tree(
        types.KDTree *kdtree,
        types.SParticle *kdparlist,
        int start,
        int end,
        int name,
        int parent,
        int depth,
        int initiate
        )nogil:

    cdef int index = 0
    cdef int len = (end - start) + 1
    if len <= 0:
        return kdtree.nodes[kdtree.numnodes]
    cdef int axis
    cdef int k = 3
    axis =  kdtree.axis[depth] 
    # depth % k
    utils.quick_sort(kdparlist + start, len, axis)
    '''
    if axis == 0:
        qsort(kdparlist + start, len, sizeof(types.SParticle), utils.compare_x)
    elif axis == 1:
        qsort(kdparlist + start, len, sizeof(types.SParticle), utils.compare_y)
    elif axis == 2:
        qsort(kdparlist + start, len, sizeof(types.SParticle), utils.compare_z)
    '''
    cdef int median = (start + end) / 2

    if depth == 0:
        kdtree.thread_index = 0
        index = 0
    else:
        index = (parent * 2) + name

    if index > kdtree.numnodes:
        return kdtree.nodes[kdtree.numnodes]

    kdtree.nodes[index].name = name
    kdtree.nodes[index].parent = parent

    if len >= 1 and depth == 0:
        kdtree.root_node[0] = kdtree.nodes[0]

    kdtree.nodes[index].particle[0] = kdparlist[median]

    if data.parnum > 127:
        if depth == 4 and initiate == 1:
            kdtree.thread_nodes[kdtree.thread_index] = index
            kdtree.thread_start[kdtree.thread_index] = start
            kdtree.thread_end[kdtree.thread_index] = end
            kdtree.thread_name[kdtree.thread_index] = name
            kdtree.thread_parent[kdtree.thread_index] = parent
            kdtree.thread_depth[kdtree.thread_index] = depth
            kdtree.thread_index += 1
            return kdtree.nodes[index]

    kdtree.nodes[index].left_child[0] = KDTree_create_tree(
        kdtree,
        kdparlist,
        start,
        median - 1,
        1,
        index,
        depth + 1,
        initiate
    )
    kdtree.nodes[index].right_child[0] = KDTree_create_tree(
        kdtree,
        kdparlist,
        median + 1,
        end,
        2,
        index,
        depth + 1,
        initiate
    )

    return kdtree.nodes[index]


cdef void KDTree_create_nodes(types.KDTree *kdtree,int parnum):#nogil:
    cdef int i = 0
    i = 2
    while i < parnum:
        i = i * 2
    kdtree.numnodes = i
    kdtree.nodes = <types.Node *>malloc((kdtree.numnodes + 1) * cython.sizeof(types.Node))
    kdtree.root_node = <types.Node *>malloc(1 * cython.sizeof(types.Node))

    for i in xrange(kdtree.numnodes):
        kdtree.nodes[i].index = i
        kdtree.nodes[i].name = -1
        kdtree.nodes[i].parent = -1

        kdtree.nodes[i].particle = <types.SParticle *>malloc(
            1 * cython.sizeof(types.SParticle)
        )

        kdtree.nodes[i].left_child = <types.Node *>malloc(1 * cython.sizeof(types.Node))
        kdtree.nodes[i].right_child = <types.Node *>malloc(1 * cython.sizeof(types.Node))
        kdtree.nodes[i].left_child[0].index = -1
        kdtree.nodes[i].right_child[0].index = -1

    kdtree.nodes[kdtree.numnodes].index = -1
    kdtree.nodes[kdtree.numnodes].name = -1
    kdtree.nodes[kdtree.numnodes].parent = -1

    kdtree.nodes[kdtree.numnodes].particle = <types.SParticle *>malloc(
        1 * cython.sizeof(types.SParticle)
    )

    kdtree.nodes[kdtree.numnodes].left_child = <types.Node *>malloc(
        1 * cython.sizeof(types.Node)
    )

    kdtree.nodes[kdtree.numnodes].right_child = <types.Node *>malloc(
        1 * cython.sizeof(types.Node)
    )

    kdtree.nodes[kdtree.numnodes].left_child[0].index = -1
    kdtree.nodes[kdtree.numnodes].right_child[0].index = -1
    kdtree.thread_nodes = <int *>malloc(128 * cython.sizeof(int))
    kdtree.thread_start = <int *>malloc(128 * cython.sizeof(int))
    kdtree.thread_end = <int *>malloc(128 * cython.sizeof(int))
    kdtree.thread_name = <int *>malloc(128 * cython.sizeof(int))
    kdtree.thread_parent = <int *>malloc(128 * cython.sizeof(int))
    kdtree.thread_depth = <int *>malloc(128 * cython.sizeof(int))
    # kdtree.axis = <int *>malloc( 64 * cython.sizeof(int) )

    for i in xrange(64):
        kdtree.axis[i] = i % 3

    return
