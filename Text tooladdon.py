bl_info = {
    "name": "Text tool addon",
    "author": "Jacob",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "3D Veiw > N Panel > My 1st addon",
    "description": "Adds monkeys in rows",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object",
}
import bpy



class TestPanel(bpy.types.Panel):
    bl_label = "Test Tool"
    bl_idname = "PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Texttool'

    def draw(self, context):
        layout = self.layout

        sub = row.row(align=True)
        row = layout.row()
        sub.prop(mesh, "primitive_cube_add", text="")


class MESH_OT_add_object(bpy.types.Operator):
    
addon_keymaps = []
classes = [TestPanel,
]  
################### Register and unregister  
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
    


    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    
if __name__ == '__main__':
    register()
