Server farms and load balancing
===============================

The goal of this lab is to simulate a server farm with a load balancer. In particular, we will evaluate the questions:

- What is better: a single fast server or several slower servers?
- How does the scheduling algorithm (round-robin, random, shortest queue first) affect the performance of the system?

This lab only considers markovian traffic, i.e., the arrival and service times are exponentially distributed. In a follow-up lab, we will consider non-markovian traffic.

> [!NOTE]
> Write your report using the template `Report.md`. You can write it in English or French



Case 1: Base scenario: M/M/1 system
-----------------------------------

As a baseline for comparison, we will first simulate a single fast server system with an M/M/1 queue.

In the `./models/` directory, you will find a Python script that simulates an M/M/1 system.

- The server has an exponential service with rate $\mu = 100$ requests per second
- The arrival rate of requests is between $\lambda = 5..99$ requests per second (5 - 99% utilization)
- The simulation script computes and plots the mean response time and the 99th percentile of the response time for file requests

Run this model to create the plot.

Interpret the results following the template in the `Report.md` file.



Case 2: Load balancing with Round-Robin
---------------------------------------

In this step we want to compare Case 1 (single fast server) with a load balancing configuration with 5 slow servers and round-robin scheduling.

Slighly modify the simulation script to simulate a system with 5 servers, each with a service rate of $\mu = 20$ requests per second. The request generator should use round-robin scheduling to assign requests to the servers.

Interpret the results following the template in the `Report.md` file.



Case 3: Overdimensioning RR
---------------------------

In Case 2 we've observed that loadbalancing with round-robin is inefficient. But how inefficient is it really? We want to quantify this. Or formulated differenty: how many servers do we need to achieve the same performance as a single fast server?

Write down the 99th percentile of the response time for the M/M/1 system at 90% utilization. This is the target value.

Now, modify the simulation script:

- keep the service rate of the servers at $\mu = 20$ requests per second, i.e., the same as in Case 2
- run the simulation with 6, 7, ... servers until you find a configuration where the 99th percentile of the response time at 90% utilization is equal or below the target value.

This should improve the performance of the loadbalancing system for high loads.
Is it possible to improve the performance for low loads as well?


Case 4: Improving the load balancing system
-------------------------------------------

Round-robin is inefficient and much less efficient than a true M/M/k system would be. Can we improve the performance of the loadbalancing system?

The goal of this case is to define a better algorithm than round-robin. Implement two different task assignment algorithms:

- **Shortest-queue-first scheduling (SFQ)**: The request is sent to the server with the shortest queue. This should be easy to implement.
- **Central queue (CQ)**: the load balancer has a central queue. This is more difficult to implement. To make it simpler, you can directly handle the jobs in the `LoadBalancer.hande_request()` method.

Compare the performance of the new scheduling algorithms with the round-robin scheduling and with the M/M/1 system.



Case 5: Mixing servers
----------------------

We will now evaluate a configuration that does not consider the task assignment algorithm, but a mix of fast and slow servers.

In Case 1, we've simulated a single server with a service rate of $\mu = 100$ requests per second.

Now imagine that we have another server which is older a slower that the first server. Implement a round-robin load balancer that distributes the requests between the two servers according to their service rate.

For example if $\mu_1 = 100$ and $\mu_2 = 20$, you could use a list of servers `[server1, server1, server1, server1, server1, server2]` and use round-robin scheduling to assign the requests to the servers. Server1 will receive 5 times more requests than server2.

- If you only consider the throughput, which configuration is better: only the fast server, or both servers?
- Can you find a configuration where the response time is better with only the fast server?
- Can you find a configuration where the response time is better with both servers?



Conclusions
-----------

Use the `Result.md` file to summarize your findings. What did you learn from this lab? What are the implications for the design of server farms and load balancing systems?
