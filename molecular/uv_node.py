import bpy
from bpy.types import Node

# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class CustomShaderTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ShaderNodeTree'


# Derived from the Node base type.
class UVNode(Node, CustomShaderTreeNode):
    # === Basics ===
    # Description string
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'UVNode'
    # Label for nice name display
    bl_label = "UV Node"
    # Icon identifier
    bl_icon = 'UV'

    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Properties
    #psys_name: bpy.props.StringProperty()

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!
    def init(self, context):
        self.inputs.new('NodeSocketObject', "Object")
        self.inputs.new('NodeSocketInt', "Particle System")
        self.inputs.new('NodeSocketInt', "Particle")

        self.outputs.new('NodeSocketVector', "UV")

    def update(self):
        if not self.inputs[0].is_linked:
            ob = self.inputs[0].default_value
        else:
            ob = self.inputs[0].links[0].from_socket.default_value

        if not self.inputs[1].is_linked:
            idx = self.inputs[1].default_value
        else:
            idx = self.inputs[1].links[0].from_socket.default_value

        pidx = self.inputs[2].default_value

        if ob is not None:
            depg = bpy.context.evaluated_depsgraph_get()
            ob_eval = ob.evaluated_get(depg)
            psys = ob_eval.particle_systems[idx]
            # doesnt work, those sockets are not smart enough python-wise :(
            uv = [0, 0, 0] * len(psys.particles)
            psys.particles.foreach_get("angular_velocity", uv)
            for l in self.outputs[0].links:
                l.to_socket.default_value = uv
            # just iterating over the loop doesnt work either
            #for i, p in enumerate(psys.particles):
            #    if self.outputs[0].is_linked:
            #        for l in self.outputs[0].links:
            #            l.to_socket.default_value = p.angular_velocity

            # here you could get exactly one color, but how shall you combine them ?
            #self.outputs[0].default_value = psys.particles[pidx].angular_velocity
            
            #probably the Particle Info Node does some black instancer magic behind the scenes, not exposed to the nodes
            #and not even speaking of python nodes in particular :( :(
