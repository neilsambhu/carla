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

# Connect to the CARLA simulator
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Get the world object
# world = client.get_world()
# Load layered map for Town 01 with minimum layout plus buildings and parked vehicles
world = client.load_world('Town01_Opt', carla.MapLayer.Buildings | carla.MapLayer.ParkedVehicles)
# world = client.load_world('Town04_Opt', carla.MapLayer.Buildings | carla.MapLayer.ParkedVehicles)
# world = client.load_world('Town10HD_Opt', carla.MapLayer.Buildings | carla.MapLayer.ParkedVehicles)
# Toggle all buildings off
# world.unload_map_layer(carla.MapLayer.Buildings)
# world.unload_map_layer(carla.MapLayer.All)
# world.unload_map_layer(carla.MapLayer.Buildings)
# world.unload_map_layer(carla.MapLayer.Decals)
# world.unload_map_layer(carla.MapLayer.Foliage)
# world.unload_map_layer(carla.MapLayer.Ground)
# world.unload_map_layer(carla.MapLayer.ParkedVehicles)
# world.unload_map_layer(carla.MapLayer.Particles)
# world.unload_map_layer(carla.MapLayer.Props)
# world.unload_map_layer(carla.MapLayer.StreetLights)
# world.unload_map_layer(carla.MapLayer.Walls)

# manual control
# manual_control = subprocess.Popen('python manual_control.py')
# manual_control.wait()
time.sleep(600)

# Define the blueprint of the vehicle you want to spawn
blueprint_library = world.get_blueprint_library()
vehicle_bp = blueprint_library.find('vehicle.tesla.model3')

# Define the spawn transform for the vehicle
#spawn_point = carla.Transform(carla.Location(x=-115, y=42.6, z=0), carla.Rotation())
spawn_point = carla.Transform(carla.Location(x=42.6, y=-115, z=0), carla.Rotation())

# Spawn the vehicle
vehicle = world.spawn_actor(vehicle_bp, spawn_point)

# Wait for a few seconds to let the vehicle spawn properly
world.wait_for_tick()

# Do something with the vehicle
print(f'Spawned vehicle {vehicle.id}')

