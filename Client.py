import socket


# HELPER FUNCTIONS
# send a single line
def send_line(sockett: socket.socket, text: str) -> None:
    sockett.sendall((text + "\n").encode("utf-8"))

# Recieve line and strip
def recieve_line(sockett: socket.socket) -> str:
    data = sockett.recv(1024)
    return data.decode("utf-8", errors="replace").strip()


# CLIENT CONNECTION FUNCTION
# Handles one connection based on enetered command
def one_connection(host: str, port: int, command: str) -> None:
    print(f"[client] CONNECTING to {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockett:
        # Connect to server
        sockett.connect((host, port))

        # Receive and print welcome banner
        banner = recieve_line(sockett)
        print(f"[client] {banner}")

        # Send the command
        print(f"[client] {command}")
        send_line(sockett, command)

        # Read and print the command response
        response = recieve_line(sockett)
        print(f"[client] {response}")

        # QUIT to close conneciton
        print("[client] QUIT")
        send_line(sockett, "QUIT")

        # Read and print the goodbye
        goodbye = recieve_line(sockett)
        print(f"[client] {goodbye}")

# run two connections
def main() -> None:
    # Prompt user for host and port
    host = input("[client] ENTER SERVER HOST: ").strip()
    port_str = input("[client] ENTER SERVER PORT: ").strip()
    try:
        port = int(port_str)
    except ValueError:
        print("[client] INVALID PORT")
        return

    # Prompt for commands
    command1 = input("[client] ENTER FIRST COMMAND: ").strip()
    command2 = input("[client] ENTER SECOND COMMAND: ").strip()

    # Run both connections 
    print("\n CONNECTION ONE")
    one_connection(host, port, command1)

    print("\n CONNECTION TWO")
    one_connection(host, port, command2)

if __name__ == "__main__":
    main()
