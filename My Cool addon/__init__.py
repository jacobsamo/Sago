bl_info = {
    "name": "A mix on things",
    "author": "Jacob",
    "version": (0,0,1),
    "blender": (2, 65, 0),
    "location": "3D Veiw > N Panel > My 1st addon or render and shutdown, Pie menu hot key: mouse button 4",
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
from . import Operators  
from . import Shutdown
from . import Menus




class MyProperties(PropertyGroup):

    my_bool: BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )







addon_keymaps = []
classes = (
MyProperties,

)


def register():

    from bpy.utils import register_class


    Operators.register()
    Shutdown.register()
    Menus.register()




    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)



def unregister():
    
    from bpy.utils import unregister_class

    Operators.unregister()
    Shutdown.unregister()
    Menus.register()


    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
            kmi = km.keymap_items.new("wm.call_menu_pie", type='BUTTON4MOUSE', value='PRESS')
            kmi.properties.name = "WM_OT_pie_menu"
            addon_keymaps.append((km,kmi))
            
        
    


    for cls in reversed(classes):
        unregister_class(cls)

    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()



    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()


