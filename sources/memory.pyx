#cython: profile=False
#cython: boundscheck=False
#cython: cdivision=True

from libc.stdlib cimport free

cimport data


cpdef memfree():
    cdef int i = 0

    data.fps = 0
    data.substep = 0
    data.deltatime = 0
    data.cpunum = 0
    data.newlinks = 0
    data.totallinks = 0
    data.totaldeadlinks = 0
    free(data.deadlinks)
    data.deadlinks = NULL

    for i in xrange(data.parnum):
        if data.parnum >= 1:
            # free(data.parlist[i].sys)
            # data.parlist[i].sys = NULL
            if data.parlist[i].neighboursnum >= 1:
                free(data.parlist[i].neighbours)
                data.parlist[i].neighbours = NULL
                data.parlist[i].neighboursnum = 0
            if data.parlist[i].collided_num >= 1:
                free(data.parlist[i].collided_with)
                data.parlist[i].collided_with = NULL
                data.parlist[i].collided_num = 0
            if data.parlist[i].links_num >= 1:
                free(data.parlist[i].links)
                data.parlist[i].links = NULL
                data.parlist[i].links_num = 0
                data.parlist[i].links_activnum = 0
            if data.parlist[i].link_withnum >= 1:
                free(data.parlist[i].link_with)
                data.parlist[i].link_with = NULL
                data.parlist[i].link_withnum = 0
            if data.parlist[i].neighboursnum >= 1:
                free(data.parlist[i].neighbours)
                data.parlist[i].neighbours = NULL
                data.parlist[i].neighboursnum = 0

    for i in xrange(data.psysnum):
        if data.psysnum >= 1:
            # free(data.psys[i].particles)
            data.psys[i].particles = NULL

    if data.psysnum >= 1:
        free(data.psys)
        data.psys = NULL

    if data.parnum >= 1:
        free(data.parlistcopy)
        data.parlistcopy = NULL
        free(data.parlist)
        data.parlist = NULL

    data.parnum = 0
    data.psysnum = 0

    if data.kdtree.numnodes >= 1:
        for i in xrange(data.kdtree.numnodes):
            free(data.kdtree.nodes[i].particle)
            data.kdtree.nodes[i].particle = NULL
            free(data.kdtree.nodes[i].left_child)
            data.kdtree.nodes[i].left_child = NULL
            free(data.kdtree.nodes[i].right_child)
            data.kdtree.nodes[i].right_child = NULL

        free(data.kdtree.thread_nodes)
        data.kdtree.thread_nodes = NULL
        free(data.kdtree.thread_start)
        data.kdtree.thread_start = NULL
        free(data.kdtree.thread_end)
        data.kdtree.thread_end = NULL
        free(data.kdtree.thread_name)
        data.kdtree.thread_name = NULL
        free(data.kdtree.thread_parent)
        data.kdtree.thread_parent = NULL
        free(data.kdtree.thread_depth)
        data.kdtree.thread_depth = NULL
        free(data.kdtree.nodes)
        data.kdtree.nodes = NULL
        free(data.kdtree.root_node)
        data.kdtree.root_node = NULL

    free(data.kdtree)
    data.kdtree = NULL
