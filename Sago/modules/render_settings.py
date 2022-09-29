import bpy
import os 
import subprocess
from time import sleep
from sys import platform

"""quick reference to the third item when calling the functions 
is due to blender saying it 'takes 2 positional arguments but 3 were given'
not sure why but it works how it does. and as the saying goes if it work don't touch it"""


class render_functions:

    def close_blender(self, context, third):
        print("Render complete - close blender")
        bpy.ops.wm.save_mainfile()
        sleep(2)
        bpy.ops.wm.quit_blender() 

    
    def sleep_computer(self, context, third):
        print("Render complete - sleep computer")
        bpy.ops.wm.save_mainfile()
        sleep(2)
        if platform == 'darwin':
            os.system('pmset sleepnow')
            
        if platform == 'win32':
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        if platform == 'linux' or platform == 'linux2':
            os.system("systemctl suspend")
        bpy.context.scene.sago.after_render_options_bool = False

    def shutdown_computer(self, context, third):
        print("Render complete - shut down computer")
        bpy.ops.wm.save_mainfile()
        sleep(2)
        if platform == 'win32':
            os.system("shutdown /s /t 1")
        
        if platform == 'darwin':
            subprocess.call(['osascript', '-e', 'tell app "System Events" to shut down'])

        if platform == 'linux' or platform == 'linux2':
            command = 'shutdown -h now'
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        bpy.context.scene.sago.after_render_options_bool = False
        sleep(2)

    def sago_save_image():
        filepath = f'{str(bpy.context.scene.save_path)}{str(bpy.context.scene.save_name)}'
        img = bpy.data.images['Render Result']
        img.save_render(filepath)
        bpy.context.scene.sago.save_image = False
