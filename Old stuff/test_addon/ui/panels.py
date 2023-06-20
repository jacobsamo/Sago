import bpy

class SimplePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_simple_panel"
    bl_label = "Simple Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My Addon'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.simple_operator", text="Run Simple Operator")

def register():
    bpy.utils.register_class(SimplePanel)

def unregister():
    bpy.utils.unregister_class(SimplePanel)
