import bpy
from bpy.props import (StringProperty, BoolProperty, IntProperty,
                       FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty,)
from bpy.types import (PropertyGroup)
from ..functions.camera_functions import *
from math import radians


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
