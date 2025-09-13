import socket
import threading
from datetime import datetime, timezone

# Server Settings
HOST = "0.0.0.0"
PORT = 6767  
BANNER = "WELCOME TO AIDANS SERVER\n"


# HELPER FUNCTIONS
# Sends okay response with payload
def send_ok(connection, payload:str) -> None:
    connection.sendall(f"OK {payload}\n".encode())

# Sends error message to client
def send_error(connection, message: str) -> None:
    connection.sendall(message.encode())

# Decode bytes into string line
def parse_line(data: bytes) -> str:
    return data.decode().strip()


# COMMAND FUNCTIONS
# Return current time to client
def time_command(connection) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    send_ok(connection, now)

# Echo text back to client
def echo_command(connection, arguments) -> None:
    send_ok(connection, " ".join(arguments))

# Reverese text sent by client
def reverse_command(connection, arguments) -> None:
    if not arguments:
        send_error(connection, b"ERROR REVERSING <text>\n".decode())
    else:
        text = " ".join(arguments)
        send_ok(connection, text[::-1])


# Client function handles each connection
def client(connection: socket.socket, address) -> None:
    print(f"[server] NEW CONNECTION FROM {address}")
    connection.sendall(BANNER.encode())

    try:
        while True:
            # Wait for client if not then close
            data = connection.recv(1024)
            if not data:
                break

            line = parse_line(data)
            print(f"[server] GOT: {line}")

            # split into command and arguments
            parts = line.split()
            cmd = parts[0].upper() if parts else ""
            args = parts[1:]

            # Check command
            if cmd == "TIME":
                time_command(connection)
            elif cmd == "ECHO":
                echo_command(connection, args)
            elif cmd == "REVERSE":
                reverse_command(connection, args)
            elif cmd == "HELP":
                send_ok(connection, "TIME | ECHO <text> | REVERSE <text> | QUIT")
            elif cmd == "QUIT":
                connection.sendall(b"SEE YOU LATER ALLIGATOR\n")
                break
            else:
                connection.sendall(b"ERROR UNKOWN COMMAND\n")
    finally:
        connection.close()
        print(f"[server] CONNECTION CLOSED {address}")


def main() -> None:
    # Create socket and start listening 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"[server] LISTENING ON {HOST}:{PORT}")

        # Handle each client in new thread (mentioned multithreading in class)
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
