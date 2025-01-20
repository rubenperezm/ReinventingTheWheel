# Load Balancer

A load balancer is a device that distributes network or application traffic across a cluster of servers. Load balancers are used to increase capacity (concurrent users) and reliability of applications. They improve the overall performance of applications by decreasing the burden on servers associated with managing and maintaining application and network sessions, as well as by performing application-specific tasks.

We have implemented a simple load balancer in Python. The load balancer is implemented as a class that takes a list of servers and a list of clients. The load balancer assigns each client to a server using one of the Static Load Balancing Algorithms we have implemented (round-robin or random). 

## Usage
Once we are in `/load_balancer` directory, we can run the following command to run a backend server:
```bash
python be.py -p PORT
```
where `PORT` is the port number on which the server will listen for incoming connections. By default, the load balancer listens on port 8080.

We can create as many backend servers as we want.

To run the load balancer, we can run the following command:
```bash
python lb.py [-h] -b HOST:PORT [HOST:PORT ...] [-c HEALTHCHECK] [-s {rr,rand}] [-p PORT]
```
where:
- `-b HOST:PORT [HOST:PORT ...]` is a list of backend servers that the load balancer will distribute incoming requests to.
- `-c HEALTHCHECK` is the health check interval in seconds. The load balancer will check the health of the backend servers every `HEALTHCHECK` seconds. If a server is not healthy, the load balancer will stop sending requests to that server.
- `-s {rr,rand}` is the load balancing strategy. We can choose between round-robin (`rr`) and random (`rand`) strategies.
- `-p PORT` is the port number on which the load balancer will listen for incoming connections. By default, the load balancer listens on port 80.

Once we have started the backend servers and the load balancer, we can open a new terminal and send requests to the load balancer using the following command:
```bash
curl http://localhost:PORT
```
where `PORT` is the port number on which the load balancer is listening for incoming connections.

If we want to test the load balancer with multiple clients, we have run `run_parallel_clients.sh` script:
```bash
./run_parallel_clients.sh
```