import bpy





#get current cameras in the scene
def get_camera_list(scene, context):
    """Return a list of all cameras in the current scene."""
    items = []
    
    for obj in scene.objects:
        if obj.type == 'CAMERA':
            items.append((obj.name, obj.name, ""))
    
    return items

def camera_list_update(self, context):
    bpy.context.scene.camera = bpy.data.objects[bpy.context.scene.active_camera]


def camera_length_update(self, context):
    cam = bpy.context.scene.active_camera
    bpy.data.objects[cam].data.lens= self.camera_length

def clipping_distance_end_update(self, context):
    cam = bpy.context.scene.active_camera
    bpy.data.objects[cam].data.clip_end = self.clipping_distance_end

def clipping_distance_start_update(self, context):
    cam = bpy.context.scene.active_camera
    bpy.data.objects[cam].data.clip_start = self.clipping_distance_start





