bl_info = {
    "name": "My Test Addon",
    "author": "Jacob",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "3D Veiw > N Panel > My 1st addon",
    "description": "Adds monkeys in rows",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object",
}
from typing import Text
import random
import bpy



###################### Operators ###########################
class MESH_OT_MONKEY_grid(bpy.types.Operator):
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
    




        

    

############## Panels and Pie Menus ########################
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
        row = layout.row()
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

            






        

       
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        #pie.operator_enum("mesh.select_mode", "type")
addon_keymaps = []
classes = [MESH_OT_MONKEY_grid,
TestPanel,
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

    

    

    
   


    
if __name__ == '__main__':
    register()

    

    

"""class VIEW3D_PT_monkey_grid(bpy.types.Panel):
    bl_space_type = 'VIEW3D'
    bl_region_type = 'UI'
    bl_category = "Monkeys"
    bl_label = "Grid"

    def draw(self, context):
        self.layout.operator('mesh.monkey_grid', text= "default grid", icon="MONKEY")"""
      
      
      
      
      
      
        


    
