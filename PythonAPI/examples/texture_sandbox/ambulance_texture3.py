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

# Set the path to the texture file
texture_path = "colorful_cat.jpeg"

import carla

# connect to the CARLA simulator
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

# get the blueprint for the ambulance vehicle
blueprint_library = world.get_blueprint_library()
ambulance_bp = blueprint_library.find('vehicle.ford.ambulance')

# spawn the ambulance vehicle
spawn_point = carla.Transform(carla.Location(x=50.0, y=0.0, z=2.0), carla.Rotation(yaw=0.0))
ambulance = world.spawn_actor(ambulance_bp, spawn_point)

# get the material from the ambulance blueprint and create a new one with the input image as its texture
texture_path = os.path.join(os.getcwd(), 'colorful_cat.jpeg')
with open(texture_path, 'rb') as f:
    texture_data = f.read()

material = ambulance_bp.get_attribute('color').recommended_values[0].as_material()
material.set_texture(0, carla.Texture('MyTexture', texture_data))

# apply the new material to the ambulance
ambulance.set_material_slot(0, material)

# wait for some time to see the result
world.wait_for_tick()

# destroy the ambulance vehicle
ambulance.destroy()
