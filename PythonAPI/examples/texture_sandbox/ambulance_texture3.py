import carla
import subprocess, time, os, random

def kill_carla_podman():
    kill_process = subprocess.Popen('podman kill --signal KILL -a', shell=True)
    kill_process.wait()
    time.sleep(1)
    kill_process = subprocess.Popen('podman container cleanup --all --rm', shell=True)
    kill_process.wait()
    time.sleep(1)
kill_carla_podman()

# 4/1/2023 7:57:17 PM: launch simulator: start
cmd = f'xhost local:root && podman run --privileged --net=host -e DISPLAY=$DISPLAY carlasim/carla:0.9.13 /bin/bash ./CarlaUE4.sh'
server_process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
time.sleep(10)
# 4/1/2023 7:57:17 PM: launch simulator: end

from PIL import Image

image_path = 'colorful_cat.jpeg'
image = Image.open(image_path)

import carla


client = carla.Client('localhost', 2000)
world = client.get_world()

blueprint_library = world.get_blueprint_library()

# Get the ambulance blueprint
ambulance_bp = blueprint_library.filter('vehicle.audi.etron')[0]

# Create a new material using the image texture
material = carla.Material('MyMaterial')
material.set_texture(0, image_path)

# Set the material to the ambulance blueprint
ambulance_bp.set_attribute('color', '0,0,0')
ambulance_bp.set_attribute('material', material.id)

spawn_point = carla.Transform(carla.Location(x=50, y=50, z=2))

ambulance = world.spawn_actor(ambulance_bp, spawn_point)

mesh = ambulance.get_mesh()
mesh.set_material(0, material)

