import bpy

def add_lamp(scene, name, type, size, color, location, rotation):
    """Creates a lamp (lamp name, type, location, rotation) at given location on the scene"""
    # create lamp
    new_lamp = bpy.data.lamps.new(name, type)
    # size lamp
    new_lamp.size = size
    # color
    new_lamp.color = color
    # create blender object
    lamp_obj = bpy.data.objects.new(name, new_lamp)
    # set location and rotation
    lamp_obj.location = location
    lamp_obj.rotation_euler = rotation
    # link to the scene
    scene.objects.link(lamp_obj)
    return lamp_obj


def add_camera(scene, name, lens,  location, rotation):
    """Creates new came at given location on the scene"""
    new_camera = bpy.data.cameras.new(name)
    # camera lens(zoom)
    new_camera.lens = lens
    # create blender camera obj
    camera_obj = bpy.data.objects.new(name, new_camera)
    # add to the scene
    scene.objects.link(camera_obj)
    # set location and rotation camera
    camera_obj.location = location
    camera_obj.rotation_euler = rotation

    return camera_obj
