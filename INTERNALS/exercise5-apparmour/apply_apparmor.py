import docker

client = docker.from_env()

image_name = "flask-apparmor"

# Check if the image already exists
try:
    client.images.get(image_name)
    print(f"Image '{image_name}' already exists. Skipping build.")
except docker.errors.ImageNotFound:
    print(f"Image '{image_name}' not found. Building...")
    client.images.build(path=".", tag=image_name)

# Run the container with existing/built image
container = client.containers.run(
    image_name,
    ports={'5000/tcp': 5000},
    security_opt=["apparmor=docker_myprofile"],
    detach=True
)

print(f"Container started: {container.short_id}")

# Verify AppArmor profile
container_info = client.api.inspect_container(container.id)
apparmor_profile = container_info['HostConfig']['SecurityOpt']

print(f"AppArmor profile applied: {apparmor_profile}")

# Stop container
print("Stopping and removing container...")
container.stop(timeout=5)
container.remove()
print("Done.")
