#import blender python modules 
from cgitb import text
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

class SAGO_MT_pie_menu(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Sago"
    #id label
    bl_idname = "SAGO_MT_pie_menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        mode = bpy.context.object.mode

        if mode == "EDIT":
        #only visable in edit mode only
            col = pie.column(align=True)
            col.scale_y = 1.2
            col.label(text = "Mesh Operators", icon = "MESH_GRID")
            col.operator("mesh.subdivide", icon="MESH_GRID")
            col.operator("mesh.quads_convert_to_tris", icon="IPO_LINEAR")
            col.operator("mesh.select_random", icon="MOD_ARRAY")

        if mode == "OBJECT":
        #Only visable in object mode only
            col = pie.column(align=True)
            col.scale_y = 1.2
            col.label(text = "Displacement", icon = "MOD_DISPLACE")
            col.scale_y = 1.2
            col.scale_x = 1.4
            col.operator("sago.add_displacement", icon="MOD_DISPLACE")
        #can be scene in any Mode
        #modifers
        col = pie.column(align=True)
        col.scale_y = 1.2
        col.label(text = "Modifers", icon = 'MODIFIER_ON')
        col.scale_y = 1.2
        col.scale_x = 1.4
        col.operator("sago.modifier_displace", text = "Displace modifier", icon="MOD_DISPLACE")
        col.operator("sago.modifier_subsurf",text="Subsurf modifier", icon="MOD_SUBSURF")
        col.operator("sago.modifier_array",text="Array modifier", icon="MOD_ARRAY")
        col.operator("sago.modifier_wireframe",text="Wireframe modifier", icon="MOD_WIREFRAME")
        
        #other operators like camera settings and monkey grid
        col = pie.column(align=True)
        col.scale_y = 1.2
        col.label(text = "Objects", icon = "META_CUBE")
        col.scale_y = 1.2
        col.scale_x = 1.4
        col.operator("sago.camera_settings", icon="VIEW_CAMERA")
        col.operator("mesh.monkey_grid", icon="MONKEY")
        col.operator("sago.toggle_face_orientation",text="toggle face orientation", icon="NORMALS_FACE")