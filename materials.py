import bpy


def create_material(name, color, alpha):
    """Create material with color"""
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.alpha = alpha
    return material


def set_material(object, material):
    """Set material at object"""
    obj_data = object.data
    if obj_data.materials:
        obj_data.materials[0] = material
    else:
        obj_data.materials.append(material)

