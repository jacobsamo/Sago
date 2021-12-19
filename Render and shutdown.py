bl_info = {
    "name": "Render and shutdown pc",
    "author": "Jacob Samorowski email:jacob35422@gmail.com",
    "version": (0, 0, 1),
    "blender": (2, 65, 0),
    "location": "render > Render and shutdown",
    "description": "Once render is finished it will save the blend file and shutdown your pc",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Render",
}
from typing import Text
import random
import bpy
import os




class RenderShutdown(bpy.types.):
    bl_label = "Render and Shutdown"
    bl_idname = ""
    bl_space_type = 'VIEW_3D'
    bl_region_type = ''
    bl_category = ''

    def draw(self, context):
        layout = self.layout

Once render is finahed:

#save file 

os.system("shutdown /s /t 1") 




addon_keymaps = []
classes = [RenderShutdown,

] 

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
