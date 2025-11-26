import docker
import time
import uuid

client = docker.from_env()
api = client.api

image_name = "flask-apparmor"
apparmor_profile = "docker_myprofile"  # change if needed

# 1) Build only if image missing
try:
    client.images.get(image_name)
    print(f"Image '{image_name}' found locally -> skipping build.")
except docker.errors.ImageNotFound:
    print(f"Image '{image_name}' not found -> building...")
    client.images.build(path=".", tag=image_name)
    print("Build finished.")

# 2) Start container
container_name = f"apparmor-test-{uuid.uuid4().hex[:8]}"
container = client.containers.run(
    image_name,
    name=container_name,
    ports={'5000/tcp': 5000},
    security_opt=[f"apparmor={apparmor_profile}"],
    detach=True
)

print(f"Started container {container.short_id} (name={container_name})")
time.sleep(1)  # give container a moment to initialize

# 3) Verify AppArmor profile applied (HostConfig.SecurityOpt)
info = api.inspect_container(container.id)
sec_opts = info.get('HostConfig', {}).get('SecurityOpt', None)
print("HostConfig.SecurityOpt:", sec_opts)

# 4) Test restricted actions
# Note: exec_run returns (exit_code, output_bytes)
tests = [
    ("Read /etc/passwd", ["cat", "/etc/passwd"]),
    ("Run shell echo", ["/bin/bash", "-c", "echo shell_run_ok"])
]

for label, cmd in tests:
    exit_code, output = container.exec_run(cmd, demux=False)
    out = output.decode(errors="replace") if output else ""
    print(f"{label} -> Exit Code: {exit_code}\nOutput:\n{out}\n{'-'*40}")

# 5) Cleanup: stop and remove container
print("Stopping and removing container...")
container.stop(timeout=5)
container.remove()
print("Done.")