import subprocess
import json


def inspect_container(container_name: str):
    try:
        result = subprocess.run(
            ["docker", "inspect", container_name],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError:
        print("[ERROR] Container does not exist or Docker is not running")
        exit(1)

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("[ERROR] Failed to parse Docker response")
        exit(1)

    if not data:
        print("[ERROR] Container not found")
        exit(1)

    container_info = data[0]
    state = container_info.get("State", {})

    if not state.get("Running", False):
        print("[ERROR] Container exists but is not running")
        exit(1)

    return {
        "id": container_info.get("Id"),
        "name": container_info.get("Name", "").lstrip("/"),
        "image": container_info.get("Config", {}).get("Image"),
        "status": state.get("Status")
    }