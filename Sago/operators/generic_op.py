import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty,
                       FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Operator)
from .. helpers.render_settings import render_functions


class VIEW3D_OT_SAGO_add_displacement(Operator):
    bl_idname = "sago.add_displacement"
    bl_label = "Displace"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    def execute(self, context):
        obj = bpy.context.active_object
        sago = bpy.context.scene.sago
        lev = sago.sub_amount
        angle = sago.deg
        strength = sago.strength
        mid_level = sago.mid_level
        subdiv_amount = sago.subdive_amount
        noise_scale = sago.tex_noise_scale
        noise_depth = sago.colu_noise_depth
        noise_nabla = sago.tex_noise_nabla

        # to create a modifer
        # obj.modifiers.new("Name of modifer e.g: sago displace", "Type of modifer e.g SUBSURF")
        bpy.ops.object.editmode_toggle()
        if sago.submesh == True:
            bpy.ops.mesh.subdivide(number_cuts=subdiv_amount)
        else:
            bpy.ops.mesh.subdivide(number_cuts=0)
        bpy.ops.object.editmode_toggle()

        # create subsurf modifer if use_sub is True
        if sago.use_sub == True:
            sub = obj.modifiers.new("Sago Subdiv", 'SUBSURF')
            if self.sub_type == 'op1':
                sub.subdivision_type = 'SIMPLE'
            if self.sub_type == 'op2':
                sub.subdivision_type = 'CATMULL_CLARK'
            sub.levels = lev
            sub.render_levels = lev

        # create texture
        if sago.texture_type == "1":
            # check if texture exists if not creates a new texture
            if bpy.data.textures.get("Sago Displace Texture") == None:
                bpy.data.textures.new("Sago Displace Texture", 'CLOUDS')
                new_tex = bpy.data.textures['Sago Displace Texture']
                new_tex.type = 'CLOUDS'
                new_tex.noise_depth = noise_depth
                new_tex.noise_scale = noise_scale
                new_tex.nabla = noise_nabla

        if sago.texture_type == "2":
            if bpy.data.textures.get("Sago Displace Texture") == None:
                bpy.data.textures.new("Sago Displace Texture", 'VORONOI')
                new_tex = bpy.data.textures['Sago Displace Texture']
                new_tex.type = 'VORONOI'
                new_tex.noise_intensity = self.vo_noise_intensity
                new_tex.noise_scale = noise_scale
                new_tex.nabla = noise_nabla

        # create a displace modifier
        dis = obj.modifiers.new("Sago Displace", 'DISPLACE')
        dis.texture = new_tex
        dis.strength = strength
        dis.mid_level = mid_level

        if sago.shade_smooth == True:
            bpy.ops.object.shade_smooth()

        if sago.smooth == True:
            mesh = obj.data
            mesh.use_auto_smooth = True
            mesh.auto_smooth_angle = angle

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        sago = bpy.context.scene.sago
        layout.use_property_split = False
        layout.use_property_decorate = True  # No animation.

        layout.separator(factor=0.1)
        col = layout.column(align=True)
        col.label(text="Displace strength and mid level")
        col.prop(sago, "strength", text="Displace strength")
        col.prop(sago, "mid_level", text="displace mid level")
        col.separator()
        col.label(text="Texture Settings:")
        col.prop(sago, "texture_type", text="Texture type")
        if sago.texture_type == "1":
            col.prop(sago, "tex_noise_scale")
            col.prop(sago, "colu_noise_depth")
            col.prop(sago, "tex_noise_nabla")
        if sago.texture_type == "2":
            col.prop(sago, "vo_noise_intensity")
            col.prop(sago, "tex_noise_scale")
            col.prop(sago, "tex_noise_nabla")

        flow = col.column_flow(columns=2, align=True)
        flow.prop(sago, "submesh")
        if sago.submesh == True:
            col.prop(sago, "subdive_amount",
                     text="Sudvide amount", icon="MESH_GRID")

        flow.prop(self, "use_sub")
        if sago.use_sub == True:
            col.prop(sago, "sub_type", text="Subsurf type")
            col.prop(sago, "sub_amount", text="Subsurf amount")
        col.separator()
        flow.prop(sago, "smooth", text="Use Auto smooth")
        flow.prop(sago, "shade_smooth")
        if sago.smooth == True:
            col.prop(sago, "deg", slider=True)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class VIEW3D_OT_SAGO_toggle_clear_view(Operator):
    bl_idname = "sago.toggle_clear_view"
    bl_label = "Toggle clear view"

    def execute(self, context):
        enabled = not bpy.context.space_data
        bpy.context.space_data.overlay.show_overlays = enabled
        bpy.context.space_data.show_gizmo = enabled


class VIEW3D_OT_SAGO_toggle_face_orientation(bpy.types.Operator):
    bl_idname = "sago.toggle_face_orientation"
    bl_label = "Face Orientation"
    bl_description = "Toggle face orientation"

    def execute(self, context):
        bpy.context.space_data.overlay.show_face_orientation = not bpy.context.space_data.overlay.show_face_orientation

        return {'FINISHED'}


classes = [
    VIEW3D_OT_SAGO_add_displacement,
    VIEW3D_OT_SAGO_toggle_clear_view,
    VIEW3D_OT_SAGO_toggle_face_orientation,
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
