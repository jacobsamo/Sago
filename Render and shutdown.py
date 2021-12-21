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
import random
import bpy
import os


  

def some_other_function(dummy):
    print("Render complete")
    bpy.ops.wm.save_mainfile()
    bpy.ops.wm.quit_blender() #instead of quitting blender shutdown computer: os.system("shutdown /s /t 1") 
    


# Will be executed once when the whole rendering process is completed
bpy.app.handlers.render_complete.append(some_other_function)


#--------------------------------------------------------
                #Operators
#--------------------------------------------------------
class Shutdown(bpy.types.Operator):
    """
    selects the surface objects will snap to
    """
    bl_idname = "Render.shutdown"
    bl_label = "Render and shut down"
    bl_description = ""




#--------------------------------------------------------
                #Panels
#--------------------------------------------------------

               
class TestPanel(bpy.types.Panel):

    bl_label = "Render and shutdown"
    bl_idname = "PT_Test"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Render extras'


    def draw(self, context):
        layout = self.layout
        view = context.space_data
        row = layout.row()

    

    
    




#--------------------------------------------------------
                #Menus
#--------------------------------------------------------










#--------------------------------------------------------
                #Properties 
#--------------------------------------------------------



class EirfireProperties(bpy.types.PropertyGroup):
    
    Render: bpy.types.BoolProperty(
        name="Make Collection Unique",
        description="Make the imported collection unique",
        default = False
        )
    



    
    
            
  
#--------------------------------------------------------
                #Notes
#--------------------------------------------------------
   

#Once a render is finished

#save file 
#bpy.ops.wm.save_mainfile()

#shutdown computer
#os.system("shutdown /s /t 1") 

#close blender aplication
#bpy.ops.wm.quit_blender()

#--------------------------------------------------------
                #Register and Unregister plus keymaps
#--------------------------------------------------------

addon_keymaps = []

classes = [MyPanel,


]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
   
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
