# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Sago",
    "description": "Extra render settings STILL IN EARLY STAGES OF DEVOLMENT",
    "author": "Jacob Samorowksi",
    "version": (0, 0, 3),
    "blender": (2, 83, 0),
    "location": "3d View > Tool shelf",
    "warning": "make sure that all your files are saved before clicking shutdown computer otherwise you will lose files i take no responsibility for the lose of files and make sure that the blend file is saved before rendering as it will not work",
    "doc_url": "https://github.com/Eirfire/Blender-addon/wiki",
    "tracker_url": "https://github.com/Eirfire/Blender-addon/issues",
    "support": "COMMUNITY",
    "category": "Generic"
}


#import blender python modules 
from cProfile import label
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

#import classes from files
from . hello_world import ( 
    hello_world,
) 
from . operators import(
    MESH_OT_MONKEY_grid,
    camera_settings,
    NODE_OT_customgroup,
    SAGO_OT_add_displace,
)

from . ui_panels import(
    VEIW3D_PT_Main_Panel,
    VEIW3D_PT_ExtraRender,
    NODE_PT_customPanel,

)

from . ui_menus import(
    WM_MT_pie_menu,
)



#------------------------------------------------------------------------------------------     
                            #Custom Properties 
#------------------------------------------------------------------------------------------  
class sago_addon_properties(AddonPreferences):
    bl_idname = __name__



    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        box = layout.box()
        row = box.row()
        col = row.column()

        box.label(text='Test box')
        box.label(text='in the addon there are many different operators and menus:\n')
        box.label(text='locations of items:')
        box.label(text='1. Pie menu- Hotkey = Mouse button 4')
        box.label(text='2. side panel - 3D view > toolshelf > sago')
        
        box.label(text='IMPORTANT!!! This addon is still in early devolment and there will be bugs so sorrybut please let me know if youand i try and fix them ASAP') 

        box.label(text='Thank Jacob')
        
        col.operator("wm.url_open", text="Resport Issues").url = "https://github.com/Eirfire/Sago-Extra-Render-Addon/issues"
        

class SagoProperties(PropertyGroup):


#extra Render settings
    close_blender: BoolProperty(
        name="close blender",
        description="A bool property",
        default = False
        )
        
    shutdown_computer: BoolProperty(
        name="Shut down computer",
        description="A bool property",
        default = False
        )

#Monkey grid properties
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



addon_keymaps = []
classes = (
    #panels
    VEIW3D_PT_Main_Panel,
    VEIW3D_PT_ExtraRender,
    NODE_PT_customPanel,
    #menus
    WM_MT_pie_menu,
    #properties
    SagoProperties,
    sago_addon_properties,
    #operators
    MESH_OT_MONKEY_grid,
    NODE_OT_customgroup,
    camera_settings,
    SAGO_OT_add_displace,
)

# Register
def register():
    #save image parameters
    bpy.types.Scene.save_path = bpy.props.StringProperty(
        name = 'save location',
        default='C:/tmp',
        subtype='DIR_PATH',
    )
    bpy.types.Scene.save_name = bpy.props.StringProperty(
        name = 'Image name',
    )

    bpy.types.Scene.save_image = bpy.props.BoolProperty(
        name = 'save_image',
        default=False,
    )

    #register class
    for cls in classes:
        bpy.utils.register_class(cls)

    #add a keymap for pie menu
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("wm.call_menu_pie", type='BUTTON4MOUSE', value='PRESS')
        kmi.properties.name = "WM_MT_pie_menu"
        addon_keymaps.append((km,kmi))
    #register custom properties
    bpy.types.Scene.sago = PointerProperty(type=SagoProperties)
    


# Unregister
def unregister():
    #unregister classes
    for cls in classes:
        bpy.utils.unregister_class(cls)
    #unregister keymaps
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    #unregister properties
    del bpy.types.Scene.sago

if __name__ == "__main__":
    register()