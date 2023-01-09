#
#               @@@@@@@@@@
#           @@@            @@@
#        @@@    @@@@@@@@@@    @@@
#       @@   @@@@@@@@@@@@@@@@   @@
#     @@   @@@@@@@@@@@@@@@@@@@@   @@
#     @   @@@@@@@@@@@@@@@@@@@@@@   @
#    @@  @@@@@@@@@@@@@@@@@@@@@@@@  @@
#    @@                            @@
#    @@                            @@
#    @@  @@@@@@@@@@@@@@@@@@@@@@@@  @@
#     @   @@@@@@@@@@@@@@@@@@@@@@   @
#     @@   @@@@@@@@@@@@@@@@@@@@   @@
#       @@   @@@@@@@@@@@@@@@@   @@
#        @@@    @@@@@@@@@@    @@@
#           @@@            @@@
#               @@@@@@@@@@
#
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

from math import radians
from . ui_menus import *
from . import modifiers
from . import operators
from . import ui_panels
from . import ui_menus
from . modules.camera_functions import *
import rna_keymap_ui
from bpy.types import (Panel, Menu, Operator, PropertyGroup, AddonPreferences)
from bpy.props import (StringProperty, BoolProperty, IntProperty,
                       FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
import bpy
bl_info = {
    "name": "Sago",
    "description": "Extra render settings and quick access tools",
    "author": "Jacob Samorowksi",
    "version": (0, 5, 0),
    "blender": (2, 83, 0),
    "location": "3d View > Tool shelf",
    "warning": "Make sure other files on computer are saved",
    "doc_url": "https://github.com/Eirfire/Blender-addon/wiki",
    "tracker_url": "https://github.com/Eirfire/Blender-addon/issues",
    "support": "COMMUNITY",
    "category": "Generic",
}


# ------------------------------------------------------------------------------------------
# Custom Properties
# ------------------------------------------------------------------------------------------
class SagoProperties(PropertyGroup):

    # extra Render settings
    after_render_options: EnumProperty(
        name="render options",
        description="Select things",
        items=[
            ('close_blender', "Close blender", "Saves scene and closes blender"),
            ('sleep_computer', "Sleep computer",
             "Saves scene and puts computer to sleep"),
            ('shutdown_computer', "Shutdown computer",
             "Saves scene and shuts down computer"),
        ]
    )
    after_render_options_bool: BoolProperty(
        name="Render options",
        description="turn on to use render options",
        default=False
    )
    renderOperators: BoolProperty(
        name="Render options",
        description="a tick to do something after render",
        default=False
    )

    save_image: BoolProperty(
        name="Save image",
        description="after render save an image",
        default=False
    )
    close_blender: BoolProperty(
        name="close blender",
        description="A bool property",
        default=False
    )

    shutdown_computer: BoolProperty(
        name="Shut down computer",
        description="A bool property",
        default=False
    )
    sleep_computer: BoolProperty(
        name="Shut down computer",
        description="A bool property",
        default=False
    )
    render_options: BoolProperty(
        name="render optionx",
        description="A bool property",
        default=False
    )

# Monkey grid properties
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
    # camera settings

    camera_length: FloatProperty(
        name="camera_length",
        description="change camera length(mm)",
        default=50,
        min=1, soft_max=5000,
        update=camera_length_update
    )

    clipping_distance_end: FloatProperty(
        name="clipping_distance",
        description="change clipping distance",
        default=100,
        min=1, soft_max=10000,
        update=clipping_distance_end_update
    )
    clipping_distance_start: FloatProperty(
        name="clipping_distance",
        description="change clipping distance",
        default=0.01,
        min=0.001, soft_max=10000,
        update=clipping_distance_start_update
    )

    texture_type: EnumProperty(
        name="",
        description="Select things",
        items=[
            ('1', "Clouds", "Clouds Texture"),
            ('2', "Vorinoi", "Clouds Texture")
        ]
    )
    smooth: BoolProperty(
        name="Smooth", description="Use auto smooth", default=False)
    shade_smooth: BoolProperty(
        name="Shade Smooth", description="Shade smooth", default=False)
    deg: FloatProperty(
        name="Angle",
        description="Auto smooth angle",
        default=radians(30),
        min=0,
        max=radians(180),
        step=10,
        precision=3,
        subtype="ANGLE"
    )
    sub_type: EnumProperty(
        name="",
        description="Selct things",
        items=[
            ('op1', "Simple", "Use simple subsurf type"),
            ('op2', "Catmull-Clark", "Use Catmull-Clark subsurf type"),
        ]
    )
    subdive_amount: IntProperty(
        name="subdive",
        description="Subdivide amount",
        default=1,
        min=0, soft_max=10
    )
    strength: FloatProperty(
        name="strength",
        description="displace strength",
        default=1,
        soft_min=0, max=100
    )
    mid_level: FloatProperty(
        name="mid level",
        description="displace mid level",
        default=0.5,
        min=0, max=1
    )
    vo_noise_intensity: FloatProperty(
        name="Noise Intensity",
        description="Texture intensity",
        default=1,
        min=0.01, max=10
    )
    tex_noise_scale: FloatProperty(
        name="Noise scale",
        description="Texture Scale",
        default=0.25,
        min=0, soft_max=2
    )
    colu_noise_depth: IntProperty(
        name="Noise Depth",
        description="Texture depth",
        default=2,
        min=0, soft_max=24
    )
    tex_noise_nabla: FloatProperty(
        name="Noise nabla",
        description="Texture nabla",
        default=0.03,
        min=0, max=0.1
    )
    use_sub: BoolProperty(
        name="SubSurf", description="Use Sub Surf", default=False)
    sub_amount: IntProperty(name="", description="", default=2, min=0, max=11)

    submesh: BoolProperty(
        name="Subdivide", description="Subdive Mesh", default=False)

# preference that go in the addon area in preferences for the addon


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

    # main drawing panel with the tabs
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

    # what is shown if the tab is set to general
    def draw_general(self, box):
        layout = self.layout
        wm = bpy.context.window_manager
        box = layout.box()
        row = box.row()
        col = row.column()

        box.label(text='version ' + str(bl_info["version"]))
        self._extracted_from_draw_info_9(
            box,
            'Panel- 3D view > toolshelf > sago',
            'Pie menu - hotkey mouse button 4',
            'hotkeys can be change in the hotkeys tab',
        )

    # what is shown if the tab is set to info
    def draw_info(self, box):
        layout = self.layout
        wm = bpy.context.window_manager
        box = layout.box()
        row = box.row()
        col = row.column()

        self._extracted_from_draw_info_9(
            box,
            'in the addon there are many different operators and menus:\n',
            'locations of items:',
            '1. Pie menu- Hotkey = Mouse button 4',
        )
        self._extracted_from__extracted_from_draw_info_9_11(
            box,
            '2. side panel - 3D view > toolshelf > sago',
            'IMPORTANT!!! This addon is still in early devolvement and there will be bugs so sorrybut please let me know if youand i try and fix them ASAP',
            'Thanks Jacob',
        )
        box.operator(
            "wm.url_open", text="Report Issues").url = "https://github.com/Eirfire/Sago-Extra-Render-Addon/issues"

    # what is shown if the tab is set to keymap
    def _extracted_from_draw_info_9(self, box, text, arg2, arg3):
        self._extracted_from__extracted_from_draw_info_9_11(
            box, text, arg2, arg3)

    def _extracted_from__extracted_from_draw_info_9_11(self, box, text, arg2, arg3):
        box.label(text=text)
        box.label(text=arg2)
        box.label(text=arg3)

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
        if kmi := get_hotkey_entry_item(
            km, 'wm.call_menu_pie', f'{str(pie_menu_name)}'
        ):
            col.context_pointer_set('keymap', km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        else:
            col.label(text='No hotkey found', icon='ERROR')
            col.operator('add_hotkey.sago', text='Add hotkey')


addon_keymaps = []
pie_menu_name = SAGO_MT_pie_menu.bl_idname


def get_hotkey_entry_item(km, kmi_name, kmi_value):
    return next(
        (
            km_item
            for i, km_item in enumerate(km.keymap_items)
            if km.keymap_items.keys()[i] == kmi_name
            and km.keymap_items[i].properties.name == kmi_value
        ),
        None,
    )


def add_hotkey():

    addon_prefs = bpy.context.preferences.addons[__name__].preferences

    if kc := bpy.context.window_manager.keyconfigs.addon:
        km = kc.keymaps.new(name='3D View Generic',
                            space_type='VIEW_3D', region_type='WINDOW')
        kmi = km.keymap_items.new('wm.call_menu_pie', type='BUTTON4MOUSE',
                                  value='PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = f'{str(pie_menu_name)}'
        kmi.active = True
        addon_keymaps.append((km, kmi))


def remove_hotkey():

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

# if get_hotkey_entry_item can't find a hotkey this will be called in the panel


class USERPREF_OT_change_hotkey(Operator):
    '''Add hotkey'''
    bl_idname = "add_hotkey.sago"
    bl_label = "Add Hotkey"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        add_hotkey()
        return {'FINISHED'}


# add all classes to be registered
classes = (
    # properties
    SagoProperties,
    sago_addon_properties,
    USERPREF_OT_change_hotkey,
    # menu
    SAGO_MT_pie_menu
)


def register():
    from bpy.utils import register_class
    # global properties
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

    for cls in classes:
        register_class(cls)

    ui_panels.register()
    operators.register()
    modifiers.register()

    add_hotkey()

    bpy.types.Scene.sago = PointerProperty(type=SagoProperties)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    ui_panels.unregister()
    operators.unregister()
    modifiers.unregister()

    remove_hotkey()
    del bpy.types.Scene.sago


if __name__ == "__main__":
    register()
