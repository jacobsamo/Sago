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
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "View 3D > Properties Panel >Sago",
    "warning": "make sure that all your files are saved before clicking shutdown computer otherwise you will lose files i take no responsibility for the lose of files and make sure that the blend file is saved before rendering as it will not work",
    "doc_url": "https://github.com/Eirfire/Blender-addon/wiki",
    "tracker_url": "https://github.com/Eirfire/Blender-addon/issues",
    "support": "COMMUNITY",
    "category": "Object",
    }


#import blender python modules 
from typing import Text
import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Panel, Menu, Operator, PropertyGroup,)
#import other python modules 
import os
import time
import random







#------------------------------------------------------------------------------------------     
                            #Panels
#------------------------------------------------------------------------------------------  


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





#------------------------------------------------------------------------------------------     
                            #Operators
#------------------------------------------------------------------------------------------  



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




#------------------------------------------------------------------------------------------     
                            #Menus
#------------------------------------------------------------------------------------------   

class WM_OT_pie_menu(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Select Mode"
    bl_idname = "WM_OT_pie_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        pie.operator("mesh.subdivide", icon="MESH_GRID")
        pie.operator("bpy.context.object.data.use_auto_smooth = True", icon="MONKEY")



#------------------------------------------------------------------------------------------     
                            #Custom Properties 
#------------------------------------------------------------------------------------------     


class SagoProperties(PropertyGroup):

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



#------------------------------------------------------------------------------------------     
                            #Registeration
#------------------------------------------------------------------------------------------  


addon_keymaps = []
classes = (TestPanel,
ExtraRender,
MESH_OT_MONKEY_grid,
WM_OT_pie_menu,
SagoProperties,

)

# Register
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

    bpy.types.Scene.my_tool = PointerProperty(type=SagoProperties)
    


# Unregister
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
