cimport types


cdef float fps = 0
cdef int substep = 0
cdef float deltatime = 0
cdef int parnum = 0
cdef int psysnum = 0
cdef int cpunum = 0
cdef int newlinks = 0
cdef int totallinks = 0
cdef int totaldeadlinks = 0
cdef int *deadlinks = NULL
cdef types.Particle *parlist = NULL
cdef types.SParticle *parlistcopy = NULL
cdef types.ParSys *psys = NULL
cdef types.KDTree *kdtree = NULL
