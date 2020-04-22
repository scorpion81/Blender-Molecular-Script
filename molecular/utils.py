import bpy


def get_object(context, obj):
    depsgraph = context.evaluated_depsgraph_get()
    return obj.evaluated_get(depsgraph)


def destroy_caches(obj):
    for psys in obj.particle_systems:
        # attempt to destroy cache prior to resimulation
        # by provoking an internal RNA update call, this will also update the psys for get_object
        if psys.settings.mol_active:
            step = psys.point_cache.frame_step
            psys.point_cache.frame_step = step
