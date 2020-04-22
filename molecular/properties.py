import multiprocessing

import bpy

from . import descriptions


def define_props():
    parset = bpy.types.ParticleSettings

    parset.mol_active = bpy.props.BoolProperty(
        name="mol_active", description=descriptions.ACTIVE, default=False
    )
    parset.mol_refresh = bpy.props.BoolProperty(
        name="mol_refresh", description=descriptions.REFRESH, default=True
    )
    parset.mol_density_active = bpy.props.BoolProperty(
        name="Calculate particles weight by density",
        description=descriptions.DENSITY_ACTIVE,
        default=False
    )

    matter_items = [
        ("-1", "custom", descriptions.MATTER_CUSTOM),
        ("1555", "sand", descriptions.MATTER_SAND),
        ("1000", "water", descriptions.MATTER_WATER),
        ("7800", "iron", descriptions.MATTER_IRON)
    ]

    parset.mol_matter = bpy.props.EnumProperty(
        name='Preset',
        items=matter_items,
        description=descriptions.MATTER
    )
    parset.mol_density = bpy.props.FloatProperty(
        name="Kg per CubeMeter:", description=descriptions.DENSITY,
        default=1000, min=0.001
    )

    parset.mol_selfcollision_active = bpy.props.BoolProperty(
        name="Activate Self Collision",
        description=descriptions.SELF_COLLISION_ACTIVE,
        default=False
    )
    parset.mol_othercollision_active = bpy.props.BoolProperty(
        name="Activate Collision with others",
        description=descriptions.OTHER_COLLISION_ACTIVE,
        default=False
    )
    parset.mol_friction = bpy.props.FloatProperty(
        name='Friction:', description=descriptions.FRICTION,
        default=0.005, min=0, max=1, precision=6, subtype='FACTOR'
    )
    parset.mol_collision_damp = bpy.props.FloatProperty(
        name="Damping:", description=descriptions.COLLISION_DAMPING,
        default=0.005, min=0, max=1, precision=6, subtype='FACTOR'
    )

    parset.mol_collision_group = bpy.props.IntProperty(
        name='Collide only with:', default=1, min=1,
        description=descriptions.COLLISION_GROUP
    )

    parset.mol_links_active = bpy.props.BoolProperty(
        name="Activate Particles linking",
        description=descriptions.LINKS_ACTIVE,
        default=False
    )
    parset.mol_other_link_active = bpy.props.BoolProperty(
        name="Activate Particles linking with Others",
        description=descriptions.LINK_OTHER_ACTIVE, default=False
        )

    parset.mol_link_group = bpy.props.IntProperty(
        name='Linking only with:', default=1, min=1,
        description=descriptions.LINK_GROUP
    )

    parset.mol_link_rellength = bpy.props.BoolProperty(
        name="Relative",
        description=descriptions.LINK_RELATIVE_LENGTH,
        default=True
    )
    parset.mol_link_friction = bpy.props.FloatProperty(
        name="Link friction", description=descriptions.LINK_FRICTION,
        min=0, max=1, default=0.005, precision=6, subtype='FACTOR'
    )
    parset.mol_link_length = bpy.props.FloatProperty(
        name="Search Length", description=descriptions.LINK_LENGTH,
        min=0, precision=6, default=1
    )
    parset.mol_link_tension = bpy.props.FloatProperty(
        name="Tension", description=descriptions.LINK_TENSION,
        min=0, precision=6, default=1
    )
    parset.mol_link_tensionrand = bpy.props.FloatProperty(
        name="Rand Tension",
        description=descriptions.LINK_TENSION_RANDOM,
        min=0, max=1, precision=6, default=0, subtype='FACTOR'
    )
    parset.mol_link_max = bpy.props.IntProperty(
        name="Max links", description=descriptions.LINK_MAX,
        min=0, default=16
    )
    parset.mol_link_stiff = bpy.props.FloatProperty(
        name="Stiff", description=descriptions.LINK_STIFFNESS,
        min=0, max=1, default=1, precision=6, subtype='FACTOR'
    )
    parset.mol_link_stiffrand = bpy.props.FloatProperty(
        name="Rand Stiff",
        description = descriptions.LINK_STIFFNESS_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )
    parset.mol_link_stiffexp = bpy.props.IntProperty(
        name="Exponent",
        description=descriptions.LINK_STIFFNESS_EXPONENT,
        default=1, min=1, max=10
    )
    parset.mol_link_damp = bpy.props.FloatProperty(
        name="Damping", description=descriptions.LINK_DAMPING,
        min=0, max=1, default=1, precision=6, subtype='FACTOR'
    )
    parset.mol_link_damprand = bpy.props.FloatProperty(
        name="Rand Damping", description=descriptions.LINK_DAMPING_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )
    parset.mol_link_broken = bpy.props.FloatProperty(
        name="Broken", description=descriptions.LINK_BROKEN,
        min=0, default=0.5, precision=6
    )
    parset.mol_link_brokenrand = bpy.props.FloatProperty(
        name="Rand Broken",
        description=descriptions.LINK_BROKEN_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )

    parset.mol_link_samevalue = bpy.props.BoolProperty(
        name="Same values for compression/expansion",
        description=descriptions.LINK_SAME_VALUE,
        default=True
    )

    parset.mol_link_estiff = bpy.props.FloatProperty(
        name="E Stiff",
        description=descriptions.LINK_EXPENSION_STIFFNESS,
        min=0, max=1, default=1, precision=6, subtype='FACTOR'
    )
    parset.mol_link_estiffrand = bpy.props.FloatProperty(
        name="Rand E Stiff",
        description=descriptions.LINK_EXPENSION_STIFFNESS_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )
    parset.mol_link_estiffexp = bpy.props.IntProperty(
        name="E Exponent",
        description=descriptions.LINK_EXPENSION_STIFFNESS_EXPONENT,
        default=1, min=1, max=10
    )
    parset.mol_link_edamp = bpy.props.FloatProperty(
        name="E Damping", description=descriptions.LINK_EXPENSION_DAMPING,
        min=0, max=1, default=1, precision=6, subtype='FACTOR'
    )
    parset.mol_link_edamprand = bpy.props.FloatProperty(
        name="Rand E Damping",
        description=descriptions.LINK_EXPENSION_DAMPING_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )
    parset.mol_link_ebroken = bpy.props.FloatProperty(
        name="E Broken",
        description=descriptions.LINK_EXPENSION_BROKEN,
        min=0, default=0.5, precision=6
    )
    parset.mol_link_ebrokenrand = bpy.props.FloatProperty(
        name="Rand E Broken",
        description=descriptions.LINK_EXPENSION_BROKEN_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )

    parset.mol_relink_group = bpy.props.IntProperty(
        name='Only links with:',
        default=1, min=1, description=descriptions.RELINK_GROUP
    )        

    parset.mol_relink_chance = bpy.props.FloatProperty(
        name="% Linking",
        description=descriptions.RELINK_CHANCE,
        min=0, max=100, default=0, precision=6
    )
    parset.mol_relink_chancerand = bpy.props.FloatProperty(
        name="Rand % Linking",
        description=descriptions.RELINK_CHANCE_RANDOM,
        default=0, min=0, max=1, precision=6, subtype='FACTOR'
    )
    parset.mol_relink_tension = bpy.props.FloatProperty(
        name="Tension",
        description=descriptions.RELINK_TENSION,
        min=0, precision=6, default=1
    )
    parset.mol_relink_tensionrand = bpy.props.FloatProperty(
        name="Rand Tension",
        description=descriptions.RELINK_TENSION_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )
    parset.mol_relink_max = bpy.props.IntProperty(
        name="Max links",
        description=descriptions.RELINK_MAX,
        min=0, default=16
    )
    parset.mol_relink_stiff = bpy.props.FloatProperty(
        name="Stiff",
        description=descriptions.RELINK_STIFFNESS,
        min=0, max=1, default=1, precision=6, subtype='FACTOR'
    )
    parset.mol_relink_stiffrand = bpy.props.FloatProperty(
        name="Rand Stiff",
        description=descriptions.RELINK_STIFFNESS_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )
    parset.mol_relink_stiffexp = bpy.props.IntProperty(
        name="Exponent",
        description=descriptions.RELINK_STIFFNESS_EXPONENT,
        min=1, max=10, default=1
    )
    parset.mol_relink_damp = bpy.props.FloatProperty(
        name="Damping",
        description=descriptions.RELINK_DAMPING,
        min=0, max=1, default=1, precision=6, subtype='FACTOR'
    )
    parset.mol_relink_damprand = bpy.props.FloatProperty(
        name="Rand Damping",
        description=descriptions.RELINK_DAMPING_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )
    parset.mol_relink_broken = bpy.props.FloatProperty(
        name="Broken",
        description=descriptions.RELINK_BROKEN,
        min=0, default=0.5, precision=6
    )
    parset.mol_relink_brokenrand = bpy.props.FloatProperty(
        name="Rand Broken",
        description=descriptions.RELINK_BROKEN_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )

    parset.mol_relink_samevalue = bpy.props.BoolProperty(
        name="Same values for compression/expansion",
        description=descriptions.RELINK_SAME_VALUE,
        default=True
    )

    parset.mol_relink_estiff = bpy.props.FloatProperty(
        name="E Stiff",
        description=descriptions.RELINK_EXPENSION_STIFFNESS,
        min=0, max=1, default=1, precision=6, subtype='FACTOR'
    )
    parset.mol_relink_estiffrand = bpy.props.FloatProperty(
        name="Rand E Stiff",
        description=descriptions.RELINK_EXPENSION_STIFFNESS_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )
    parset.mol_relink_estiffexp = bpy.props.IntProperty(
        name="Exponent",
        description=descriptions.RELINK_EXPENSION_STIFFNESS_EXPONENT,
        min=1, max=10, default=1
    )
    parset.mol_relink_edamp = bpy.props.FloatProperty(
        name="E Damping",
        description=descriptions.RELINK_EXPENSION_DAMPING,
        min=0, max=1, default=1, precision=6, subtype='FACTOR'
    )
    parset.mol_relink_edamprand = bpy.props.FloatProperty(
        name="Rand E Damping",
        description=descriptions.RELINK_EXPENSION_DAMPING_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )
    parset.mol_relink_ebroken = bpy.props.FloatProperty(
        name="E Broken",
        description=descriptions.RELINK_EXPENSION_BROKEN,
        min=0, default=0.5, precision=6
    )
    parset.mol_relink_ebrokenrand = bpy.props.FloatProperty(
        name="Rand E Broken",
        description=descriptions.RELINK_EXPENSION_BROKEN_RANDOM,
        min=0, max=1, default=0, precision=6, subtype='FACTOR'
    )

    parset.mol_var1 = bpy.props.IntProperty(
        name="Current numbers of particles",
        description=descriptions.VAR_1,
        min=1, default=1000
    )
    parset.mol_var2 = bpy.props.IntProperty(
        name="Current substep",
        description=descriptions.VAR_2,
        min=1, default=4
    )
    parset.mol_var3=bpy.props.IntProperty(
        name="Targeted numbers of particles",
        description=descriptions.VAR_3,
        min=1, default=1000
    )
    parset.mol_bakeuv = bpy.props.BoolProperty(
        name="mol_bakeuv",
        description=descriptions.BAKE_UV,
        default=False
    )

    bpy.types.Scene.mol_timescale_active = bpy.props.BoolProperty(
        name="mol_timescale_active",
        description=descriptions.TIME_SCALE_ACTIVE,
        default=False
    )
    bpy.types.Scene.timescale = bpy.props.FloatProperty(
        name="timescale",
        description=descriptions.TIME_SCALE,
        default=1
    )
    bpy.types.Scene.mol_substep = bpy.props.IntProperty(
        name="Substeps",
        description=descriptions.SUBSTEP,
        min=0, max=900, default=4
    )
    bpy.types.Scene.mol_bake = bpy.props.BoolProperty(
        name="Bake all at ending",
        description=descriptions.BAKE,
        default=True
    )
    bpy.types.Scene.mol_render = bpy.props.BoolProperty(
        name="Render at ending",
        description=descriptions.RENDER,
        default=False
    )
    bpy.types.Scene.mol_cpu = bpy.props.IntProperty(
        name="CPU",
        description=descriptions.CPU,
        default=multiprocessing.cpu_count(),
        min=1, max =multiprocessing.cpu_count()
    )

    bpy.types.Scene.mol_exportdata = []
    bpy.types.Scene.mol_minsize = bpy.props.FloatProperty()
    bpy.types.Scene.mol_simrun = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.mol_timeremain = bpy.props.StringProperty()
    bpy.types.Scene.mol_old_endframe = bpy.props.IntProperty()
    bpy.types.Scene.mol_newlink = bpy.props.IntProperty()
    bpy.types.Scene.mol_deadlink = bpy.props.IntProperty()
    bpy.types.Scene.mol_totallink = bpy.props.IntProperty()
    bpy.types.Scene.mol_totaldeadlink = bpy.props.IntProperty()
    bpy.types.Scene.mol_objuvbake = bpy.props.StringProperty()
    bpy.types.Scene.mol_psysuvbake = bpy.props.StringProperty()
    bpy.types.Scene.mol_stime = bpy.props.FloatProperty()
