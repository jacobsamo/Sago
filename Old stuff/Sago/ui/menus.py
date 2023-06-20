import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty,
                       FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Panel, Menu, Operator, PropertyGroup, AddonPreferences)


class SAGO_MT_pie_menu(Menu):
    bl_label = "Sago"
    bl_idname = "SAGO_MT_pie_menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        mode = bpy.context.object.mode
        layout.use_property_split = False
        layout.use_property_decorate = False
        
        if mode == "EDIT":
            col = pie.column(align=True)
            col.scale_y = 1.2
            col.label(text="Mesh Operators", icon="MESH_GRID")
            col.operator("mesh.subdivide", icon="MESH_GRID")
            col.operator("mesh.quads_convert_to_tris", icon="IPO_LINEAR")
            col.operator("mesh.select_random", icon="MOD_ARRAY")

        if mode == "OBJECT":
            col = pie.column(align=True)
            col.scale_y = 1.2
            col.label(text="Displacement", icon="MOD_DISPLACE")
            col.scale_y = 1.2
            col.scale_x = 1.4
            col.operator("sago.add_displacement", icon="MOD_DISPLACE")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.separator(factor=1)
        col = row.column(align=True)
        col.label(text="Modifiers", icon='MODIFIER_ON')
        col.scale_y = 1.2
        row = col.row(align=True)
        row.operator("sago.modifier_displace",
                     text="Displace", icon="MOD_DISPLACE")
        row.operator("sago.modifier_subsurf",
                     text="Subsurf", icon="MOD_SUBSURF")
        row = col.row(align=True)
        row.operator("sago.modifier_array", text="Array", icon="MOD_ARRAY")
        row.operator("sago.modifier_wireframe",
                     text="Wireframe", icon="MOD_WIREFRAME")

        # cameras settings, monkey_grid, etc
        col = pie.column(align=True)
        col.scale_y = 1.2
        col.label(text="Objects", icon="META_CUBE")
        col.scale_x = 1.4
        col.operator("sago.camera_settings", icon="VIEW_CAMERA")
        col.operator("mesh.monkey_grid", icon="MONKEY")
        col.operator("sago.toggle_face_orientation",
                     text="toggle face orientation", icon="NORMALS_FACE")


classes = [
    SAGO_MT_pie_menu
]

def register():
    # register keymap for this pie menu
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', shift=True)
    kmi.properties.name = "SAGO_MT_pie_menu"


    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    # unregister keymap for this pie menu
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps['Object Mode']
    for kmi in km.keymap_items:
        if kmi.idname == 'wm.call_menu_pie':
            if kmi.properties.name == "SAGO_MT_pie_menu":
                km.keymap_items.remove(kmi)
                break
            
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


