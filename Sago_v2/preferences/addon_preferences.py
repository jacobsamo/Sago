import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty,
                       FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (AddonPreferences, Operator)
from ..helpers.camera_functions import *
from ..helpers.key_map import SAGO_key_map
from .. import bl_info
from ..ui.menus import SAGO_MT_pie_menu
from math import radians
import rna_keymap_ui


addon_keymaps = []
pie_menu_name = SAGO_MT_pie_menu.bl_idname


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
        if kmi := SAGO_key_map.get_hotkey(
            km, 'wm.call_menu_pie', f'{str(pie_menu_name)}'
        ):
            col.context_pointer_set('keymap', km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        else:
            col.label(text='No hotkey found', icon='ERROR')
            col.operator('add_hotkey.sago', text='Add hotkey')


class USERPREFS_OT_SAGO_add_hotkey(Operator):
    '''Add hotkey'''
    bl_idname = "add_hotkey.sago"
    bl_label = "Add Hotkey"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        SAGO_key_map.add_hotkey(addon_keymaps=addon_keymaps, property_name=pie_menu_name)
        return {'FINISHED'}