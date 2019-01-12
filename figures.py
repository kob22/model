import bpy


def create_plane_object(name, vertices, faces):
    """Creates a plane object from vertices and faces and return a BlendData object"""
    # new object type BlendData Mesh
    new_mesh = bpy.data.meshes.new(name)
    # make mesh from list vertices and faces
    new_mesh.from_pydata(vertices, [], [faces])
    # update
    new_mesh.update()
    return bpy.data.objects.new(name, new_mesh)


def create_cuboid(name, length, width, height):
    """Creates simple cuboid of given dimensions"""
    # Vertices
    vertices = [(0, 0, 0), (0, width, 0), (length, width, 0), (length, 0, 0), (0, 0, height), (0, width, height), (length, width, height) , (length, 0, height)]
    # Faces
    faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    # creates new meshe from vertices and faces
    new_cuboid = bpy.data.meshes.new(name)
    new_cuboid.from_pydata(vertices, [], faces)
    # new cuboid obj
    cuboid_obj = bpy.data.objects.new(name, new_cuboid)

    return cuboid_obj

