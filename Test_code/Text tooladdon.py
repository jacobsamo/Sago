bl_info = {
    "name": "Render and shutdown pc",
    "author": "Jacob Samorowski email:jacob35422@gmail.com",
    "version": (0, 0, 1),
    "blender": (2, 65, 0),
    "location": "render > Render and shutdown",
    "description": "Once render is finished it will save the blend file and shutdown your pc",
    "warning": "",
    "doc_url": "https://github.com/Eirfire/Blender-addon.wiki.git",
    "tracker_url": "",
    "category": "Render",
}
import random
import bpy
import os

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
classes = [TestPanel,
WM_OT_pie_menu,

]  
################### Register and unregister  
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
