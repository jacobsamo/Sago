import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty,
                       FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Operator)
from ..functions.render_settings import render_functions


class DATA_SAGO_check_ImageSave(bpy.types.Operator):
    """Check if saving render image"""
    bl_idname = "sago.check_render_settings"
    bl_label = "check render settings"
    bl_description = "Check what render settings are enabled"

    def execute(self, context):
        bpy.ops.render.render(use_viewport=True)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        sago = bpy.context.scene.sago
        scene = context.scene

        col = layout.column(align=True)
        col.label(text="Do you want to save rendered image")
        col.prop(sago, 'save_image', text='Save image')
        if sago.save_image == True:
            col.label(text="add filetype to name")
            col.prop(scene, 'save_name')
            col.separator(factor=0.2)
            col.prop(scene, 'save_path', text='dir')
            bpy.app.handlers.render_complete.append(
                render_functions().sago_save_image)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class VIEW3D_OT_SAGO_camera_settings(Operator):
    bl_idname = "sago.camera_settings"
    bl_label = "Camera settings"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    preset_enum: EnumProperty(
        name="",
        description="Select things",
        items=[
            ('op1', "Custom", "Custom Preset"),
            ('op2', "Horizontal", "Camera resolution: 1920x1080"),
            ('op3', "Vertical", "Camera resolution: 1080x1920"),
            ('op4', "Box", "Camera resolution: 1080x1080")
        ]
    )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        rd = context.scene.render
        scene = context.scene
        sago = scene.sago

        col = layout.column(align=True)
        col.prop(self, 'preset_enum', text='Presets')
        col.separator()
        col.prop(scene, "camera", text="Active Camera")
        col.separator()
        col.prop(sago, 'camera_length', text='Camera Length')
        col.separator()
        col.prop(rd, "resolution_x", text="Resolution X")
        col.prop(rd, "resolution_y", text="Y")
        col.separator()
        col.prop(sago, 'clipping_distance_start', text="Clip Start")
        col.prop(sago, 'clipping_distance_end', text="Clip End")

    def execute(self, context):

        # deselect everting than select the camera
        bpy.ops.object.select_all(action='DESELECT')
        sel_cam = bpy.context.scene.active_camera
        bpy.data.objects[sel_cam].select_set(True)
        # select the active camera in the outliner
        bpy.context.view_layer.objects.active = bpy.data.objects[sel_cam]

        pre = self.preset_enum
        if pre == 'op2':
            bpy.context.scene.render.resolution_y = 1080
            bpy.context.scene.render.resolution_x = 1920
            x = 0
            while x == 0:
                x += 1
        elif pre == 'op3':
            self.execute(1920)
        elif pre == 'op4':
            self.execute(1080)
        return {'FINISHED'}

    def execute(self, arg0):
        x = 0
        bpy.context.scene.render.resolution_x = 1080
        bpy.context.scene.render.resolution_y = arg0
        while x == 0:
            x += 1


classes = [
    DATA_SAGO_check_ImageSave,
    VIEW3D_OT_SAGO_camera_settings
]


def register():

    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
