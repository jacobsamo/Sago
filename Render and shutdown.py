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
    
bpy.app.handlers.render_complete.append(some_other_function)     




# add your custom property to the Scene tpye
bpy.types.Scene.my_prop = BoolProperty(
    name="Prop name",
        description="Some tooltip",
        default = True)
        
# your custom panel
class MyPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "UI"        # where it will appear (render, world, material...)
    bl_label = 'My custom panel'
    
    @classmethod
    def poll(self, context):
        return True
        
    def draw(self, context):
        layout = self.layout
        sce = context.scene
        # draw the checkbox (implied from property type = bool)
        layout.prop(sce, "my_prop") 




class Shutdown(bpy.types.Panel):
    bl_label = "Shutdown Computer"
    bl_idname = "PT_Control"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Render and shutdown'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        # display the properties
        layout.prop(mytool, "my_bool", text="Bool Property")


        # check if bool property is enabled
        if (mytool.my_bool == True):
            print ("Property Enabled")
        

        else:
            print ("Property Disabled")



    def draw(self, context):


        layout = self.layout
        layout.use_property_split = True

        row = layout.row()
        row.operator("render.shutdown", icon="CAMERA_DATA")

        
class MySettings(PropertyGroup):

    my_bool: BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )
    


 


    
            
 




       


#Once a render is finished

#save file 
#bpy.ops.wm.save_mainfile()

#shutdown computer
#os.system("shutdown /s /t 1") 

#close blender aplication
#bpy.ops.wm.quit_blender()



addon_keymaps = []
classes = [Shutdown, 
RenderAndShutdown,
MySettings,

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
