#import blender python modules 
import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Panel, Menu, Operator, PropertyGroup,)
#import other python modules 
import os
import time
import random




class TestPanel(Panel):
    bl_idname = "OBJECT_PT_SaMix"
    bl_label = "A Mix Of Random Things"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sago"

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
    bl_idname = "OBJECT_PT_Sarender"
    bl_label = "Extra Render Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sago"


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        row = layout.row()
        row.label(text="Things that can happen after a render")
        row = layout.row()
        row.prop(mytool, "close_blender", text="Close blender")
        row = layout.row()
        row.prop(mytool, "shutdown_computer", text="Shutdown computer")

        


        if (mytool.close_blender == True):
            bpy.app.handlers.render_complete.append(some_other_function)  
        
        if (mytool.shutdown_computer == True):
            bpy.app.handlers.render_complete.append(some_function)  


def some_other_function(dummy):
    print("Render complete")
    bpy.ops.wm.save_mainfile()
    time.sleep(2)
    bpy.ops.wm.quit_blender()


def some_function(dummy):
    print("Render complete")
    bpy.ops.wm.save_mainfile()
    time.sleep(2)
    os.system("shutdown /s /t 1")

classes = [TestPanel, ExtraRender]  
  
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)