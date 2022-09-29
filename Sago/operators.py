import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Panel, Menu, Operator, PropertyGroup, AddonPreferences)
from . modules.render_settings import render_functions



class MESH_OT_MONKEY_grid(bpy.types.Operator):
    """The Tool Tip"""
    bl_idname = 'mesh.monkey_grid'
    bl_label = 'Monkey Grid'
    bl_options = {"REGISTER", "UNDO"}
    
    count_x: IntProperty(
        name="X", 
        description="Number of monkeys in the x-direction",
        default=3,
        min=0, soft_max=10,
    )
    count_y: IntProperty(
        name="Y", 
        description="Number of monkeys in the Y-direction",
        default=3,
        min=0, soft_max=10,
    )
    size: FloatProperty(
        name="Size",
        description="Size of each monkey",
        default=0.5,
        min=0, soft_max=1,
    )

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'VIEW_3D'
    

    def execute(self, context):
        for idx in range(self.count_x * self.count_y ):
            x= idx % self.count_x
            y= idx //self.count_x
            bpy.ops.mesh.primitive_monkey_add( 
            size=self.size,
            location=(x,y, 1))
    
            
        
        return {'FINISHED'}




class SAGO_OT_add_displace(Operator):
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
        

        #to create a modifer
        #obj.modifiers.new("Name of modifer e.g: sago displace", "Type of modifer e.g SUBSURF")
        bpy.ops.object.editmode_toggle()
        if sago.submesh == True:
            bpy.ops.mesh.subdivide(number_cuts=subdiv_amount)
        else:
            bpy.ops.mesh.subdivide(number_cuts=0)
        bpy.ops.object.editmode_toggle()

        #create subsurf modifer if use_sub is True
        if sago.use_sub == True:
            sub = obj.modifiers.new("Sago Subdiv", 'SUBSURF')
            if self.sub_type == 'op1':
                sub.subdivision_type = 'SIMPLE'
            if self.sub_type == 'op2':
                sub.subdivision_type = 'CATMULL_CLARK'
            sub.levels = lev
            sub.render_levels = lev

        #create texture
        if sago.texture_type == "1":
            #check if texture exists if not creates a new texture
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
        
    
            
        #create a displace modifier
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


        layout.separator(factor= 0.1)
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
            col.prop(sago, "subdive_amount", text="Sudvide amount", icon="MESH_GRID")
    

        
        flow.prop(self, "use_sub")
        if sago.use_sub == True:
            col.prop(sago, "sub_type", text="Subsurf type")
            col.prop(sago, "sub_amount", text="Subsurf amount") 
        col.separator()
        flow.prop(sago, "smooth", text="Use Auto smooth")
        flow.prop(sago, "shade_smooth")
        if sago.smooth == True:
            col.prop(sago, "deg", slider= True)
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    


class SAGO_OT_toggle_clear_view(Operator):
    bl_idname = "sago.toggle_clear_view"
    bl_label = "Toggle clear view"

    def execute(self, context):
        enabled = not bpy.context.space_data
        bpy.context.space_data.overlay.show_overlays = enabled 
        bpy.context.space_data.show_gizmo = enabled


class toggle_face_orientation(bpy.types.Operator):
    bl_idname = "sago.toggle_face_orientation"
    bl_label = "Face Orientation"
    bl_description = "Toggle face orientation"


    def execute(self, context):
        bpy.context.space_data.overlay.show_face_orientation = not bpy.context.space_data.overlay.show_face_orientation

        return {'FINISHED'}


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
            col.separator(factor= 0.2)
            col.prop(scene, 'save_path', text='dir')
            bpy.app.handlers.render_complete.append(render_functions().sago_save_image) 

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)



#==================================================================
#                           Camera 
#==================================================================

class camera_settings(Operator):
    bl_idname = "sago.camera_settings"
    bl_label = "Camera settings"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    preset_enum: EnumProperty(
        name= "",
        description= "Select things",
        items= [ 
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
        col.prop(self, 'preset_enum', text = 'Presets')
        col.separator()
        col.prop(scene, "camera", text = "Active Camera")
        col.separator()
        col.prop(sago, 'camera_length', text = 'Camera Length')
        col.separator()
        col.prop(rd, "resolution_x", text="Resolution X")
        col.prop(rd, "resolution_y", text="Y")
        col.separator()
        col.prop(sago, 'clipping_distance_start', text="Clip Start")
        col.prop(sago, 'clipping_distance_end', text="Clip End")
        
    def execute(self, context):

        #deselect everting than select the camera
        bpy.ops.object.select_all(action='DESELECT')
        sel_cam = bpy.context.scene.active_camera
        bpy.data.objects[sel_cam].select_set(True)
        #select the active camera in the outliner
        bpy.context.view_layer.objects.active = bpy.data.objects[sel_cam]   
        
        pre = self.preset_enum  
        if pre == 'op2':
            x   = 0
            while x == 0:
                bpy.context.scene.render.resolution_y = 1080 
                bpy.context.scene.render.resolution_x = 1920
                x += 1
        if pre == 'op3':
            x   = 0
            while x == 0:
                bpy.context.scene.render.resolution_x = 1080
                bpy.context.scene.render.resolution_y = 1920
                x += 1
        if pre == 'op4':
            x   = 0
            while x == 0:
                bpy.context.scene.render.resolution_x = 1080
                bpy.context.scene.render.resolution_y = 1080
                x += 1
        return {'FINISHED'}


classes = (
    MESH_OT_MONKEY_grid,
    SAGO_OT_add_displace,
    toggle_face_orientation,
    #camera operators
    DATA_SAGO_check_ImageSave,
    camera_settings,
)
def register():
    # Importing register class
    from bpy.utils import register_class

    # Registering main classes:
    for cls in classes:
        register_class(cls)

def unregister():
    # Importing unregister class
    from bpy.utils import unregister_class

    # Unregistering main classes:
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()