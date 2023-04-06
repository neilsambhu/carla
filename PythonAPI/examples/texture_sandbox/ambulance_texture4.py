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

import carla.libcarla as libcarla
from PIL import Image

# Load input image
image_path = "colorful_cat.jpeg"
image = Image.open(image_path)

# Create new texture for vehicles
#texture = carla.Texture("CustomTexture", image.tobytes())

# create a connection to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# get the world object from the server
world = client.get_world()

# get the blueprint library
blueprint_library = world.get_blueprint_library()

# get the blueprint for a white car
white_car_bp = blueprint_library.filter('vehicle.*')[0]

# set the color of the car to white
white_car_bp.set_attribute('color', '255,255,255')

# set the spawn location of the first car
spawn_point = carla.Transform(carla.Location(x=50.0, y=50.0, z=2.0))

# spawn 10 white cars at different locations in the world
for i in range(10):
    # try to spawn the car at the current location
    try:
        white_car = world.spawn_actor(white_car_bp, spawn_point)
    # if spawn fails, move the spawn location and try again
    except RuntimeError:
        spawn_point.location.x += 10.0
        spawn_point.location.y += 10.0
        white_car = world.spawn_actor(white_car_bp, spawn_point)
    
    # move the spawn location for the next car
    spawn_point.location.x += 50.0
    spawn_point.location.y += 50.0
time.sleep(600)
