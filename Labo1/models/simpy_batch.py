import simpy
import random
import numpy as np
from visualization.plots import heatmap_plot, histogram_plot, scatter_plot, percentile_plot

import os
print(f"Current working directory: {os.getcwd()}")

# Parameters
arrival_rate_web = 36.0  # Web page requests per second
service_rate = 234.0  # Service rate for file requests
num_requests = 1_000_000

# Results
response_times = []

# ---------------------------------------------------------------------------
# SimPy model
env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

def request_generator(env):
    for i in range(num_requests):
        yield env.timeout(random.expovariate(arrival_rate_web))
        num_files = random.randint(1, 9)
        for _ in range(num_files):
            env.process(process_request(env))

def process_request(env):
    arrival_time = env.now
    job = server.request()
    # Wait for the server to become available (wait in the queue)
    yield job
    # Process the request
    yield env.timeout(random.expovariate(service_rate))
    departure_time = env.now
    response_times.append(departure_time - arrival_time)
    server.release(job)

env.process(request_generator(env))
env.run()

# ---------------------------------------------------------------------------
# Compute the results
mean_response_time = np.mean(response_times)
print(f'Mean response time: {mean_response_time:.4f} s')
response_time_99 = np.percentile(response_times, 99)
print(f'Response time (99th percentile): {response_time_99:.4f} s')

print(f"Number of response times collected: {len(response_times)}")

response_times = np.array(response_times)

# Generate plots
try:
    histogram_plot(response_times, title="Histogram of Response Times", xlabel="Response time (s)", filename='histogram.png')
    scatter_plot(response_times, title="Scatter Plot of Response Times", ylabel="Response time (s)", filename='scatter.png')
    percentile_plot(response_times, title="Percentile Plot of Response Times", ylabel="Response time (s)", filename='percentiles.png')
    heatmap_plot(response_times, title="Heatmap of Response Times", ylabel="Response time (s)", filename='heatmap.png')
    print("Plots have been successfully generated and saved.")
except Exception as e:
    print(f"An error occurred while generating plots: {e}")
