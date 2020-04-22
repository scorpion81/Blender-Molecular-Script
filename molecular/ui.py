import bpy

from . import names
from .utils import get_object


class MolecularPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Molecular Script"
    bl_idname = "OBJECT_PT_molecular"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "particle"

    @classmethod
    def poll(cls, context):
        return context.object.particle_systems.active

    def draw_header(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        row = layout.row()
        if not psys is None:
            row.prop(psys.settings, "mol_active", text='')

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        #for the data    
        psys_eval = get_object(context, context.object).particle_systems.active
        
        layout.enabled = psys.settings.mol_active
        row = layout.row()
        row.label(text=names.DENSITY)
        box = layout.box()
        box.prop(
            psys.settings,
            "mol_density_active"
        )
        subbox = box.box()
        subbox.enabled  = psys.settings.mol_density_active
        row = subbox.row()
        row.prop(psys.settings, "mol_matter")
        row = subbox.row()

        if int(psys.settings.mol_matter) == 0:
            row.enabled = True
        elif int(psys.settings.mol_matter) >= 1:
            row.enabled = False

        row.prop(psys.settings, "mol_density")
        pmass = (psys.settings.particle_size ** 3) * psys.settings.mol_density
        row = subbox.row()
        weight_text = "Total system approx weight: {0:.4} kg".format(
            len(psys_eval.particles) * pmass
        )
        row.label(icon="INFO", text=weight_text) 
        row = layout.row()
        row.label(text=names.COLLISION)
        box = layout.box()
        box.prop(
            psys.settings,
            "mol_selfcollision_active"
        )
        box.prop(
            psys.settings,
            "mol_othercollision_active"
        )
        box.prop(
            psys.settings,
            "mol_collision_group",
        )
        box.prop(
            psys.settings,
            "mol_friction",
        )
        box.prop(
            psys.settings,
            "mol_collision_damp"
        )

        row = layout.row()
        row.label(text=names.LINKS)
        box = layout.box()
        box.prop(
            psys.settings,
            "mol_links_active"
        )
        box.prop(
            psys.settings,
            "mol_other_link_active"
        )
        box.prop(
            psys.settings,
            "mol_link_group"
        )

        subbox = box.box()
        subbox.enabled = psys.settings.mol_links_active or \
                         psys.settings.mol_other_link_active
        subbox.label(text=names.INITIAL_LINKING)
        row = subbox.row()
        row.prop(psys.settings, "mol_link_length")
        row.prop(psys.settings, "mol_link_rellength")
        row = subbox.row()
        row.prop(psys.settings, "mol_link_max")
        row = subbox.row()
        row.prop(psys.settings, "mol_link_friction")
        layout.separator()
        row = subbox.row()
        row.prop(psys.settings, "mol_link_tension")
        row.prop(psys.settings, "mol_link_tensionrand")
        row = subbox.row()
        row.prop(psys.settings, "mol_link_stiff")
        row.prop(psys.settings, "mol_link_stiffrand")
        #row = subbox.row()
        #row.prop(psys.settings, "mol_link_stiffexp")
        row = subbox.row()
        row.prop(psys.settings, "mol_link_damp")
        row.prop(psys.settings, "mol_link_damprand")
        row = subbox.row()
        row.prop(psys.settings, "mol_link_broken")
        row.prop(psys.settings, "mol_link_brokenrand")
        row = subbox.row()
        layout.separator()
        row = subbox.row()
        row.prop(
            psys.settings,
            "mol_link_samevalue"
        )
        row = subbox.row()
        row.enabled = not psys.settings.mol_link_samevalue
        row.prop(psys.settings, "mol_link_estiff")
        row.prop(psys.settings, "mol_link_estiffrand")
        #row = subbox.row()
        #row.enabled = not psys.settings.mol_link_samevalue
        #row.prop(psys.settings, "mol_link_estiffexp")
        row = subbox.row()
        row.enabled = not psys.settings.mol_link_samevalue
        row.prop(psys.settings, "mol_link_edamp")
        row.prop(psys.settings, "mol_link_edamprand")
        row = subbox.row()
        row.enabled = not psys.settings.mol_link_samevalue
        row.prop(psys.settings, "mol_link_ebroken")
        row.prop(psys.settings, "mol_link_ebrokenrand")

        subbox = box.box()
        subbox.active = psys.settings.mol_links_active
        subbox.label(text=names.NEW_LINKING)
        row = subbox.row()
        row.prop(psys.settings, "mol_relink_group")
        row = subbox.row()
        row.prop(psys.settings, "mol_relink_chance")
        row.prop(psys.settings, "mol_relink_chancerand")
        row = subbox.row()
        row.prop(psys.settings, "mol_relink_max")
        row = subbox.row()
        layout.separator()
        row = subbox.row()
        row.prop(psys.settings,"mol_relink_tension")
        row.prop(psys.settings,"mol_relink_tensionrand")
        row = subbox.row()
        row.prop(psys.settings,"mol_relink_stiff")
        row.prop(psys.settings,"mol_relink_stiffrand")
        #row = subbox.row()
        #row.prop(psys.settings, "mol_relink_stiffexp")
        row = subbox.row()
        row.prop(psys.settings, "mol_relink_damp")
        row.prop(psys.settings, "mol_relink_damprand")
        row = subbox.row()
        row.prop(psys.settings, "mol_relink_broken")
        row.prop(psys.settings, "mol_relink_brokenrand")
        row = subbox.row()
        layout.separator()
        row = subbox.row()
        row.prop(
            psys.settings,
            "mol_relink_samevalue"
        )
        row = subbox.row()
        row.enabled = not psys.settings.mol_relink_samevalue
        row.prop(psys.settings, "mol_relink_estiff")
        row.prop(psys.settings, "mol_relink_estiffrand")
        #row = subbox.row()
        #row.enabled = not psys.settings.mol_relink_samevalue
        #row.prop(psys.settings, "mol_relink_estiffexp")
        row = subbox.row()
        row.enabled = not psys.settings.mol_relink_samevalue
        row.prop(psys.settings, "mol_relink_edamp")
        row.prop(psys.settings, "mol_relink_edamprand")
        row = subbox.row()
        row.enabled = not psys.settings.mol_relink_samevalue
        row.prop(psys.settings, "mol_relink_ebroken")
        row.prop(psys.settings, "mol_relink_ebrokenrand")

        row = layout.row()
        row.label(text=names.UVS)
        box = layout.box()
        row = box.row()

        if obj.data.uv_layers.active != None:
            row.prop(
                psys.settings,
                "mol_bakeuv",
                text="Bake UV at ending (current: \"{0}\")".format(
                    obj.data.uv_layers.active.name
                )
            )
        else:
            row.active = False
            row.prop(
                psys.settings,
                "mol_bakeuv",
                text="Bake UV at ending (current: None)"
            )

        row = layout.row()
        row.label(text='')
        row = layout.row()
        row.label(text=names.SIMULATE)
        row = layout.row()
        row.prop(scn, "frame_start", text="Start Frame")
        row.prop(scn, "frame_end", text="End Frame")

        # row = layout.row()
        # row.prop(scn,"mol_timescale_active", text="Activate TimeScaling")
        # row = layout.row()
        # row.enabled = scn.mol_timescale_active
        # row.prop(scn, "timescale", text="Time Scale")

        row = layout.row()
        row.prop(scn, "mol_substep")
        row.label(text='')
        row = layout.row()
        row.label(text=names.CPU_USED)
        row.prop(scn, "mol_cpu")
        row = layout.row()
        row.prop(scn, "mol_bake")
        row.prop(scn, "mol_render")
        row = layout.row()

        icon = 'PARTICLE_DATA'

        if scn.mol_simrun == False and psys.point_cache.is_baked == False:
            row.enabled = True
            row.operator(
                "object.mol_simulate",
                icon=icon,
                text="Start Molecular Simulation"
            )
            row = layout.row()
            row.enabled = False
            row.operator("ptcache.free_bake_all", text="Free All Bakes")

        if psys.point_cache.is_baked == True and scn.mol_simrun == False:
            row.enabled = False
            row.operator(
                "object.mol_simulate",
                icon=icon,
                text="Simulation baked"
            )
            row = layout.row()
            row.enabled = True
            row.operator("ptcache.free_bake_all", text="Free All Bakes")

        if scn.mol_simrun == True:
            row.enabled = False
            row.operator(
                "object.mol_simulate",
                icon=icon,
                text="Process: {} left".format(scn.mol_timeremain)
            )
            row = layout.row()
            row.enabled = False
            row.operator("ptcache.free_bake_all", text="Free All Bakes")

        box = layout.box()
        row = box.row()
        box.enabled = True
        row.label(text=names.MOLECULAR_TOOLS, icon='MODIFIER')
        subbox = box.box()
        row = subbox.row()
        row.label(text=names.PARTICLE_UV)
        row = subbox.row()
        row.alignment = 'CENTER'
        row.label(icon='INFO', text=names.SET_POSITION)
        row = subbox.row()
        row.alignment = 'CENTER'
        row.label(text=names.UV_HELP)
        row = subbox.row()
        row.alignment = 'CENTER'
        row.label(text=names.CYCLES_HELP)
        row = subbox.row()
        row.operator(
            "object.mol_set_global_uv",
            icon='GROUP_UVS',
            text="Set Global UV"
        )
        row = subbox.row()

        if obj.data.uv_layers.active != None:
            row.operator(
                "object.mol_set_active_uv",
                icon='GROUP_UVS',
                text = "Set Active UV (current: \"{0}\")".format(
                    obj.data.uv_layers.active.name
                )
            )
        else:
            row.active = False
            row.operator(
                "object.mol_set_active_uv",
                icon='GROUP_UVS',
                text="Set Active UV (no uvs found)"
            )

        subbox = box.box()
        row = subbox.row()
        row.label(text=names.SUBSTEPS_CALCULATOR)
        row = subbox.row()
        row.label(
            icon='INFO',
            text="Current systems have: {} particles".format(len(psys_eval.particles))
        )
        row = subbox.row()
        row.prop(psys.settings, "mol_var1")
        row = subbox.row()
        row.prop(psys.settings,"mol_var2")
        row = subbox.row()
        row.prop(psys.settings,"mol_var3")
        diff = (psys.settings.mol_var3 / psys.settings.mol_var1)
        factor = psys.settings.mol_var3 ** (1 / 3) / psys.settings.mol_var1 ** (1 / 3)
        newsubstep = int(round(factor * psys.settings.mol_var2))
        row = subbox.row()
        row.label(
            icon='FORWARD',
            text="You must set new substep to: {}".format(newsubstep)
        )
        row = subbox.row()
        row.label(
            icon='ERROR',
            text="Multiply particles size by: {}".format(round(1 / factor, 5))
        )
        row = subbox.row()
        row.label(
            icon='ERROR',
            text="Multiply others sys particle number by: {}".format(round(diff, 5))
        )

        box = layout.box()
        row = box.row()
        box.active = False
        box.alert = False
        row.alignment = 'CENTER'
        row.label(text=names.THANKS)
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=names.SUPPORT_WORK)
        row = box.row()
        row.alignment = 'CENTER'
        row.operator(
            "wm.url_open",
            text="click here to Donate",
            icon='URL'
        ).url = "www.pyroevil.com/donate/"
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=names.VISIT)
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=names.SITE)
