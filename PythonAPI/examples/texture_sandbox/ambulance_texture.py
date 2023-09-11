#!/usr/bin/env python
# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================
import glob
import os
import sys
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import carla
import subprocess, time

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

# Connect to the CARLA simulator
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Get the ambulance blueprint
blueprint_library = client.get_world().get_blueprint_library()
#for item in blueprint_library:
#	print(f'{item.id}')
#vehicle_bp = blueprint_library.find('vehicle.ambulance')
vehicle_bp = blueprint_library.find('vehicle.ford.ambulance')

# Create a new material with the desired texture
texture_file = 'colorful_cat.jpeg'
with open(texture_file, 'rb') as f:
	image_data = f.read()
height = 512
width = 512
pixel_format = 'RGBA'
#image = carla.Image(image_data, height, width, pixel_format)
raw_texture = carla.RawTexture(texture_data, height, width, pixel_format)
texture = carla.Texture('AmbulanceTexture', raw_texture)
material = carla.Material('AmbulanceMaterial')
material.set_texture('BaseColor', texture)
vehicle_bp.set_attribute('material.0', material)

# Add the new material to the ambulance blueprint
#vehicle_bp.set_attribute('materials', '0', material)

# Spawn the ambulance in the simulator
spawn_point = carla.Transform(carla.Location(x=50, y=0, z=2), carla.Rotation(yaw=180))
vehicle = client.get_world().spawn_actor(vehicle_bp, spawn_point)

# Wait for the simulation to initialize
client.get_world().wait_for_tick()

# Apply the new material to the ambulance
vehicle.apply_physics_control(carla.VehiclePhysicsControl(1.0, 0.0, True, True))

# Wait for the simulation to finish
client.get_world().wait_for_tick()

