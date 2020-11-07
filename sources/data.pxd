cimport types


cdef float fps
cdef int substep
cdef float deltatime
cdef int parnum
cdef int psysnum
cdef int cpunum
cdef int newlinks
cdef int totallinks
cdef int totaldeadlinks
cdef int *deadlinks
cdef types.Particle *parlist
cdef types.SParticle *parlistcopy
cdef types.ParSys *psys
cdef types.KDTree *kdtree
