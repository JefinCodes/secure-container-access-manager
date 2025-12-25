import sys
import re
from auth import authenticate_user, bootstrap_first_user, init_db
from rbac import authorize_user
from docker_utils import inspect_container


def print_usage():
    print("Usage:")
    print("  python scam.py enter <container_name>")
    print("")
    print("Commands:")
    print("  enter    Securely enter a container")


def validate_container_name(name: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.-]+$"
    return re.match(pattern, name) is not None


def handle_enter(container_name: str):
    print(f"[INFO] Requested access to container: {container_name}")

    user = authenticate_user()

    authorize_user(user, container_name)

    container = inspect_container(container_name)

    print("[INFO] Docker inspection successful")
    print(f"[INFO] Container '{container['name']}' is running")
    print(f"[DEBUG] User context: {user}")
    print(f"[DEBUG] Container context: {container}")


def main():
    init_db()
    bootstrap_first_user()

    args = sys.argv

    if len(args) < 2:
        print("[ERROR] No command provided\n")
        print_usage()
        sys.exit(1)

    command = args[1]

    if command != "enter":
        print(f"[ERROR] Unknown command: '{command}'\n")
        print_usage()
        sys.exit(1)

    if len(args) < 3:
        print("[ERROR] Container name required\n")
        print_usage()
        sys.exit(1)

    container_name = args[2]

    if not validate_container_name(container_name):
        print("[ERROR] Invalid container name")
        print("Allowed characters: letters, numbers, '_', '-', '.'")
        sys.exit(1)

    handle_enter(container_name)


if __name__ == "__main__":
    main()