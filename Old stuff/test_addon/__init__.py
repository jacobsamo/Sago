bl_info = {
    "name": "test_addon",
    "blender": (2, 93, 0),
    "category": "Object",
}

import importlib
from .  ui import operators
from .  ui import panels
import bpy

files = [
    operators,
    panels
]

def register():
    for file in files:
        importlib.reload(file)
        file.register()

def unregister():
    for file in files:
        file.unregister()

if __name__ == "__main__":
    register()


