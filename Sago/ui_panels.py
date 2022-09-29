import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Panel, Menu, Operator, PropertyGroup, AddonPreferences)
from . modules.render_settings import render_functions
render = render_functions()

class VIEW3D_PT_SAGO_render_settings(Panel):
    bl_idname = "VIEW3D_PT_SAGO_render_settings"
    bl_label = "Render settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sago"
    bl_order = 1
    
    def draw_header(self, context):
        layout = self.layout
        scene = context.scene
        sago = scene.sago
        self.layout.prop(sago, 'renderOperators', text = "")


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        sago = scene.sago
        rd = context.scene.render
        sce = bpy.ops.marker
        layout.active = sago.renderOperators

        col = layout.column(align=True)
        row = col.row()
        #add a render button
        col.operator('sago.check_render_settings', text="Render Image",icon='RENDER_STILL')
        props2 = col.operator(
            "render.render", text="Render Animation", icon='RENDER_ANIMATION')
        props2.animation = True
        props2.use_viewport = True
        #things to happen after a render such as shutdown or closing blender
        col = layout.column(align=True)
    
        if bpy.data.is_saved:
            col.label(text="File is saved")
            row = layout.row()
            row.prop(sago, 'after_render_options_bool', text='')
            row.active = sago.after_render_options_bool
            row.prop(sago, 'after_render_options', text='')
             
        else:
            col.label(text="ERROR save file", icon="ERROR")
            col.operator("wm.save_as_mainfile", text="Save File")
            
        col = layout.column(align=True)
        col.prop(sago, 'save_image', text='Save image')
        if sago.save_image:
            col.label(text="add filetype to name")
            col.prop(scene, 'save_name')
            col.separator(factor= 0.2)
            col.prop(scene, 'save_path', text='dir')
            bpy.app.handlers.render_complete.append(render.sago_save_image) 
        
        if sago.after_render_options_bool:
            
            if (sago.after_render_options == "sleep_computer"):
                bpy.app.handlers.render_complete.append(render.sleep_computer) 
            elif (sago.after_render_options == "shutdown_computer"):
                bpy.app.handlers.render_complete.append(render.shutdown_computer)   
            elif (sago.after_render_options == 'close_blender'):
                bpy.app.handlers.render_complete.append(render.close_blender) 
            else:
                return ''
           
                
                


class VEIW3D_PT_SAGO_extra_tools(Panel):
    bl_idname = "OBJECT_PT_extra_tools"
    bl_label = "Extra operators"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sago"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 10

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("mesh.monkey_grid", icon="MONKEY")
        layout.operator('sago.add_displacement', text="Displace", icon="MOD_DISPLACE")
    
#==================================================================
#                        Camera panels
#==================================================================


class VEIW3D_PT_SAGO_camera_settings(Panel):
    bl_idname = "SAGO_PT_camera_settings"
    bl_label = "Camera settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sago"
    bl_order = 5
    

    def draw_header(self, context):
        self.layout.label(text = "", icon = "VIEW_CAMERA")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        cam = bpy.context.scene.active_camera
        dof = bpy.data.objects[cam].data.dof

        rd = context.scene.render
        scene = context.scene
        sago = scene.sago

        col = layout.column(align=True)
        row = col.row(align = True)
        col.operator('view3d.camera_to_view', text="camera to view", icon='CAMERA_STEREO')
        col.separator()
        col.operator('view3d.camera_to_view_selected', text="capture everything", icon='VIEW_CAMERA')
        col.separator()
        col.prop(context.scene, 'active_camera', text='', icon='CAMERA_DATA')
        col.separator()
        col.prop(sago, 'camera_length', text = 'Focal length')
        col.separator()
        col.prop(rd, "resolution_x", text="Resolution X")
        col.prop(rd, "resolution_y", text="Y")
        col.separator()
        col.prop(sago, 'clipping_distance_start', text="Clip Start")
        col.prop(sago, 'clipping_distance_end', text="Clip End")
        col.separator()
        col = layout.row().box()
        col.prop(dof, 'use_dof', text='Depth of field')
        

class DATA_SAGO_camera_dof_aperture(Panel):
    bl_label = "Aperture"
    bl_idname = "SAGO_PT_camera_controls"
    bl_parent_id = VEIW3D_PT_SAGO_camera_settings.bl_idname
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sago"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        cam = bpy.context.scene.active_camera
        dof = bpy.data.objects[cam].data.dof
        layout.active = dof.use_dof

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        col = layout.column()
        col.prop(dof, "focus_object", text="Focus on Object")
        sub = col.column()
        sub.active = (dof.focus_object is None)
        sub.prop(dof, "focus_distance", text="Focus Distance")

        col = flow.column()
        col.prop(dof, "aperture_fstop")

        col = flow.column()
        col.prop(dof, "aperture_blades")
        col.prop(dof, "aperture_rotation")
        col.prop(dof, "aperture_ratio")







#node editor panels
class NODE_PT_customPanel(Panel):
    bl_label = "Custom Geo Group"
    bl_idname = "NODE_PT_sago_geonode"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Sago"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text='There might be something here in the future')


classes = (
    VIEW3D_PT_SAGO_render_settings,
    VEIW3D_PT_SAGO_extra_tools,
    NODE_PT_customPanel,
    #camera panels
    VEIW3D_PT_SAGO_camera_settings,
    DATA_SAGO_camera_dof_aperture,
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