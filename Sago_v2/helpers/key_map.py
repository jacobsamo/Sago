import bpy



class SAGO_key_map():
    """key map helpers"""

    def get_hotkey(self, km, kmi_name, kmi_value):
        """Get hotkey from blender keymap. to use `bpy.content.window_manger.keyconfigs.user."""
        return next(
            (
                km_item
                for i, km_item in enumerate(km.keymap_items)
                if km.keymap_items.keys()[i] == kmi_value
                and km.keymap_items[i].properties.name == kmi_value
            ),
            None,
        )

    def add_hotkey(self, property_name, addon_keymaps):
        # sourcery skip: use-named-expression
        prefs = bpy.context.preferences.addons[__name__].preferences
        kc = bpy.context.window_manager.keyconfigs.addon
        if kc:
            km = kc.keymaps.new(name='3D View Generic', space_type='VIEW_3D', region_type='WINDOW')
            kmi = km.keymap_items.new('wm.call_menu_pie', type='BUTTON4MOUSE', value='PRESS', ctrl=False, shift=False, alt=False)
            kmi.properties.name = f'{str(property_name)}'
            kmi.active = True
            addon_keymaps.append((km, kmi))

    def remove_hotkey(self, addon_keymaps):
        """Remove hotkey from keymaps"""
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

        addon_keymaps.clear()

