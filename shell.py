import subprocess
import sys
from audit import start_session, end_session


def start_container_shell(container_name: str, username: str):
    print("[INFO] Starting secure shell session")
    print("[INFO] Type 'exit' to leave the container")

    session_id = start_session(username, container_name)

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

        exit_code = process.returncode

    except KeyboardInterrupt:
        print("\n[INFO] Session interrupted by user")
        exit_code = 130

    except Exception as e:
        print(f"[ERROR] Failed to start shell: {e}")
        exit_code = 1

    finally:
        end_session(session_id, exit_code)
        print("[INFO] Container shell session ended")