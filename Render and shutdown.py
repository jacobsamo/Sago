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


class RenderAndShutdown(bpy.types.Operator):

    bl_idname = 'render.shutdown'
    bl_label = 'Render And shutdown'
     
    def execute(self, context):
        bpy.ops.render.render(animation=True)

class TOPBAR_PT_Render_shutdown(bpy.types.Panel):
    """
    adds a tab under render to render an aimtion and shutdown the computer once fi
    """
    bl_idname = "TOPBAR_PT_Render_shutdown"
    bl_region_type = 'HEADER'
    bl_space_type = 'TOPBAR'
    bl_label = "Render and shutdown"



 
def some_other_function(dummy):
    print("Render complete")
    bpy.ops.wm.save_mainfile()
    bpy.ops.wm.quit_blender() #instead of quitting blender shutdown computer: os.system("shutdown /s /t 1") 

    
            
bpy.app.handlers.render_complete.append(some_other_function)      


   

       


Once a render is finished

#save file 
bpy.ops.wm.save_mainfile()

#shutdown computer
os.system("shutdown /s /t 1") 

#close blender aplication
bpy.ops.wm.quit_blender()



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
