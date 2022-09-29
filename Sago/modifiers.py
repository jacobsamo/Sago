import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Panel, Menu, Operator, PropertyGroup, AddonPreferences)






class sago_mod_subsurf(Operator):
    bl_idname = "sago.modifier_subsurf"
    bl_label = "Adds a subsurf modifier"
    
    def execute(self, context):
        bpy.context.active_object.modifiers.new("Sago Subdiv", 'SUBSURF')
        return {'FINISHED'}

class sago_mod_displace(Operator):
    bl_idname = "sago.modifier_displace"
    bl_label = "Adds a Displacement modifier"
    
    def execute(self, context):
        bpy.context.active_object.modifiers.new("Sago Dsiplace", 'DISPLACE')
        return {'FINISHED'}

class sago_mod_array(Operator):
    bl_idname = "sago.modifier_array"
    bl_label = "Adds an Array modifier"
    
    def execute(self, context):
        bpy.context.active_object.modifiers.new("Sago array", 'ARRAY')
        return {'FINISHED'}

class sago_mod_wireframe(Operator):
    bl_idname = "sago.modifier_wireframe"
    bl_label = "Adds a wireframe modifier"
    
    def execute(self, context):
        bpy.context.active_object.modifiers.new("Sago Wireframe", 'WIREFRAME')
        return {'FINISHED'}

classes = (
    sago_mod_subsurf,
    sago_mod_displace,
    sago_mod_array,
    sago_mod_wireframe,
)
def register():
    # Importing register class
    from bpy.utils import register_class

    # Registering main classes:
    for cls in classes:
        register_class(cls)

def unregister():
    # Importing unregister class
    from bpy.utils import unregister_class

    # Unregistering main classes:
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()