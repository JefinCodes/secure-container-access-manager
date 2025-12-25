import subprocess
import sys


def start_container_shell(container_name: str):
    print("[INFO] Starting secure shell session")
    print("[INFO] Type 'exit' to leave the container")

    try:
        process = subprocess.run(
            [
                "docker",
                "exec",
                "-it",
                container_name,
                "/bin/sh"
            ],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
    except KeyboardInterrupt:
        print("\n[INFO] Session interrupted by user")
    except Exception as e:
        print(f"[ERROR] Failed to start shell: {e}")
        return

    print("[INFO] Container shell session ended")