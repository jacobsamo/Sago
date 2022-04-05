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

bl_info = {
    "name": "Sago",
    "description": "Extra render settings STILL IN EARLY STAGES OF DEVOLMENT",
    "author": "Jacob Samorowksi",
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "View 3D > Properties Panel >Sago",
    "warning": "make sure that all your files are saved before clicking shutdown computer otherwise you will lose files i take no responsibility for the lose of files and make sure that the blend file is saved before rendering as it will not work",
    "doc_url": "https://github.com/Eirfire/Blender-addon/wiki",
    "tracker_url": "https://github.com/Eirfire/Blender-addon/issues",
    "support": "COMMUNITY",
    "category": "Generic",
    }


#import blender python modules 
from ast import Pass
from typing import Text
import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (Panel, Menu, Operator, PropertyGroup,)
#import other python modules 
import os
import time
import random







#------------------------------------------------------------------------------------------     
                            #Panels
#------------------------------------------------------------------------------------------  


class VEIW3D_PT_Main_Panel(Panel):
    bl_idname = "OBJECT_PT_SaMix"
    bl_label = "A Mix Of Random Things"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sago"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Add object", icon= "CUBE")
        row = layout.row()
        row.operator("mesh.primitive_cube_add", icon="CUBE")
        row = layout.row()
        row.operator("mesh.primitive_uv_sphere_add", icon="MESH_UVSPHERE")
        row = layout.row()
        row.operator("mesh.monkey_grid", icon="MONKEY")

        layout.separator()
        row.operator("mesh.subdivide", icon="MESH_GRID")


class VEIW3D_PT_ExtraRender(Panel):
    bl_idname = "OBJECT_PT_Sarender"
    bl_label = "Extra Render Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sago"


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        sago = scene.sago
        rd = context.scene.render

        col = layout.column(align=True)
        col.prop(rd, "resolution_x", text="Resolution X")
        col.prop(rd, "resolution_y", text="Resolution Y")
        col.label(text="Things that can happen after a render")
        col.prop(sago, "close_blender", text="Close blender")
        col.prop(sago, "shutdown_computer", text="Shutdown computer")

        if (sago.close_blender == True):
            bpy.app.handlers.render_complete.append(some_other_function)  
        
        if (sago.shutdown_computer == True):
            bpy.app.handlers.render_complete.append(some_function)  



        
def some_other_function(dummy):
    print("Render complete")
    bpy.context.scene.my_tool.close_blender = False
    bpy.ops.wm.save_mainfile()
    time.sleep(2)
    bpy.ops.wm.quit_blender()    

def some_function(dummy):
    print("Render complete")
    bpy.context.scene.my_tool.shutdown_computer = False
    bpy.ops.wm.save_mainfile()
    time.sleep(2)
    os.system("shutdown /s /t 1")




class NODE_PT_customPanel(Panel):
    bl_label = "Custom Geo Group"
    bl_idname = "NODE_PT_sago_geonode"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Sago"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator("sago.geoScatter", text="Geo Scatter")


#------------------------------------------------------------------------------------------     
                            #Operators
#------------------------------------------------------------------------------------------  

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


class camera_settings(Operator):
    bl_idname = "sago.camera_settings"
    bl_label = "Camera settings"
    bl_options = {"REGISTER", "UNDO"}


    preset_enum: EnumProperty(
        name= "",
        description= "Selct things",
        items= [ 
            ('op1', "Custom", "Custom Preset"),
            ('op2', "Horizontal", "Camera resolution: 1920x1080"),
            ('op3', "Vertical", "Camera resolution: 1080x1920"),
            ('op4', "Box", "Camera resolution: 1080x1080")
        ]
    )
    camera_length: FloatProperty(
        name="camera_length",
        description="change camera length(mm)",
        default=50,
        min=1, soft_max=5000,
    )

    Depth_Of_Feild: BoolProperty(
        name="dof",
        description= "Use depth of feild",
        default=False
        )

    cliping_distance_end: FloatProperty(
        name="cliping_distance",
        description="change clipping distance",
        default= 100,
        min=1, soft_max = 10000
    )
    cliping_distance_start: FloatProperty(
        name="cliping_distance",
        description="change clipping distance",
        default= 0.01,
        min= 0.001, soft_max = 10000
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

        col = layout.column(align=True)
        col.prop(self, 'preset_enum', text = 'Presets')
        col.separator()
        col.prop(scene, "camera", text = "Active Camera")
        col.separator()
        col.prop(self, 'camera_length', text = 'Camera Length')
        col.separator()
        col.prop(rd, "resolution_x", text="Resolution X")
        col.prop(rd, "resolution_y", text="Y")
        col.separator()
        col.prop(self, 'cliping_distance_start', text="Clip Start")
        col.prop(self, 'cliping_distance_end', text="Clip End")
        
        


    def execute(self, context):

        C = bpy.context
        C.active_object.select_set(False)
        C.scene.camera.select_set(True)
        pre = self.preset_enum
        cam = bpy.data.cameras[0]


        cam.lens = self.camera_length
        cam.clip_end = self.cliping_distance_end
        cam.clip_start = self.cliping_distance_start
        if pre == 'op1':
            self.report({'INFO'}, "Camera settings changed")
        if pre == 'op2':
            bpy.context.scene.render.resolution_x = 1920
            bpy.context.scene.render.resolution_y = 1080
            self.report({'INFO'}, "Camera res = 1920x1080")
        if pre == 'op3':
            bpy.context.scene.render.resolution_x = 1080
            bpy.context.scene.render.resolution_y = 1920
            self.report({'INFO'}, "Camera res = 1080x1920")
        if pre == 'op4':
            bpy.context.scene.render.resolution_x = 1080
            bpy.context.scene.render.resolution_y = 1080
            self.report({'INFO'}, "Camera res = 1080x1080")
        
        return {'FINISHED'}


class NODE_OT_customgroup(Operator):
    """Tooltip"""
    bl_idname = "node.simple_operator"
    bl_label = "sago.geoScatter"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'


    def execute(self, context):

        
        mod = bpy.context.active_object

        for mod in mod.modifiers:
            if mod.type == 'NODES':
                Scatter(1)
            
            else:
                self.report({'INFO'}, "Object needs geometry nodes")

        

        
            
        return {"FINISHED"}


    


#------------------------------------------------------------------------------------------     
                            #Menus
#------------------------------------------------------------------------------------------   

class WM_MT_pie_menu(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Select Mode"
    bl_idname = "WM_MT_pie_menu"
    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        mode = bpy.context.active_object.mode

        if mode == "EDIT":
        #Edit mode only
            pie.operator("mesh.subdivide", icon="MESH_GRID")
            pie.operator("mesh.quads_convert_to_tris", icon="IPO_LINEAR")
            pie.operator("mesh.select_random", icon="MOD_ARRAY")


        #Any Mode
        pie.operator("sago.camera_settings", icon="VIEW_CAMERA")
        pie.operator("mesh.monkey_grid", icon="MONKEY")




#------------------------------------------------------------------------------------------     
                            #Custom Properties 
#------------------------------------------------------------------------------------------     
def Scattername(dummy):
    bpy.ops.node.add_node(type="GeometryNodeGroup", use_transform=True, 
    settings=[{"name":"node_tree", "value":"bpy.data.node_groups['Scatter']"}])


def Scatter(dummy):
    group = bpy.data.node_groups.new(type="GeometryNodeTree", name="Scatter")

    #add input sockets
    group.inputs.new('NodeSocketGeometry', 'Geometry')
    group.inputs.new('NodeSocketFloat', 'Distance Min')
    group.inputs.new('NodeSocketFloat', 'Denisty Max')
    group.inputs.new('NodeSocketFloat', 'Denisty Factor')
    group.inputs.new('NodeSocketInt', 'Seed')
    group.inputs.new('NodeSocketGeometry', 'Object')
    group.inputs.new('NodeSocketBool', 'Pick Instance')
    group.inputs.new('NodeSocketVector', 'Rotation')
    group.inputs.new('NodeSocketVector', 'Scale')

    #Add input 1
    input_node = group.nodes.new("NodeGroupInput")
    input_node.location = (-700, 0)

    #Add Input 2
    input_node2 = group.nodes.new("NodeGroupInput")
    input_node2.location = (-100, -600)


    #add a group input
    group.outputs.new("NodeSocketGeometry", "Geometry")
    output_node = group.nodes.new("NodeGroupOutput")
    output_node.location = (700, 0)

    #Add Distrubitue Points On Faces Node
    dis_node = group.nodes.new('GeometryNodeDistributePointsOnFaces')
    dis_node.location = (-100, -100)
    dis_node.distribute_method = 'POISSON'

    #Add instance on points node
    inst_node = group.nodes.new('GeometryNodeInstanceOnPoints')
    inst_node.location = (200, -100)


    link = group.links.new

    #link nodes that are inside
    link(dis_node.outputs["Points"], inst_node.inputs["Points"])
    #link(dis_node.outputs["Normal"], inst_node.inputs["Rotation"])


    #link inputs 1
    link(input_node.outputs['Geometry'], dis_node.inputs[0])
    link(input_node.outputs['Distance Min'], dis_node.inputs[2])
    link(input_node.outputs['Denisty Max'], dis_node.inputs[3])
    link(input_node.outputs['Denisty Factor'], dis_node.inputs[4])
    link(input_node.outputs['Seed'], dis_node.inputs[5])


    #link inputs 2
    link(input_node2.outputs['Object'], inst_node.inputs['Instance'])
    link(input_node2.outputs['Pick Instance'], inst_node.inputs['Pick Instance'])
    link(input_node2.outputs['Rotation'], inst_node.inputs["Rotation"])
    link(input_node2.outputs['Scale'], inst_node.inputs['Scale'])


    #output
    link(inst_node.outputs['Instances'], output_node.inputs['Geometry'])

    bpy.ops.node.add_node(type="GeometryNodeGroup", use_transform=True, 
    settings=[{"name":"node_tree", "value":"bpy.data.node_groups['Scatter']"}])



#------------------------------------------------------------------------------------------     
                            #Custom Properties 
#------------------------------------------------------------------------------------------  


class SagoProperties(PropertyGroup):


#extra Render settings
    close_blender: BoolProperty(
        name="close blender",
        description="A bool property",
        default = False
        )
        
    shutdown_computer: BoolProperty(
        name="Shut down computer",
        description="A bool property",
        default = False
        )

    safilepath: StringProperty(
        name='Image filepath',
        subtype='DIR_PATH',

    )


#Monkey grid properties
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

#pie menu 




#------------------------------------------------------------------------------------------     
                            #Registeration
#------------------------------------------------------------------------------------------  


addon_keymaps = []
classes = (
#panels
VEIW3D_PT_Main_Panel,
VEIW3D_PT_ExtraRender,
#menus
WM_MT_pie_menu,
#properties
SagoProperties,
#operators
MESH_OT_MONKEY_grid,
camera_settings,
NODE_OT_customgroup,
)

# Register
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("wm.call_menu_pie", type='BUTTON4MOUSE', value='PRESS')
        kmi.properties.name = "WM_MT_pie_menu"
        addon_keymaps.append((km,kmi))

    bpy.types.Scene.sago = PointerProperty(type=SagoProperties)
    


# Unregister
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    del bpy.types.Scene.sago

if __name__ == "__main__":
    register()
