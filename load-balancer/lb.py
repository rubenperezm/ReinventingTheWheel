import argparse
import importlib
import requests
import socket
import time
import threading

from sel import backend_selection


class LoadBalancer():
    def __init__(self, port, backends, selection_method, healthcheck_interval):
        self.port = port
        self.backends = self.parse_backends(backends)
        self.healthcheck_interval = healthcheck_interval
        self.selection_method = selection_method
        self.available_backends = [True] * len(backends)

        self.start_server()

    def handle_client(self, client_socket, backend_host, backend_port):
        print(f'Received request from {client_socket.getpeername()[0]}')

        request = client_socket.recv(1024).decode()
        print(request)

        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect((backend_host, backend_port))
        backend_socket.sendall(request.encode())

        response = backend_socket.recv(1024)
        backend_socket.close()

        print(f'Response from server {backend_host}:{backend_port}: {response.decode()}')

        client_socket.sendall(response)
        client_socket.close()

    def health_check(self):
        while True:
            for i, (host, port) in enumerate(self.backends):
                url = f"http://{host}:{port}/health"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        self._change_health_status(i, True)
                    else:
                        self._change_health_status(i, False)
                except:
                    self._change_health_status(i, False)
                
            time.sleep(self.healthcheck_interval)

    def _change_health_status(self, i, status):
        self.available_backends[i] = status
        print(f"Backend server {self.backends[i][0]}:{self.backends[i][1]} is {'healthy' if status else 'unhealthy'}")

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', self.port))
        server_socket.listen(5)
        print(f"Listening on port {self.port}...")

        healthcheck_thread = threading.Thread(target=self.health_check)
        healthcheck_thread.daemon = True
        healthcheck_thread.start()

        backend_selector = backend_selection(self.backends, self.available_backends, self.selection_method)

        while True:
            backend_host, backend_port = next(backend_selector)
            client_socket, _ = server_socket.accept()
            client_handler = threading.Thread(
                target=self.handle_client,
                args=(client_socket, backend_host, backend_port)
            )
            client_handler.start()

    def parse_backends(self, backends):
        parsed_backends = []

        for backend in backends:
            host, port = backend.split(':')
            parsed_backends.append((host, int(port)))

        return parsed_backends

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b",
        "--backends",
        type=str,
        nargs="+",
        required=True,
        metavar="HOST:PORT",
        help="Hostnames and ports of the backend servers"
    )

    parser.add_argument(
        "-c",
        "--healthcheck",
        type=int,
        default=10,
        help="Health check interval in seconds"
    )

    parser.add_argument(
        "-s",
        "--selection",
        type=str,
        default="rr",
        choices=["rr", "rand"],
        help="Selection method for backends. Choose between 'rr' (round-robin) and 'rand' (random)"
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=80,
        help="Port number for the load balancer"
    )

    args = parser.parse_args()

    backends = args.backends
    port = args.port
    healthcheck_interval = args.healthcheck

    selection_module = importlib.import_module('sel')
    selection_method = getattr(selection_module, args.selection)

    LoadBalancer(port, backends, selection_method, healthcheck_interval)