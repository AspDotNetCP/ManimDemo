import bpy
import os

# Path to the folder containing the PNG files
image_folder = r"C:\Downloads\Labyrinth-of-Fear-3D-main\My_Game\media\output_folder"  # Update to the correct path

# Get the list of PNG files in the folder
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])

# Clear existing objects
bpy.ops.wm.read_factory_settings(use_empty=True)

# Create a new scene
scene = bpy.context.scene

# Set the render resolution
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

# Set the frame range
scene.frame_start = 1
scene.frame_end = len(image_files)

# Create a new plane
bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
plane = bpy.context.object

# Create a new material
material = bpy.data.materials.new(name="ImageMaterial")
material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]

# Create an image texture node
image_texture = material.node_tree.nodes.new('ShaderNodeTexImage')
material.node_tree.links.new(bsdf.inputs['Base Color'], image_texture.outputs['Color'])

# Assign the material to the plane
plane.data.materials.append(material)

# Load the first image to initialize the texture
image_path = os.path.join(image_folder, image_files[0])
image = bpy.data.images.load(image_path)
image_texture.image = image

# Animate the plane by changing the texture for each frame
for frame_number, image_file in enumerate(image_files, start=1):
    image_path = os.path.join(image_folder, image_file)
    image_texture.image = bpy.data.images.load(image_path)
    image_texture.image_user.frame_start = frame_number
    image_texture.image_user.frame_offset = frame_number - 1
    image_texture.image_user.use_auto_refresh = True

# Set the output path for the rendered animation
scene.render.filepath = r"C:\Downloads\Labyrinth-of-Fear-3D-main\My_Game\media\output_folder\animation"  # Update to the correct path
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'

# Render the animation
bpy.ops.render.render(animation=True)