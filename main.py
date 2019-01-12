import bpy
import os

from room_objects import *
from other_objects import *
from materials import *
import json
# blender scene
bpyscene = bpy.context.scene
bpyscene.render.engine = 'CYCLES'

# delete all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()


def render_rgb(scene, object_name, material_name):
    """Render object only RGB channels"""

    # use nodes
    bpy.context.scene.use_nodes = True

    nodes = scene.node_tree.nodes

    render_layers = nodes['Render Layers']
    composite = nodes["Composite"]

    # links nodes
    scene.node_tree.links.new(
        render_layers.outputs['Image'],
        composite.inputs['Image']
    )

    # file path for render
    scene.render.filepath = os.path.join(os.path.dirname(os.path.abspath((__file__))),
                                                object_name + '/' + object_name + '_' + material_name + '/' + 'RGB_TILE_1X1')
    # render to file
    bpy.ops.render.render(write_still=True)
    return material_name


def render_zdepth(scene, object_name):
    """Render object zdepth"""

    # use nodes
    bpy.context.scene.use_nodes = True

    nodes = scene.node_tree.nodes

    # normalize Z to 0..1 and invert colors
    normalize = nodes.new("CompositorNodeNormalize")
    invert = nodes.new("CompositorNodeInvert")

    # links
    render_layers = nodes['Render Layers']
    composite = nodes["Composite"]

    scene.node_tree.links.new(
        render_layers.outputs['Depth'],
        normalize.inputs['Value']
    )

    scene.node_tree.links.new(
        normalize.outputs['Value'],
        invert.inputs['Color']
    )

    scene.node_tree.links.new(
        invert.outputs['Color'],
        composite.inputs['Image']
    )

    # file path for render
    scene.render.filepath = os.path.join(os.path.dirname(os.path.abspath((__file__))), object_name + '/ZDEPTH_TILE_1X1' )
    # render to file
    bpy.ops.render.render(write_still= True)


def render_alpha(scene, object_name):
    """Render object alpha"""
    # use nodes
    bpy.context.scene.use_nodes = True
    nodes = scene.node_tree.nodes

    render_layers = nodes['Render Layers']
    composite = nodes["Composite"]

    # links alpha to composite image
    scene.node_tree.links.new(
        render_layers.outputs['Alpha'],
        composite.inputs['Image']
    )

    # file path for render
    scene.render.filepath = os.path.join(os.path.dirname(os.path.abspath((__file__))), object_name + '/ALPHA_TILE_1X1')
    # render to file
    bpy.ops.render.render(write_still= True)


def render(scene, object, materials):
    """Render rgb, alpha and zdepth objects with different materials and return variants"""
    variants = []
    for i, material in enumerate(materials):
        set_material(object, material)
        name_v = render_rgb(scene, object.name, material.name)
        variants.append(dict(id=i, name=object.name + '_' + name_v))
    render_alpha(scene, object.name)
    render_zdepth(scene, object.name)

    return variants

# room dimensions
width = 4
length = 5
height = 2.5

# add lamps
add_lamp(bpyscene, 'LAMP1', 'AREA', color=(1, 1, 1), size=1.5, location=(0.01, width/2, height -1), rotation=(0,-1.43, 0))
add_lamp(bpyscene, 'LAMP2', 'AREA', color=(1, 1, 1), size=1.5, location=(length/2, width-0.2, height -1), rotation=(-1,-1.43, 0))

# cam
list_cameras = []
cam1 = add_camera(bpyscene, 'CAMERA1', 10, location=(0.2, 1.3, 1.6), rotation=(1.43, 0, -1.48))

list_cameras.append(cam1.name)
bpyscene.camera = bpyscene.objects[list_cameras[0]]

# materials
materials_list = []
materials_list.append(create_material('wild_grey', color=(0.174647, 0.212231, 0.234551), alpha=1 ))
materials_list.append(create_material('white', color=(1, 1, 1), alpha=1))
materials_list.append(create_material('brown', color=(0.235, 0.069, 0), alpha=1))
materials_list.append(create_material(('dark brwon'), color=(0.2, 0.1, 0), alpha=1))

# Render settings
bpyscene.render.image_settings.color_mode = 'RGB'
bpyscene.render.image_settings.file_format = 'TIFF'
bpyscene.cycles.samples = 10
bpy.context.scene.cycles.film_transparent = True

# objects list
objs = [create_table('Table', bpyscene, location=(3.8, 0.5, 0.4), scale=(0.4, 0.4, 0.4)), create_chair('Chair', bpyscene, location=(4.5, 2.1, 0.3), scale=(0.4, 0.4, 0.4), rotation=(0, 0, -3.8)), create_monkey(bpyscene, location=(3, 2, 1)), create_icospehre(bpyscene, location=(2,1,1))]

# unlink all objects
for obj in objs:
    bpyscene.objects.unlink(obj)
layers = []

# render object one by one and save to dictionary
for i, obj in enumerate(objs):
    bpyscene.objects.link(obj)
    variants = render(bpyscene, obj, materials_list)
    shapes = [{"children": 0, "id": 0, "name": obj.name, "variants": variants}]
    layers.append({"id": i, "name": obj.name, "shapes": shapes})
    bpy.data.objects.remove(obj)

# save json file with object and materials
DATA = {"layers": layers}
with open('data.json', 'w') as outfile:
    json.dump(DATA, outfile, indent=4)

