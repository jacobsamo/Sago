bl_info = {
    "name": "Sago",
    "author": "Jacob",
    "version": (0,0,1),
    "blender": (2, 9, 0),
    "location": "3D Veiw > N Panel > Sago, Pie menu hot key: mouse button 4",
    "description": "A mix of items",
    "warning": "when using the render and shutdown make sure that you have save everything on your computer before running i take no responeiblity for any lose of files ",
    "doc_url": "",
    "tracker_url": "",
    "category": "",


}


#blender modules 
import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (PropertyGroup)

#other moduals 
import os
import random 





###########Panels################


class TestPanel(Panel):



    bl_label = "test Panel"
    bl_idname = "PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Mix'

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

class ExtraRender(Panel):
    bl_idname = "TestPanel"
    bl_label = "Extra render settings"
  


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.prop(mytool, "close_blender")
        row = layout.row()
        row.prop(mytool, "shutdown_computer")

        if (mytool.close_blender == True):
            bpy.app.handlers.render_complete.append(some_other_function)  
        
        if (mytool.shutdown_computer == True):
            bpy.app.handlers.render_complete.append(some_function)  

def some_other_function(dummy):
    print("Render complete")
    bpy.ops.wm.save_mainfile()
    bpy.ops.wm.quit_blender()


def some_function(dummy):
    print("Render complete")
    bpy.ops.wm.save_mainfile()
    time.sleep(2)
    os.system("shutdown /s /t 1")



##############operators############

class MESH_OT_MONKEY_grid(Operator):
    """The Tool Tip"""
    bl_idname = 'mesh.monkey_grid'
    bl_label = 'Monkey Grid'
    bl_options = {"REGISTER", "UNDO"}
    
    count_x: bpy.props.IntProperty(
        name="X", 
        description="Number of monkeys in the x-direction",
        default=3,
        min=0, soft_max=10,
    )
    count_y: bpy.props.IntProperty(
        name="Y", 
        description="Number of monkeys in the Y-direction",
        default=3,
        min=0, soft_max=10,
    )
    size: bpy.props.FloatProperty(
        name="Size",
        description="Size of each monkey",
        default=0.5,
        min=0, soft_max=1,
    )
    

    def execute(self, context):
        for idx in range(self.count_x * self.count_y ):
            x= idx % self.count_x
            y= idx //self.count_x
            bpy.ops.mesh.primitive_monkey_add( 
            size=self.size,
            location=(x,y, 1))
    
            
        
        return {'FINISHED'}





############pie menus################

class WM_OT_pie_menu(Menu):
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


############register and unregister#############

ddon_keymaps = []
classes = [MESH_OT_MONKEY_grid,
TestPanel,
WM_OT_pie_menu,
ExtraRender

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

    