import bpy
from figures import *


def create_room(length, width, height, scene):
    """Creates a room with given dimensions and returns 6 BlendData objects"""
    # Room vertices
    vertices = [(0, 0, 0), (0, width, 0), (length, width, 0), (length, 0, 0), (0, 0, height), (0, width, height), (length, width, height) , (length, 0, height)]

    # creates room planes
    floor = create_plane_object("Floor", vertices, [0, 1, 2, 3])
    ceiling = create_plane_object("Ceiling", vertices, [4, 5, 6, 7])

    wall_1 = create_plane_object("Wall 1", vertices, [0, 1, 5, 4])
    wall_2 = create_plane_object("Wall 2", vertices, [1, 2, 6, 5])
    wall_3 = create_plane_object("Wall 3", vertices, [2, 3, 7, 6])
    wall_4 = create_plane_object("Wall 4", vertices, [3, 0, 4, 7])

    scene.objects.link(floor)
    scene.objects.link(ceiling)
    scene.objects.link(wall_1)
    scene.objects.link(wall_2)
    scene.objects.link(wall_3)
    scene.objects.link(wall_4)


def create_table(name, scene, location, scale):
    """Create simple table"""
    # deselect all object on the sceene
    bpy.ops.object.select_all(action='DESELECT')

    # creates legs
    legs = []
    for i in range(1, 5):
        legs.append(create_cuboid("Leg " + str(i), 0.2, 0.2, 1))

    # set up legs location
    x, y = 0, 0
    for leg in legs:
        leg.location = (x, y, 0)
        if y == 0:
            y += 2
        elif y == 2:
            x = 1
            y = 0
    # create top of table
    table = create_cuboid(name, 1.8, 2.8, 0.2)
    table.location = (-0.3, -0.3, 1)

    # join all parts together
    for leg in legs:
        scene.objects.link(leg)
        leg.select = True
    scene.objects.link(table)
    table.select = True
    scene.objects.active = table
    bpy.ops.object.join()

    # set scale
    table.scale = scale
    # set table location
    table.location = location

    return table


def create_chair(name, scene, location, scale, rotation):
    """Creates simple chair"""
    # deselect all object on the sceene
    bpy.ops.object.select_all(action='DESELECT')

    # creates legs
    legs = []
    for i in range(1, 5):
        legs.append(create_cuboid("Leg " + str(i), 0.12, 0.12, 0.8))

    # set up legs location
    x, y = 0, 0
    for leg in legs:
        leg.location = (x * 0.8, y * 0.8, 0)
        if y == 0:
            y += 1
        elif y == 1:
            x = 1
            y = 0

    # backrest
    backrest = create_cuboid('Backrest', 0.92, 0.12, 1)
    backrest.location = (0, 0, 0.8)

    # chair
    chair = create_cuboid(name, 0.92, 0.92, 0.12)
    chair.location = (0, 0, 0.8)

    # join all parts together
    for leg in legs:
        scene.objects.link(leg)
        leg.select = True

    scene.objects.link(backrest)
    backrest.select = True
    scene.objects.link(chair)
    chair.select = True
    scene.objects.active = chair
    bpy.ops.object.join()

    # set chair location on the scne
    chair.location = location
    # set scale
    chair.scale = scale
    # set rotation
    chair.rotation_euler = rotation

    return chair


def create_monkey(scene, location):
    """Create monkey"""
    bpy.ops.mesh.primitive_monkey_add(location=location)
    return scene.objects['Suzanne']


def create_icospehre(scene, location):
    """Create icospehre"""
    bpy.ops.mesh.primitive_ico_sphere_add(location=location)
    return scene.objects['Icosphere']
