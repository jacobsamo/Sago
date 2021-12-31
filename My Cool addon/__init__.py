bl_info = {
    "name": "A mix on things",
    "author": "Jacob",
    "version": (0,0,1),
    "blender": (2, 9, 0),
    "location": "3D Veiw > N Panel > Mix, Pie menu hot key: mouse button 4",
    "description": "A mix of items",
    "warning": "when using the render and shutdown make sure that you have save everything on your computer before running i take no responeiblity for any lose of files ",
    "doc_url": "",
    "tracker_url": "",
    "category": "",


}


#blender modules 
import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (PropertyGroup)

#other moduals 
import os
import random 


#import from other files 
from . import Extra_render
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

    Extra_render.register()
    Menus.register()
    Panels.register()
    operators.register()




    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)



def unregister():
    
    from bpy.utils import unregister_class

    
    Extra_render.unregister()
    Menus.unregister()
    Panels.unregister()
    operators.unregister()


    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()

    

