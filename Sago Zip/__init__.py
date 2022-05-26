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
    "description": "Extra render settings and quick acces tool",
    "author": "Jacob Samorowksi",
    "version": (0, 0, 4),
    "blender": (2, 83, 0),
    "location": "3d View > Tool shelf",
    "warning": "Make sure other files on computer are saved",
    "doc_url": "https://github.com/Eirfire/Blender-addon/wiki",
    "tracker_url": "https://github.com/Eirfire/Blender-addon/issues",
    "support": "COMMUNITY",
    "category": "Generic",
}


#import blender python modules 
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
from . operators import(
    MESH_OT_MONKEY_grid,
    camera_settings,
    SAGO_OT_add_displace,
    sago_mod_subsurf,
    sago_mod_displace,
    sago_mod_array,
    sago_mod_wireframe,
    toggle_face_orientation,
)

from . ui_panels import(
    VEIW3D_PT_Main_Panel,
    VEIW3D_PT_ExtraRender,
    NODE_PT_customPanel,

)

from . ui_menus import(
    SAGO_MT_pie_menu,
    
)



#------------------------------------------------------------------------------------------     
                            #Custom Properties 
#------------------------------------------------------------------------------------------  
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
    

#prefence that go in the addon aera in prefences for the addon
class sago_addon_properties(AddonPreferences):
    bl_idname = __name__

    tabs: EnumProperty(
        name="Tabs",
        items=[
            ("GENERAL", "General", ""),
            ("INFO", "Info", ""),
            ("KEYMAP", "Keymap", ""),
        ],
        default="GENERAL",
    )

    #main drawing panel with the tabs
    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)
        row = column.row()
        row.prop(self, "tabs", expand=True)

        box = layout.box()

        if self.tabs == "GENERAL":
            self.draw_general(box)
        elif self.tabs == "INFO":
            self.draw_info(box)
        elif self.tabs == "KEYMAP":
            self.draw_keymap(box)
        
    #what is shown if the tab is set to general
    def draw_general(self, box):
        layout = self.layout
        wm = bpy.context.window_manager
        box = layout.box()
        row = box.row()
        col = row.column()

        box.label(text='version ' + str(bl_info["version"]))
        box.label(text='Panel- 3D view > toolshelf > sago')
        box.label(text='Pie menu - hotkey mouse button 4')
        box.label(text='hotkeys can be change in the hotkeys tab')

    #what is shown if the tab is set to info
    def draw_info(self, box):
        layout = self.layout
        wm = bpy.context.window_manager
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
        
        box.operator("wm.url_open", text="Resport Issues").url = "https://github.com/Eirfire/Sago-Extra-Render-Addon/issues"

    #what is shown if the tab is set to keymap
    def draw_keymap(self, box):
        layout = self.layout
        wm = bpy.context.window_manager
        box = layout.box()
        row = box.row()
        col = row.column()
		
        col.label(text='Pie menu hot key:')
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps['3D View Generic']
        kmi = get_hotkey_entry_item(km, 'wm.call_menu_pie', f'{str(pie_menu_name)}')
        if kmi:
            col.context_pointer_set('keymap', km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        else:
            col.label(text='No hotkey found', icon='ERROR')
            col.operator('add_hotkey.sago', text='Add hotkey')



        




#add hotkey/ hotkeys to blender   
addon_keymaps = []
pie_menu_name = SAGO_MT_pie_menu.bl_idname

#find the hotkey in blenders keymap
def get_hotkey_entry_item(km, kmi_name, kmi_value):

	for i, km_item in enumerate(km.keymap_items):
		if km.keymap_items.keys()[i] == kmi_name:
			if km.keymap_items[i].properties.name == kmi_value:
				return km_item
	return None

#adds the hotkey to blenders keymap
def add_hotkey():

	addon_prefs = bpy.context.preferences.addons[__name__].preferences

	kc = bpy.context.window_manager.keyconfigs.addon
	if kc:
		km = kc.keymaps.new(name='3D View Generic', space_type='VIEW_3D', region_type='WINDOW')
		kmi = km.keymap_items.new('wm.call_menu_pie', type='BUTTON4MOUSE', value='PRESS', ctrl=False, shift=False, alt=False)
		kmi.properties.name = f'{str(pie_menu_name)}'
		kmi.active = True
		addon_keymaps.append((km, kmi))

#removes the hotkey from blenders keymap
def remove_hotkey():

	for km, kmi in addon_keymaps:
		km.keymap_items.remove(kmi)

	addon_keymaps.clear()

#if get_hotkey_entry_item can't find a hotkey this will be called in the pannel
class USERPREF_OT_change_hotkey(Operator):
	'''Add hotkey'''
	bl_idname = "add_hotkey.sago"
	bl_label = "Add Hotkey"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, context):
		add_hotkey()
		return {'FINISHED'}
        





#add all classes to be registered
classes = (
    #panels
    VEIW3D_PT_Main_Panel,
    VEIW3D_PT_ExtraRender,
    NODE_PT_customPanel,
    #menus
    SAGO_MT_pie_menu,
    #properties
    SagoProperties,
    sago_addon_properties,
    USERPREF_OT_change_hotkey,
    #operators
    MESH_OT_MONKEY_grid,
    camera_settings,
    SAGO_OT_add_displace,
    sago_mod_subsurf,
    sago_mod_displace,
    sago_mod_array,
    sago_mod_wireframe,
    toggle_face_orientation,
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

    #add hotkey/ hotkeys
    add_hotkey()
    #register custom properties
    bpy.types.Scene.sago = PointerProperty(type=SagoProperties)
    


# Unregister
def unregister():
    #unregister classes
    for cls in classes:
        bpy.utils.unregister_class(cls)
    #unregister keymaps
    remove_hotkey()
    #unregister properties
    del bpy.types.Scene.sago

#makes the file an executable file and reduces errors in code
if __name__ == "__main__":
    register()