import math

import bpy

from .utils import get_object


def pack_data(context, initiate):
    psyslen = 0
    parnum = 0
    scene = context.scene
    for ob in bpy.data.objects:
        obj = get_object(context, ob)

        for psys in obj.particle_systems:           
            if psys.settings.mol_matter != "-1":
                psys.settings.mol_density = float(psys.settings.mol_matter)
            if psys.settings.mol_active and len(psys.particles):
                parlen = len(psys.particles)
                par_loc = [0, 0, 0] * parlen
                par_vel = [0, 0, 0] * parlen
                par_size = [0] * parlen
                par_alive = []
                for par in psys.particles:
                    parnum += 1
                    if par.alive_state == "UNBORN":
                        par_alive.append(2)
                    if par.alive_state == "ALIVE":
                        par_alive.append(0)
                    if par.alive_state == "DEAD":
                        par_alive.append(3)

                psys.particles.foreach_get('location', par_loc)
                psys.particles.foreach_get('velocity', par_vel)

                if initiate:
                    par_mass = []

                    if psys.settings.mol_density_active:
                        for par in psys.particles:
                            par_mass.append(psys.settings.mol_density * (4 / 3 * math.pi * ((par.size / 2) ** 3)))
                    else:
                        for par in psys.particles:
                            par_mass.append(psys.settings.mass)

                    """
                    if scene.mol_timescale_active == True:
                        psys.settings.timestep = 1 / (scene.render.fps / scene.timescale)
                    else:
                        psys.settings.timestep = 1 / scene.render.fps 
                    """

                    psyslen += 1
                    psys.particles.foreach_get('size', par_size)
                    if bpy.context.scene.mol_minsize > min(par_size):
                        bpy.context.scene.mol_minsize = min(par_size)

                    if psys.settings.mol_link_samevalue:
                        psys.settings.mol_link_estiff = psys.settings.mol_link_stiff
                        psys.settings.mol_link_estiffrand = psys.settings.mol_link_stiffrand
                        psys.settings.mol_link_estiffexp = psys.settings.mol_link_stiffexp
                        psys.settings.mol_link_edamp = psys.settings.mol_link_damp
                        psys.settings.mol_link_edamprand = psys.settings.mol_link_damprand
                        psys.settings.mol_link_ebroken = psys.settings.mol_link_broken
                        psys.settings.mol_link_ebrokenrand = psys.settings.mol_link_brokenrand

                    if psys.settings.mol_relink_samevalue:
                        psys.settings.mol_relink_estiff = psys.settings.mol_relink_stiff
                        psys.settings.mol_relink_estiffrand = psys.settings.mol_relink_stiffrand
                        psys.settings.mol_relink_estiffexp = psys.settings.mol_relink_stiffexp
                        psys.settings.mol_relink_edamp = psys.settings.mol_relink_damp
                        psys.settings.mol_relink_edamprand = psys.settings.mol_relink_damprand
                        psys.settings.mol_relink_ebroken = psys.settings.mol_relink_broken
                        psys.settings.mol_relink_ebrokenrand = psys.settings.mol_relink_brokenrand

                    params = [0] * 47

                    params[0] = psys.settings.mol_selfcollision_active
                    params[1] = psys.settings.mol_othercollision_active
                    params[2] = psys.settings.mol_collision_group
                    params[3] = psys.settings.mol_friction
                    params[4] = psys.settings.mol_collision_damp
                    params[5] = psys.settings.mol_links_active

                    if psys.settings.mol_link_rellength:
                        params[6] = psys.settings.particle_size * psys.settings.mol_link_length
                    else:
                        params[6] = psys.settings.mol_link_length

                    params[7] = psys.settings.mol_link_max
                    params[8] = psys.settings.mol_link_tension
                    params[9] = psys.settings.mol_link_tensionrand
                    params[10] = psys.settings.mol_link_stiff
                    params[11] = psys.settings.mol_link_stiffrand
                    params[12] = psys.settings.mol_link_stiffexp
                    params[13] = psys.settings.mol_link_damp
                    params[14] = psys.settings.mol_link_damprand
                    params[15] = psys.settings.mol_link_broken
                    params[16] = psys.settings.mol_link_brokenrand
                    params[17] = psys.settings.mol_link_estiff
                    params[18] = psys.settings.mol_link_estiffrand
                    params[19] = psys.settings.mol_link_estiffexp
                    params[20] = psys.settings.mol_link_edamp
                    params[21] = psys.settings.mol_link_edamprand
                    params[22] = psys.settings.mol_link_ebroken
                    params[23] = psys.settings.mol_link_ebrokenrand
                    params[24] = psys.settings.mol_relink_group
                    params[25] = psys.settings.mol_relink_chance
                    params[26] = psys.settings.mol_relink_chancerand
                    params[27] = psys.settings.mol_relink_max
                    params[28] = psys.settings.mol_relink_tension
                    params[29] = psys.settings.mol_relink_tensionrand
                    params[30] = psys.settings.mol_relink_stiff
                    params[31] = psys.settings.mol_relink_stiffexp
                    params[32] = psys.settings.mol_relink_stiffrand
                    params[33] = psys.settings.mol_relink_damp
                    params[34] = psys.settings.mol_relink_damprand
                    params[35] = psys.settings.mol_relink_broken
                    params[36] = psys.settings.mol_relink_brokenrand
                    params[37] = psys.settings.mol_relink_estiff
                    params[38] = psys.settings.mol_relink_estiffexp
                    params[39] = psys.settings.mol_relink_estiffrand
                    params[40] = psys.settings.mol_relink_edamp
                    params[41] = psys.settings.mol_relink_edamprand
                    params[42] = psys.settings.mol_relink_ebroken
                    params[43] = psys.settings.mol_relink_ebrokenrand
                    params[44] = psys.settings.mol_link_friction  
                    params[45] = psys.settings.mol_link_group 
                    params[46] = psys.settings.mol_other_link_active 

                mol_exportdata = bpy.context.scene.mol_exportdata

                if initiate:
                    mol_exportdata[0][2] = psyslen
                    mol_exportdata[0][3] = parnum
                    mol_exportdata.append((
                        parlen,
                        par_loc,
                        par_vel,
                        par_size,
                        par_mass,
                        par_alive,
                        params
                    ))
                else:
                    mol_exportdata.append((par_loc, par_vel, par_alive))
