import bpy

from . import names
from .utils import get_object


class MolecularBasePanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "particle"
    bl_options = {'DEFAULT_CLOSED', }

    @classmethod
    def poll(cls, context):
        return context.object.particle_systems.active


class MolecularDensityPanel(MolecularBasePanel):
    bl_label = names.DENSITY
    bl_idname = "OBJECT_PT_molecular_density"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active

        layout.prop(psys.settings, "mol_density_active", toggle=True)

        if not psys.settings.mol_density_active:
            return

        layout.prop(psys.settings, "mol_matter")

        if int(psys.settings.mol_matter) >= 1:
            weight_text = "Total system approx weight: {0:.4} kg".format(
                psys.settings.mol_matter
            )
            layout.label(icon="INFO", text=weight_text)
            return

        layout.prop(psys.settings, "mol_density")
        pmass = (psys.settings.particle_size ** 3) * psys.settings.mol_density
        weight_text = "Total system approx weight: {0:.2f} kg".format(
            len(psys_eval.particles) * pmass
        )
        layout.label(icon="INFO", text=weight_text) 


class MolecularCollisionPanel(MolecularBasePanel):
    bl_label = names.COLLISION
    bl_idname = "OBJECT_PT_molecular_collision"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        # particle system settings
        stg = psys.settings

        layout.enabled = stg.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active

        layout.prop(stg, "mol_selfcollision_active", toggle=True)
        layout.prop(stg, "mol_othercollision_active", toggle=True)
        if stg.mol_othercollision_active:
            layout.prop(stg, "mol_collision_group")
        if stg.mol_selfcollision_active or stg.mol_othercollision_active:
            layout.prop(stg, "mol_friction")
            layout.prop(stg, "mol_collision_damp")


class MolecularLinksPanel(MolecularBasePanel):
    bl_label = names.LINKS
    bl_idname = "OBJECT_PT_molecular_links"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol_active

        layout.prop(psys.settings, "mol_links_active", toggle=True)
        layout.prop(psys.settings, "mol_other_link_active", toggle=True)
        if psys.settings.mol_other_link_active:
            layout.prop(psys.settings, "mol_link_group")


class MolecularInitLinksPanel(MolecularBasePanel):
    bl_label = names.INITIAL_LINKING
    bl_idname = "OBJECT_PT_molecular_init_links"
    bl_parent_id = 'OBJECT_PT_molecular_links'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings
        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
        )

        row = layout.row()
        row.prop(psys.settings, "mol_link_length")
        row.prop(psys.settings, "mol_link_rellength")
        row = layout.row()
        row.prop(psys.settings, "mol_link_max")
        row = layout.row()
        row.prop(psys.settings, "mol_link_friction")
        layout.separator()
        row = layout.row()
        row.prop(psys.settings, "mol_link_tension")
        row.prop(psys.settings, "mol_link_tensionrand")
        row = layout.row()
        row.prop(psys.settings, "mol_link_samevalue", toggle=True)
        if not psys.settings.mol_link_samevalue:
            layout.label(text='Compression:')
        row = layout.row()
        row.prop(psys.settings, "mol_link_stiff")
        row.prop(psys.settings, "mol_link_stiffrand")
        #row = layout.row()
        #row.prop(psys.settings, "mol_link_stiffexp")
        row = layout.row()
        row.prop(psys.settings, "mol_link_damp")
        row.prop(psys.settings, "mol_link_damprand")
        row = layout.row()
        row.prop(psys.settings, "mol_link_broken")
        row.prop(psys.settings, "mol_link_brokenrand")
        if not psys.settings.mol_link_samevalue:
            layout.label(text='Expansion:')
            row = layout.row()
            row.enabled = not psys.settings.mol_link_samevalue
            row.prop(psys.settings, "mol_link_estiff")
            row.prop(psys.settings, "mol_link_estiffrand")
            #row = layout.row()
            #row.enabled = not psys.settings.mol_link_samevalue
            #row.prop(psys.settings, "mol_link_estiffexp")
            row = layout.row()
            row.enabled = not psys.settings.mol_link_samevalue
            row.prop(psys.settings, "mol_link_edamp")
            row.prop(psys.settings, "mol_link_edamprand")
            row = layout.row()
            row.enabled = not psys.settings.mol_link_samevalue
            row.prop(psys.settings, "mol_link_ebroken")
            row.prop(psys.settings, "mol_link_ebrokenrand")


class MolecularNewLinksPanel(MolecularBasePanel):
    bl_label = names.NEW_LINKING
    bl_idname = "OBJECT_PT_molecular_new_links"
    bl_parent_id = 'OBJECT_PT_molecular_links'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        stg = psys.settings

        layout.enabled = stg.mol_active and (
            stg.mol_links_active or stg.mol_other_link_active
        )
        row = layout.row()
        row.prop(psys.settings, "mol_relink_group")
        row = layout.row()
        row.prop(psys.settings, "mol_relink_chance")
        row.prop(psys.settings, "mol_relink_chancerand")
        row = layout.row()
        row.prop(psys.settings, "mol_relink_max")
        row = layout.row()
        layout.separator()
        row = layout.row()
        row.prop(psys.settings,"mol_relink_tension")
        row.prop(psys.settings,"mol_relink_tensionrand")
        row = layout.row()
        row.prop(psys.settings, "mol_relink_samevalue", toggle=True)
        if not psys.settings.mol_relink_samevalue:
            layout.label(text='Compression:')
        row = layout.row()
        row.prop(psys.settings,"mol_relink_stiff")
        row.prop(psys.settings,"mol_relink_stiffrand")
        #row = layout.row()
        #row.prop(psys.settings, "mol_relink_stiffexp")
        row = layout.row()
        row.prop(psys.settings, "mol_relink_damp")
        row.prop(psys.settings, "mol_relink_damprand")
        row = layout.row()
        row.prop(psys.settings, "mol_relink_broken")
        row.prop(psys.settings, "mol_relink_brokenrand")
        row = layout.row()
        if not psys.settings.mol_relink_samevalue:
            layout.label(text='Expansion:')
            row = layout.row()
            row.prop(psys.settings, "mol_relink_estiff")
            row.prop(psys.settings, "mol_relink_estiffrand")
            #row = layout.row()
            #row.enabled = not psys.settings.mol_relink_samevalue
            #row.prop(psys.settings, "mol_relink_estiffexp")
            row = layout.row()
            row.prop(psys.settings, "mol_relink_edamp")
            row.prop(psys.settings, "mol_relink_edamprand")
            row = layout.row()
            row.prop(psys.settings, "mol_relink_ebroken")
            row.prop(psys.settings, "mol_relink_ebrokenrand")


class MolecularSimulatePanel(MolecularBasePanel):
    bl_label = names.SIMULATE
    bl_idname = "OBJECT_PT_molecular_simulate"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active

        layout.prop(scn, "frame_start", text="Start Frame")
        layout.prop(scn, "frame_end", text="End Frame")

        # row = layout.row()
        # row.prop(scn,"mol_timescale_active", text="Activate TimeScaling")
        # row = layout.row()
        # row.enabled = scn.mol_timescale_active
        # row.prop(scn, "timescale", text="Time Scale")

        layout.prop(scn, "mol_substep")
        layout.prop(scn, "mol_cpu", text=names.CPU_USED)
        layout.prop(scn, "mol_bake")
        layout.prop(scn, "mol_render")

        row = layout.row()

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


class MolecularToolsPanel(MolecularBasePanel):
    bl_label = names.MOLECULAR_TOOLS
    bl_idname = "OBJECT_PT_molecular_tools"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active

        box = layout.box()
        row = box.row()
        row.label(text=names.PARTICLE_UV)
        row = box.row()
        row.alignment = 'CENTER'
        row.label(icon='INFO', text=names.SET_POSITION)
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=names.UV_HELP)
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text=names.CYCLES_HELP)
        row = box.row()
        row.operator(
            "object.mol_set_global_uv",
            icon='GROUP_UVS',
            text="Set Global UV"
        )
        row = box.row()

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

        box = layout.box()
        row = box.row()
        row.label(text=names.SUBSTEPS_CALCULATOR)
        row = box.row()
        row.label(
            icon='INFO',
            text="Current systems have: {} particles".format(len(psys_eval.particles))
        )
        row = box.row()
        row.prop(psys.settings, "mol_var1")
        row = box.row()
        row.prop(psys.settings,"mol_var2")
        row = box.row()
        row.prop(psys.settings,"mol_var3")
        diff = (psys.settings.mol_var3 / psys.settings.mol_var1)
        factor = psys.settings.mol_var3 ** (1 / 3) / psys.settings.mol_var1 ** (1 / 3)
        newsubstep = int(round(factor * psys.settings.mol_var2))
        row = box.row()
        row.label(
            icon='FORWARD',
            text="You must set new substep to: {}".format(newsubstep)
        )
        row = box.row()
        row.label(
            icon='ERROR',
            text="Multiply particles size by: {}".format(round(1 / factor, 5))
        )
        row = box.row()
        row.label(
            icon='ERROR',
            text="Multiply others sys particle number by: {}".format(round(diff, 5))
        )


class MolecularAboutPanel(MolecularBasePanel):
    bl_label = 'About'
    bl_idname = "OBJECT_PT_molecular_about"
    bl_parent_id = 'OBJECT_PT_molecular'

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol_active
        # for the data    
        psys_eval = get_object(context, context.object).particle_systems.active

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


class MolecularPanel(MolecularBasePanel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Molecular"
    bl_idname = "OBJECT_PT_molecular"

    def draw_header(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        row = layout.row()
        if not psys is None:
            row.prop(psys.settings, "mol_active", text='')

    def draw(self, context):
        layout = self.layout
        obj = context.object
        psys = obj.particle_systems.active
        if psys is None:
            return
        layout.enabled = psys.settings.mol_active


panel_classes = (
    MolecularPanel,
    MolecularSimulatePanel,
    MolecularDensityPanel,
    MolecularCollisionPanel,
    MolecularLinksPanel,
    MolecularInitLinksPanel,
    MolecularNewLinksPanel,
    MolecularToolsPanel,
    MolecularAboutPanel
)
