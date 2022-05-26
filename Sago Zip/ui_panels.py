#import blender python modules 
import bpy
from . import bl_info
import bmesh
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Panel, Menu, Operator, PropertyGroup, AddonPreferences)
import rna_keymap_ui
#import other python modules 
import os
import time
import math
from math import *



class VEIW3D_PT_Main_Panel(Panel):
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
        layout.operator('sago.add_displacement')

        layout.separator()
        row.operator("mesh.subdivide", icon="MESH_GRID")

class VEIW3D_PT_ExtraRender(Panel):
    bl_idname = "OBJECT_PT_Sarender"
    bl_label = "Extra render settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sago"


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        sago = scene.sago
        rd = context.scene.render
        sce = context.scene

        col = layout.column(align=True)
        #change camera resolution
        col.prop(rd, "resolution_x", text="Resolution X")
        col.prop(rd, "resolution_y", text="Resolution Y")
        col.operator("sago.camera_settings", text='camera settings')
        #add a render button
        props1 = col.operator("render.render", text="Render Image",icon='RENDER_STILL')
        props1.use_viewport = True
        props2 = col.operator(
            "render.render", text="Render Animation", icon='RENDER_ANIMATION')
        props2.animation = True
        props2.use_viewport = True
        #things to happen after a render such as shutdown or closing blender
        col = layout.column(align=True)
        col.label(text="Things that can happen after a render")
        if bpy.data.is_saved:
            col.label(text="File is saved")
            col.prop(sago, "close_blender", text="Close blender")
            col.prop(sago, "shutdown_computer", text="Shutdown computer")
        else:
            col.label(text="ERROR File needs to be saved", icon="ERROR")
            col.operator("wm.save_as_mainfile", text="Save As...")
            
        col = layout.column(align=True)
        col.label(text="if rendering a image")
        col.prop(sce, 'save_image', text='Save image')
        if bpy.context.scene.save_image == True:
            col.label(text="make sure you add file type e.g .png")
            col.prop(sce, 'save_name')
            col.separator(factor= 0.2)
            col.prop(sce, 'save_path')
            bpy.app.handlers.render_complete.append(sago_image_save) 
        
        if (sago.close_blender == True):
            bpy.app.handlers.render_complete.append(some_other_function)  
        
        if (sago.shutdown_computer == True):
            bpy.app.handlers.render_complete.append(some_function)  





      

def some_other_function(self, dummy):
    sago = bpy.context.scene.sago
    print("Render complete")
    sago.close_blender = False
    bpy.ops.wm.save_mainfile()
    time.sleep(2)
    bpy.ops.wm.quit_blender()    

def some_function(self, dummy):
    sago = bpy.context.scene.sago
    print("Render complete")
    sago.shutdown_computer = False
    bpy.ops.wm.save_mainfile()
    time.sleep(2)
    os.system("shutdown /s /t 1")

def sago_image_save(self, context):
    filepath = f'{str(bpy.context.scene.save_path)}{str(bpy.context.scene.save_name)}'
    img = bpy.data.images['Render Result']
    img.save_render(filepath)
    bpy.context.scene.save_image = False

#node editor panels
class NODE_PT_customPanel(Panel):
    bl_label = "Custom Geo Group"
    bl_idname = "NODE_PT_sago_geonode"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Sago"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text='There might be something here in the future')
