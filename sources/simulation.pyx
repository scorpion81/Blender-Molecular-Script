#cython: profile=False
#cython: boundscheck=False
#cython: cdivision=True

cimport cython
from time import perf_counter as clock
from cython.parallel import prange
from libc.stdlib cimport malloc, realloc, free

cimport types, collide, data, kd_tree, link


cdef extern from *:
    int INT_MAX
    float FLT_MAX


cdef extern from "stdlib.h":
    ctypedef void const_void "const void"
    void qsort(
        void *base,
        int nmemb,
        int size,
        int(*compar)(const_void *, const_void *)
    )nogil


cpdef simulate(importdata):
    cdef int i = 0
    cdef int ii = 0
    cdef int profiling = 0

    cdef float minX = INT_MAX
    cdef float minY = INT_MAX
    cdef float minZ = INT_MAX
    cdef float maxX = -INT_MAX
    cdef float maxY = -INT_MAX
    cdef float maxZ = -INT_MAX
    cdef float maxSize = -INT_MAX
    cdef types.Pool *parPool = <types.Pool *>malloc(1 * cython.sizeof(types.Pool))
    parPool.parity = <types.Parity *>malloc(2 * cython.sizeof(types.Parity))
    parPool[0].axis = -1
    parPool[0].offset = 0
    parPool[0].max = 0

    # cdef float *zeropoint = [0,0,0]
    data.newlinks = 0
    for i in xrange(data.cpunum):
        data.deadlinks[i] = 0
    if profiling == 1:
        print("-->start simulate")
        stime2 = clock()
        stime = clock()

    update(importdata)

    if profiling == 1:
        print("-->update time", clock() - stime, "sec")
        stime = clock()

    for i in xrange(data.parnum):
        data.parlistcopy[i].id = data.parlist[i].id
        data.parlistcopy[i].loc[0] = data.parlist[i].loc[0]
        # if data.parlist[i].loc[0] >= FLT_MAX or data.parlist[i].loc[0] <= -FLT_MAX :
            # print('ALERT! INF value in X')
        if data.parlist[i].loc[0] < minX:
            minX = data.parlist[i].loc[0]
        if data.parlist[i].loc[0] > maxX:
            maxX = data.parlist[i].loc[0]
        data.parlistcopy[i].loc[1] = data.parlist[i].loc[1]
        if data.parlist[i].loc[1] < minY:
            minY = data.parlist[i].loc[1]
        if data.parlist[i].loc[1] > maxY:
            maxY = data.parlist[i].loc[1]
        data.parlistcopy[i].loc[2] = data.parlist[i].loc[2]
        if data.parlist[i].loc[2] < minZ:
            minZ = data.parlist[i].loc[2]
        if data.parlist[i].loc[2] > maxZ:
            maxZ = data.parlist[i].loc[2]
        if data.parlist[i].sys.links_active == 1:
            if data.parlist[i].links_num > 0:
                for ii in xrange(data.parlist[i].links_num):
                    if data.parlist[i].links[ii].lenght > maxSize:
                        maxSize = data.parlist[i].links[ii].lenght
        if (data.parlist[i].size * 2) > maxSize:
            maxSize = (data.parlist[i].size * 2)

    if (maxX - minX) >= (maxY - minY) and (maxX - minX) >= (maxZ - minZ):
        parPool[0].axis = 0
        parPool[0].offset = 0 - minX
        parPool[0].max = maxX + parPool[0].offset

    if (maxY - minY) > (maxX - minX) and (maxY - minY) > (maxZ - minZ):
        parPool[0].axis = 1
        parPool[0].offset = 0 - minY
        parPool[0].max = maxY + parPool[0].offset

    if (maxZ - minZ) > (maxY - minY) and (maxZ - minZ) > (maxX - minX):
        parPool[0].axis = 2
        parPool[0].offset = 0 - minZ
        parPool[0].max = maxZ + parPool[0].offset       

    if (parPool[0].max / ( data.cpunum * 10 )) > maxSize:
        maxSize = (parPool[0].max / ( data.cpunum * 10 ))

    '''
    cdef float Xsize = maxX - minX
    cdef float Ysize = maxY - minY
    cdef float Zsize = maxZ - minZ
    cdef float newXsize = Xsize
    cdef float newYsize = Ysize
    cdef float newZsize = Zsize
    pyaxis = []
    for i in xrange(64):
        if Xsize >= Ysize and Xsize >= Zsize:
            data.kdtree.axis[i] = 0
            newXsize = Xsize / 2
        if Ysize > Xsize and Ysize > Zsize:
            data.kdtree.axis[i] = 1
            newYsize = Ysize / 2
        if Zsize > Xsize and Zsize > Ysize:
            data.kdtree.axis[i] = 2
            newZsize = Zsize / 2
            
        Xsize = newXsize
        Ysize = newYsize
        Zsize = newZsize
        pyaxis.append(data.kdtree.axis[i])
    '''

    cdef int pair
    cdef int heaps
    cdef float scale = 1 / ( maxSize * 2.1 )

    for pair in xrange(2):

        parPool[0].parity[pair].heap = \
            <types.Heap *>malloc((<int>(parPool[0].max * scale) + 1) * \
            cython.sizeof(types.Heap))

        for heaps in range(<int>(parPool[0].max * scale) + 1):
            parPool[0].parity[pair].heap[heaps].parnum = 0
            parPool[0].parity[pair].heap[heaps].maxalloc = 50

            parPool[0].parity[pair].heap[heaps].par = \
                <int *>malloc(parPool[0].parity[pair].heap[heaps].maxalloc * \
                cython.sizeof(int))

    for i in xrange(data.parnum):
        pair = <int>(((
            data.parlist[i].loc[parPool[0].axis] + parPool[0].offset) * scale) % 2
        )
        heaps = <int>((
            data.parlist[i].loc[parPool[0].axis] + parPool[0].offset) * scale
        )
        parPool[0].parity[pair].heap[heaps].parnum += 1

        if parPool[0].parity[pair].heap[heaps].parnum > \
                parPool[0].parity[pair].heap[heaps].maxalloc:

            parPool[0].parity[pair].heap[heaps].maxalloc = \
                <int>(parPool[0].parity[pair].heap[heaps].maxalloc * 1.25)

            parPool[0].parity[pair].heap[heaps].par = \
                <int *>realloc(
                    parPool[0].parity[pair].heap[heaps].par,
                    (parPool[0].parity[pair].heap[heaps].maxalloc + 2 ) * \
                    cython.sizeof(int)
                )

        parPool[0].parity[pair].heap[heaps].par[
            (parPool[0].parity[pair].heap[heaps].parnum - 1)] = data.parlist[i].id

    if profiling == 1:
        print("-->copy data time", clock() - stime, "sec")
        stime = clock()

    kd_tree.KDTree_create_tree(data.kdtree, data.parlistcopy, 0, data.parnum - 1, 0, -1, 0, 1)

    with nogil:
        for i in prange(
                        data.kdtree.thread_index,
                        schedule='dynamic',
                        chunksize=10,
                        num_threads=data.cpunum
                        ):
            kd_tree.KDTree_create_tree(
                data.kdtree,
                data.parlistcopy,
                data.kdtree.thread_start[i],
                data.kdtree.thread_end[i],
                data.kdtree.thread_name[i],
                data.kdtree.thread_parent[i],
                data.kdtree.thread_depth[i],
                0
            )

    if profiling == 1:
        print("-->create tree time", clock() - stime,"sec")
        stime = clock()

    with nogil:
        for i in prange(
                        <int>data.parnum,
                        schedule='dynamic',
                        chunksize=10,
                        num_threads=data.cpunum
                        ):
            kd_tree.KDTree_rnn_query(
                data.kdtree,
                &data.parlist[i],
                data.parlist[i].loc,
                data.parlist[i].size * 2
            )

    if profiling == 1:
        print("-->neighbours time", clock() - stime, "sec")
        stime = clock()

    with nogil:
        for pair in xrange(2):
            for heaps in prange(
                                <int>(parPool[0].max * scale) + 1,
                                schedule='dynamic',
                                chunksize=1,
                                num_threads=data.cpunum
                                ):
                for i in xrange(parPool[0].parity[pair].heap[heaps].parnum):

                    collide.collide(
                        &data.parlist[parPool[0].parity[pair].heap[heaps].par[i]]
                    )

                    link.solve_link(
                        &data.parlist[parPool[0].parity[pair].heap[heaps].par[i]]
                    )

                    if data.parlist[
                        parPool[0].parity[pair].heap[heaps].par[i]
                    ].neighboursnum > 1:

                        # free(data.parlist[i].neighbours)

                        data.parlist[
                            parPool[0].parity[pair].heap[heaps].par[i]
                        ].neighboursnum = 0

    '''
    with nogil:
        for i in xrange(data.parnum):
            collide.collide(&data.parlist[i])
            link.solve_link(&data.parlist[i])
            if data.parlist[i].neighboursnum > 1:
                #free(data.parlist[i].neighbours)
                data.parlist[i].neighboursnum = 0
    '''

    if profiling == 1:
        print("-->collide/solve link time", clock() - stime, "sec")
        stime = clock()

    exportdata = []
    parloc = []
    parvel = []
    parloctmp = []
    parveltmp = []

    for i in xrange(data.psysnum):
        for ii in xrange(data.psys[i].parnum):
            parloctmp.append(data.psys[i].particles[ii].loc[0])
            parloctmp.append(data.psys[i].particles[ii].loc[1])
            parloctmp.append(data.psys[i].particles[ii].loc[2])
            parveltmp.append(data.psys[i].particles[ii].vel[0])
            parveltmp.append(data.psys[i].particles[ii].vel[1])
            parveltmp.append(data.psys[i].particles[ii].vel[2])
        parloc.append(parloctmp)
        parvel.append(parveltmp)
        parloctmp = []
        parveltmp = [] 

    data.totallinks += data.newlinks
    pydeadlinks = 0
    for i in xrange(data.cpunum):
        pydeadlinks += data.deadlinks[i]
    data.totaldeadlinks += pydeadlinks

    exportdata = [
        parloc,
        parvel,
        data.newlinks,
        pydeadlinks,
        data.totallinks,
        data.totaldeadlinks
    ]

    for pair in xrange(2):
        for heaps in range(<int>(parPool[0].max * scale) + 1):
            parPool[0].parity[pair].heap[heaps].parnum = 0
            free(parPool[0].parity[pair].heap[heaps].par)
        free(parPool[0].parity[pair].heap)
    free(parPool[0].parity)
    free(parPool)

    if profiling == 1:
        print("-->export time", clock() - stime, "sec")
        print("-->all process time", clock() - stime2, "sec")
    return exportdata


cdef void update(mol_data):
    cdef int i = 0
    cdef int ii = 0
    for i in xrange(data.psysnum):
        for ii in xrange(data.psys[i].parnum):
            data.psys[i].particles[ii].loc[0] = mol_data[i][0][(ii * 3)]
            data.psys[i].particles[ii].loc[1] = mol_data[i][0][(ii * 3) + 1]
            data.psys[i].particles[ii].loc[2] = mol_data[i][0][(ii * 3) + 2]
            data.psys[i].particles[ii].vel[0] = mol_data[i][1][(ii * 3)]
            data.psys[i].particles[ii].vel[1] = mol_data[i][1][(ii * 3) + 1]
            data.psys[i].particles[ii].vel[2] = mol_data[i][1][(ii * 3) + 2]

            if data.psys[i].particles[ii].state == 0 and mol_data[i][2][ii] == 0:
                data.psys[i].particles[ii].state = mol_data[i][2][ii] + 1
                if data.psys[i].links_active == 1:
                    kd_tree.KDTree_rnn_query(
                        data.kdtree,
                        &data.psys[i].particles[ii],
                        data.psys[i].particles[ii].loc,
                        data.psys[i].particles[ii].sys.link_length
                    )
                    link.create_link(data.psys[i].particles[ii].id, data.psys[i].link_max)
                    # free(data.psys[i].particles[ii].neighbours)
                    data.psys[i].particles[ii].neighboursnum = 0

            elif data.psys[i].particles[ii].state == 1 and mol_data[i][2][ii] == 0:
                data.psys[i].particles[ii].state = 1

            else:
                data.psys[i].particles[ii].state = mol_data[i][2][ii]

            data.psys[i].particles[ii].collided_with = <int *>realloc(
                data.psys[i].particles[ii].collided_with,
                1 * cython.sizeof(int)
            )
            data.psys[i].particles[ii].collided_num = 0
