"Simulation model for load balancing with SimPy."

import random
from matplotlib import pyplot as plt
import simpy
import numpy as np


# ---------------------------------------------------------------------------
# Request generator
# ---------------------------------------------------------------------------
class Client:
    """A client generates requests and sends them to the load balancer."""
    def generate_requests(self, env, num_requests, arrival_rate, loadbalancer):
        """Generate new requests and send them to the load balancer."""

        for _ in range(num_requests):
            yield env.timeout(random.expovariate(arrival_rate))
            loadbalancer.handle_request()

# ---------------------------------------------------------------------------
# Load balancer
# ---------------------------------------------------------------------------
class LoadBalancer:
    """The loadbalancer manages n servers. It receives requests and forwards them to the servers.

       The load balancer may implement different task assignment policies,
       e.g., round-robin, random, etc.
    """

    def __init__(self, env, servers):
        self.env = env
        self.servers = servers
        self.next_server = 0

    def handle_request(self):
        """Choose a server and send the request to it."""
        arrival_time = self.env.now
        server = self.round_robin() # Use the task assignment policy here
        self.env.process(server.handle_request(arrival_time))

    # Load balancing policies ----------------------------------------------
    def round_robin(self):
        """Round-robin load balancing policy."""
        server = self.servers[self.next_server]
        self.next_server = (self.next_server + 1) % len(self.servers)
        return server

    def shortest_queue_first(self):
        """Shortest queue load balancing policy."""
        server = min(self.servers, key=lambda s: len(s.resource.queue))
        return server

    def process_queue(self):
        """Process requests from the central queue."""
        while True:
            arrival_time = yield self.queue.get()
            server = self.get_available_server()
            if server:
                self.env.process(server.handle_request(arrival_time))

    def get_available_server(self):
        """Get the first available server."""
        for server in self.servers:
            if len(server.resource.queue) == 0:
                return server
        return None

# ---------------------------------------------------------------------------
# Server node
# ---------------------------------------------------------------------------
class Server:
    """A server that processes requests."""

    def __init__(self, env, service_rate, results):
        self.env = env
        self.service_rate = service_rate
        self.resource = simpy.Resource(env, capacity=1)
        self.results = results

    def handle_request(self, arrival_time):
        """Server process: handle the request and write the response time to the results"""

        job = self.resource.request()
        # Wait for the server to become available (wait in the queue)
        yield job
        # Process the request
        yield self.env.timeout(random.expovariate(self.service_rate))
        departure_time = self.env.now
        self.results.append(departure_time - arrival_time)
        self.resource.release(job)



# ===========================================================================
# Main functions to run the simulation with different configurations
# ===========================================================================
def main():
    """Run a number of simulations with different configurations. Generate the result plots.

       In the current implementation, this function runs the simulations of a
       load-balancing server farm.
       The arrival rate is varied for each run to evaluate the performance at different loads
    """

    # Simulation coniguration
    plot_file = "../visualizations/5_server_old_rr.png"
    num_requests = 500_000
    service_rates = [100, 100, 100, 100, 100, 20] # List of service rates of each server
    arrival_rates = list(range(5, 100, 5)) + [99] # List of arrival rates to simulate

    # Lists to store the results of the different simulation runs
    response_times_mean = []
    response_times_99 = []

    for arrival_rate in arrival_rates:
        print(f"Simulating arrival rate = {arrival_rate}")
        response_times = simulate(num_requests, arrival_rate, service_rates)

        response_times_mean.append(np.mean(response_times))
        response_times_99.append(np.percentile(response_times, 99))

    print_results_table(arrival_rates, response_times_mean, response_times_99)
    plot_results(plot_file, arrival_rates, response_times_mean, response_times_99)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def simulate(num_requests, arrival_rate, service_rates):
    """Run a single simulation with the given parameters."""
    response_times = [] # Used for the simulation results

    # Configure the nodes
    env = simpy.Environment()
    client = Client()
    servers = [Server(env, service_rate, response_times) for service_rate in service_rates]
    load_balancer = LoadBalancer(env, servers)

    # Run the simulation
    env.process(client.generate_requests(env, num_requests, arrival_rate, load_balancer))
    env.run()
    return response_times


def print_results_table(arrival_rates, response_times_mean, response_times_99):
    """Print the results in a table format."""
    print()
    print("Results:")
    print("Arrival rate | Mean response time | 99th percentile |")
    print("------------:|-------------------:|----------------:|")
    for i, arrival_rate in enumerate(arrival_rates):
        print(f"{arrival_rate:>12.0f} | {response_times_mean[i]:>18.3f} | {response_times_99[i]:>15.3f} |")

def plot_results(filename, arrival_rates, response_times_mean, response_times_99):
    """Plot the results in a graph."""
    plt.plot(arrival_rates , response_times_mean, label="Mean")
    plt.plot(arrival_rates, response_times_99, label="99th percentile")
    plt.ylim(0, 2.5)
    plt.xlabel("Arrival rate")
    plt.ylabel("Response time (s)")
    plt.legend()
    plt.savefig(filename)
    print()
    print(f"Plot saved to {filename}")


# ---------------------------------------------------------------------------
# Run one of the simulation types

main()
