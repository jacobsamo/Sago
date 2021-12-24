#blender modules 
import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (PropertyGroup)

#other moduals 
import os
import random 



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
    

addon_keymaps = []
classes = [MESH_OT_MONKEY_grid,]  
  
def register():
    for cls in classes:
        bpy.utils.register_class(cls)



    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

   

    
if __name__ == '__main__':
    register()