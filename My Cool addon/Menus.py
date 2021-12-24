#blender modules 
import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (PropertyGroup)

#other moduals 
import os
import random 


class TestPanel(bpy.types.Panel):



    bl_label = "test Panel"
    bl_idname = "PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My 1st Addon'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Add object", icon= "CUBE")
        row = layout.row()
        row.operator("mesh.primitive_cube_add", icon="CUBE")
        row = layout.row()
        row.operator("mesh.primitive_uv_sphere_add", icon="MESH_UVSPHERE")
        row = layout.row()
        row.operator("mesh.monkey_grid", icon="MONKEY")

        layout.separator()
        row.operator("mesh.subdivide", icon="MESH_GRID")

class WM_OT_pie_menu(bpy.types.Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Select Mode"
    bl_idname = "WM_OT_pie_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        pie.operator("mesh.subdivide", icon="MESH_GRID")
        pie.operator("bpy.context.object.data.use_auto_smooth = True", icon="MONKEY")

       

        mode = object.mode
        if mode == "OBJECT":
            pie.operator("mesh.primitive_uv_sphere_add")

        if mode == "EDIT":
             pie.operator("mesh.subdivide", icon="MESH_GRID")
             pie.operator("mesh.primitive_cube_add", icon="CUBE")







addon_keymaps = []
classes = [WM_OT_pie_menu, TestPanel]  
  

def register():
    for cls in classes:
        bpy.utils.register_class(cls)



    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("wm.call_menu_pie", type='BUTTON4MOUSE', value='PRESS')
        kmi.properties.name = "WM_OT_pie_menu"
        addon_keymaps.append((km,kmi))
    


    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    
if __name__ == '__main__':
    register()
