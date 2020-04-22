#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

bl_info = {
    "name": "Molecular",
    "author":
        "Jean-Francois Gallant (PyroEvil), "
        "Pavel_Blend, "
        "Martin Felke (scorpion81)",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "Properties editor > Particles Tabs",
    "description":
        "Addon for calculating collisions "
        "and for creating links between particles",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "http://pyroevil.com/molecular-script-docs/",
    "tracker_url": "http://pyroevil.com/contact/" ,
    "category": "Physics"
}


def register():

    import bpy

    from . import properties, ui, operators

    properties.define_props()
    bpy.utils.register_class(operators.MolSimulateModal)
    bpy.utils.register_class(operators.MolSimulate)
    bpy.utils.register_class(operators.MolSetGlobalUV)
    bpy.utils.register_class(operators.MolSetActiveUV)
    for panel in ui.panel_classes:
        bpy.utils.register_class(panel)


def unregister():

    import bpy

    from . import properties, ui, operators

    bpy.utils.unregister_class(operators.MolSimulateModal)
    bpy.utils.unregister_class(operators.MolSimulate)
    bpy.utils.unregister_class(operators.MolSetGlobalUV)
    bpy.utils.unregister_class(operators.MolSetActiveUV)
    for panel in reversed(ui.panel_classes):
        bpy.utils.unregister_class(panel)


if __name__ == "__main__":
    register()
