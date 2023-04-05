import carla
import subprocess, time, os

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

# Connect to the CARLA simulator
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the world and get the ambulance actor
world = client.get_world()
blueprint_library = world.get_blueprint_library()
ambulance_bp = blueprint_library.find("vehicle.ford.ambulance")

# Spawn 10 ambulance vehicles
spawn_points = world.get_map().get_spawn_points()
for i in range(10):
    spawn_point = spawn_points[i]
    ambulance_actor = world.spawn_actor(ambulance_bp, spawn_point)
    ambulance_actor.set_simulate_physics(False)
    ambulance_actor.set_attribute('role_name', 'ambulance{}'.format(i))

# Get the pre-existing ambulance vehicle
ambulance_actors = world.get_actors().filter('vehicle.ford.ambulance')
ambulance_actor = ambulance_actors[0]

'''# Modify the texture of the pre-existing ambulance vehicle
material = ambulance_actor.get_material(0)
texture_package = "/Game/MyAmbulance"
asset_tools = world.get_asset_tools()
asset_tools.import_asset(texture_path, texture_package)
texture_name = "Texture2D'/Game/MyAmbulance/MyAmbulanceTexture.MyAmbulanceTexture'"
texture = blueprint_library.find(texture_name)
material.set_texture_param("Texture", texture)'''
