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
    "description": "You can Render your animations and either close blender or shutdown your computer",
    "author": "Jacob Samorowksi" "Contact me: Jacob35422@gmail.com",
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "View 3D > Properties Panel",
    "warning" : "make sure you have saved all files before checking the shutdown box as you might lose some files, i take no responsibility responiblity for this",
    "doc_url": "https://github.com/Eirfire/Blender-addon/wiki",
    "tracker_url": "https://github.com/Eirfire/Blender-addon/issues",
    "support": "",
    "category": "Object",
    }


#blender modules 
import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (PropertyGroup)

#other moduals 
import os
import random 


#import from other files 
from . import Menus
from . import operators
from . import Panels




class MyProperties(PropertyGroup):

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







addon_keymaps = []
classes = (
MyProperties,

)


def register():

    from bpy.utils import register_class

    Menus.register()
    Panels.register()
    operators.register()




    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)



def unregister():
    
    from bpy.utils import unregister_class

    
    Menus.unregister()
    Panels.unregister()
    operators.unregister()


    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()

    

