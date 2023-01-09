# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from .helpers.key_map import *
from .helpers.render_settings import *
from .helpers.camera_functions import *
from .preferences.preferences import SagoProperties
from .preferences.addon_preferences import USERPREFS_OT_SAGO_add_hotkey, sago_addon_properties
from .operators.generic_op import generic_op
from .operators.camera_op import camera_op
from .ui.panels import panels
from .ui.menus import menus
from math import radians
import rna_keymap_ui
from bpy.types import (Panel, Menu, Operator, PropertyGroup, AddonPreferences)
from bpy.props import (StringProperty, BoolProperty, IntProperty,
                       FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
import bpy
bl_info = {
    "name": "Sago_v2",
    "author": "Jacob",
    "description": "Extra render settings and quick access tools",
    "version": (0, 5, 0),
    "location": "3d View > Tool shelf",
    "warning": "Make sure other files on computer are saved",
    "doc_url": "https://github.com/Eirfire/Blender-addon/wiki",
    "tracker_url": "https://github.com/Eirfire/Blender-addon/issues",
    "support": "COMMUNITY",
    "category": "Generic"
}


# Import Modules

# preferences

# Helpers


SagoProperties()
sago_addon_properties()


classes = [
    USERPREFS_OT_SAGO_add_hotkey,
    sago_addon_properties,
    SagoProperties
]


def register():
    bpy.types.Scene.save_path = bpy.props.StringProperty(
        name='save location',
        default='/tmp/',
        subtype='DIR_PATH',
    )
    bpy.types.Scene.save_name = bpy.props.StringProperty(
        name='Image name',
    )

    bpy.types.Scene.save_image = bpy.props.BoolProperty(
        name='save_image',
        default=False,
    )
    bpy.types.Scene.active_camera = bpy.props.EnumProperty(
        name='Cameras',
        description='All cameras in current scene.',
        items=get_camera_list,
        update=camera_list_update,
    )

    SAGO_key_map.add_hotkey()

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.sago = PointerProperty(type=SagoProperties)


def unregister():

    SAGO_key_map.remove_hotkey()

    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.sago


if __name__ == "__main__":
    register()
