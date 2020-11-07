#cython: profile=False
#cython: boundscheck=False
#cython: cdivision=True

# NOTE: order of slow fonction to be optimize/multithreaded:
# kdtreesearching, kdtreecreating, linksolving


cimport cython
from cython.parallel import prange
from libc.stdlib cimport malloc, free

cimport data, types, kd_tree, link


cdef extern from "stdlib.h":
    ctypedef void const_void "const void"
    void qsort(
        void *base,
        int nmemb,
        int size,
        int(*compar)(const_void *, const_void *)
    )nogil


print("cmolcore imported with success! v1.12")


cpdef init(importdata):
    cdef int i = 0
    cdef int ii = 0
    cdef int profiling = 0
    data.newlinks = 0
    data.totallinks = 0
    data.totaldeadlinks = 0
    data.fps = float(importdata[0][0])
    data.substep = int(importdata[0][1])
    data.deltatime = (data.fps * (data.substep + 1))
    data.psysnum = importdata[0][2]
    data.parnum = importdata[0][3]
    data.cpunum = importdata[0][4]
    data.deadlinks = <int *>malloc(data.cpunum * cython.sizeof(int))
    print("  Number of cpu's used:", data.cpunum)
    data.psys = <types.ParSys *>malloc(data.psysnum * cython.sizeof(types.ParSys))
    data.parlist = <types.Particle *>malloc(data.parnum * cython.sizeof(types.Particle))
    data.parlistcopy = <types.SParticle *>malloc(data.parnum * cython.sizeof(types.SParticle))
    cdef int jj = 0
    for i in xrange(data.psysnum):
        data.psys[i].id = i
        data.psys[i].parnum = importdata[i + 1][0]
        data.psys[i].particles = <types.Particle *>malloc(data.psys[i].parnum * \
            cython.sizeof(types.Particle))
        data.psys[i].particles = &data.parlist[jj]
        for ii in xrange(data.psys[i].parnum):
            data.parlist[jj].id = jj
            data.parlist[jj].loc[0] = importdata[i + 1][1][(ii * 3)]
            data.parlist[jj].loc[1] = importdata[i + 1][1][(ii * 3) + 1]
            data.parlist[jj].loc[2] = importdata[i + 1][1][(ii * 3) + 2]
            data.parlist[jj].vel[0] = importdata[i + 1][2][(ii * 3)]
            data.parlist[jj].vel[1] = importdata[i + 1][2][(ii * 3) + 1]
            data.parlist[jj].vel[2] = importdata[i + 1][2][(ii * 3) + 2]
            data.parlist[jj].size = importdata[i + 1][3][ii]
            data.parlist[jj].mass = importdata[i + 1][4][ii]
            data.parlist[jj].state = importdata[i + 1][5][ii]
            data.psys[i].selfcollision_active = importdata[i + 1][6][0]
            data.psys[i].othercollision_active = importdata[i + 1][6][1]
            data.psys[i].collision_group = importdata[i + 1][6][2]
            data.psys[i].friction = importdata[i + 1][6][3]
            data.psys[i].collision_damp = importdata[i + 1][6][4]
            data.psys[i].links_active = importdata[i + 1][6][5]
            data.psys[i].link_length = importdata[i + 1][6][6]
            data.psys[i].link_max = importdata[i + 1][6][7]
            data.psys[i].link_tension = importdata[i + 1][6][8]
            data.psys[i].link_tensionrand = importdata[i + 1][6][9]
            data.psys[i].link_stiff = importdata[i + 1][6][10] * 0.5
            data.psys[i].link_stiffrand = importdata[i + 1][6][11]
            data.psys[i].link_stiffexp = importdata[i + 1][6][12]
            data.psys[i].link_damp = importdata[i + 1][6][13]
            data.psys[i].link_damprand = importdata[i + 1][6][14]
            data.psys[i].link_broken = importdata[i + 1][6][15]
            data.psys[i].link_brokenrand = importdata[i + 1][6][16]
            data.psys[i].link_estiff = importdata[i + 1][6][17] * 0.5
            data.psys[i].link_estiffrand = importdata[i + 1][6][18]
            data.psys[i].link_estiffexp = importdata[i + 1][6][19]
            data.psys[i].link_edamp = importdata[i + 1][6][20]
            data.psys[i].link_edamprand = importdata[i + 1][6][21]
            data.psys[i].link_ebroken = importdata[i + 1][6][22]
            data.psys[i].link_ebrokenrand = importdata[i + 1][6][23]
            data.psys[i].relink_group = importdata[i + 1][6][24]
            data.psys[i].relink_chance = importdata[i + 1][6][25]
            data.psys[i].relink_chancerand = importdata[i + 1][6][26]
            data.psys[i].relink_max = importdata[i + 1][6][27]
            data.psys[i].relink_tension = importdata[i + 1][6][28]
            data.psys[i].relink_tensionrand = importdata[i + 1][6][29]
            data.psys[i].relink_stiff = importdata[i + 1][6][30] * 0.5
            data.psys[i].relink_stiffexp = importdata[i + 1][6][31]
            data.psys[i].relink_stiffrand = importdata[i + 1][6][32]
            data.psys[i].relink_damp = importdata[i + 1][6][33]
            data.psys[i].relink_damprand = importdata[i + 1][6][34]
            data.psys[i].relink_broken = importdata[i + 1][6][35]
            data.psys[i].relink_brokenrand = importdata[i + 1][6][36]
            data.psys[i].relink_estiff = importdata[i + 1][6][37] * 0.5
            data.psys[i].relink_estiffexp = importdata[i + 1][6][38]
            data.psys[i].relink_estiffrand = importdata[i + 1][6][39]
            data.psys[i].relink_edamp = importdata[i + 1][6][40]
            data.psys[i].relink_edamprand = importdata[i + 1][6][41]
            data.psys[i].relink_ebroken = importdata[i + 1][6][42]
            data.psys[i].relink_ebrokenrand = importdata[i + 1][6][43]
            data.psys[i].link_friction = importdata[i + 1][6][44]
            data.psys[i].link_group = importdata[i + 1][6][45]
            data.psys[i].other_link_active = importdata[i + 1][6][46]

            data.parlist[jj].sys = &data.psys[i]
            data.parlist[jj].collided_with = <int *>malloc(1 * cython.sizeof(int))
            data.parlist[jj].collided_num = 0
            data.parlist[jj].links = <types.Links *>malloc(1 * cython.sizeof(types.Links))
            data.parlist[jj].links_num = 0
            data.parlist[jj].links_activnum = 0
            data.parlist[jj].link_with = <int *>malloc(1 * cython.sizeof(int))
            data.parlist[jj].link_withnum = 0
            data.parlist[jj].neighboursmax = 10
            data.parlist[jj].neighbours = <int *>malloc(data.parlist[jj].neighboursmax * \
                cython.sizeof(int))
            data.parlist[jj].neighboursnum = 0
            jj += 1

    jj = 0
    data.kdtree = <types.KDTree *>malloc(1 * cython.sizeof(types.KDTree))
    kd_tree.KDTree_create_nodes(data.kdtree, data.parnum)

    with nogil:
        for i in prange(
                        <int>data.parnum,
                        schedule='dynamic',
                        chunksize=10,
                        num_threads=data.cpunum
                        ):
            data.parlistcopy[i].id = data.parlist[i].id
            data.parlistcopy[i].loc[0] = data.parlist[i].loc[0]
            data.parlistcopy[i].loc[1] = data.parlist[i].loc[1]
            data.parlistcopy[i].loc[2] = data.parlist[i].loc[2]

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

    with nogil:
        for i in prange(
                        <int>data.parnum,
                        schedule='dynamic',
                        chunksize=10,
                        num_threads=data.cpunum
                        ):
            if data.parlist[i].sys.links_active == 1:
                kd_tree.KDTree_rnn_query(
                    data.kdtree,
                    &data.parlist[i],
                    data.parlist[i].loc,
                    data.parlist[i].sys.link_length
                )

    for i in xrange(data.parnum):
        link.create_link(data.parlist[i].id, data.parlist[i].sys.link_max)
        if data.parlist[i].neighboursnum > 1:
            # free(data.parlist[i].neighbours)
            data.parlist[i].neighboursnum = 0
    data.totallinks += data.newlinks
    print("  New links created: ", data.newlinks)
    return data.parnum
