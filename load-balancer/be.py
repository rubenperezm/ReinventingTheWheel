import argparse
import socket

def start_server(port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(5)
    print(f"Listening on port {port}...")

    while True:
        client_socket, address = server_socket.accept()

        print(f"Received request from {address[0]}")

        data = client_socket.recv(1024).decode()
        print(data)

        message = f"HTTP/1.1 200 OK\n\nHello from the Backend Server on port {port}!"
        client_socket.sendall(message.encode())
        print("Replied with a hello message")

        client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        help="Port number for the backend server"
    )

    args = parser.parse_args()

    start_server(args.port)
