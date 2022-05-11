#import blender python modules 
from unicodedata import name
import bpy
import bmesh
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Panel, Menu, Operator, PropertyGroup, AddonPreferences)
import rna_keymap_ui
#import other python modules 
import os
import time
import math
from math import *


class WM_MT_pie_menu(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Select Mode"
    bl_idname = "WM_MT_pie_menu"
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        mode = bpy.context.object.mode

        if mode == "EDIT":
        #Edit mode only
            col = pie.column(align=True)
            col.scale_y = 1.2
            col.label(text = "Mesh Operators", icon = "MESH_GRID")
            col.operator("mesh.subdivide", icon="MESH_GRID")
            col.operator("mesh.quads_convert_to_tris", icon="IPO_LINEAR")
            col.operator("mesh.select_random", icon="MOD_ARRAY")

        if mode == "OBJECT":
            col = pie.column(align=True)
            col.scale_y = 1.2
            col.label(text = "Displacement", icon = "MOD_DISPLACE")
            col.scale_y = 1.2
            col.scale_x = 1.4
            col.operator("sago.add_displacement", icon="MOD_DISPLACE")
        #Any Mode
        col = pie.column(align=True)
        col.scale_y = 1.2
        col.label(text = "Object", icon = "META_CUBE")
        col.scale_y = 1.2
        col.scale_x = 1.4
        col.operator("sago.camera_settings", icon="VIEW_CAMERA")
        col.operator("mesh.monkey_grid", icon="MONKEY")