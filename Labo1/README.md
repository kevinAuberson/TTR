Introduction to to capacity planning and performance analysis with SimPy
========================================================================

In this lab, we want to use SimPy to simulate a single server system and evaluate the performance of the system. The system is depicted below.

![Single server system](images/queue.svg)

We are going to evaluate the question: if the arrival rate $\lambda$ doubles, how do we need to increate $\mu$ to achieve the same performance?

We will evaluate this question for different cases, presented in the sections below.

> [!NOTE]
> Write your report using the template `Report.md`. You can write it in English or French


Case 1a: Base scenario M/M/1
----------------------------

The base scenario is as follows:

- Requests arrive according to a Poisson process with $\lambda = 90$ requests per second.
- Requests have an exponential service time distribution with rate parameter $\mu$ requests per second (i.e., the mean service time is $1/\mu$).
- The server uses an FCFS scheduling policy.

We want to achieve a mean response time $E[t] = 100\ ms$.

Use the M/M/1 queueing model to compute the required service rate $\mu$ for this scenario.



Case 1b: M/M/1 model when doubling the arrival rate
--------------------------------------------------

Let's assume that the arrival rate $\lambda$ doubles to $\lambda = 180/s$.

Do we need to double the service rate $\mu$ to achieve the same mean response time $E[T]$? The answer is no! Using the M/M/1 model, compute the mean response time $E[T]$ if $\mu$ doubles.

Which value of $\mu$ is required to achieve the same mean response time as in the base scenario? Use the M/M/1 model to compute this value. Then insert this value in the table on top of this document.



Using SimPy
-----------

Analytical models don't allow us to evaluate more complex scenarios. We will therefore use SimPy as simulator to evaluate the performance of the system.

### Installation

Follow the tutorial [SimPy in 10 minutes](https://simpy.readthedocs.io/en/latest/simpy_intro/index.html) to install SimPy and run the first examples.

To accelerate the SimPy simulations you can optionally install PyPy, a faster Python interpreter: [PyPy installation](https://doc.pypy.org/en/latest/install.html). If you use PyPy, you need to add the SimPy and NumPy packages to PyPy:

```bash
pypy3 -m ensurepip
pypy3 -m pip install simpy numpy
```

To run simulations with PyPy, use the `pypy3` command instead of `python3`.

### M/M/1 simulation

The model `models/simpy_m_m_1_mean.py` already provides an implementation of the M/M/1 model. Use this model to simulate Cases 1a and 1b. Do the results correspond to the analytical results?



Case 2a: Batch arrivals
-----------------------

The M/M/1 model is not a realistic approximation of real-world Web traffic. A Web page contains several objects such as the HTML page, images, or JavaScript files. We will now consider an arrival process, where requests arrive in bursts (batch arrival process)

- Web page requests arrive according to a Poisson with a rate $\lambda$.
- A web page requires between 1 and 9 file downloads, according to a uniform distribution.
- Each file download has a exponential service time with parameter $\mu$.

To simulate this model, do the following:

- Copy the file `simpy_m_m_1.py` into a file `simpy_batch.py`.
- Compute the arrival rate of web pages $\lambda$ such that the arrival rate of file download requests is equal to 90 per second, as in Case 1a.
- Adapt the implementation of the `request_generator` in file `sim_batch.py` such that Web page requests arrive with this rate and that each Web page request generates a uniformly distributed random number of 1 to 9 file requests on the server.

Perform simulation to determine the mean service rate $\mu$ such that the mean response time $E[t] = 100$ ms.



Case 2b: Batch arrivals and double arrival rate
-----------------------------------------------

Now double the arrival rate of Web requests, which doubles the arrival rate of file requests, too.

Simulate the model to determine the required service rate such that the reponse time is again 100 ms.



Case 3a: Batch arrivals and 99th percentile
-------------------------------------------

Up to now we've determined the required service rate to achieve a *mean* response time $E[t] = 100$ ms. That means, we've performed capacity planning based on mean values.

In the real world, mean values won't tell us if there is a problem. We have to look at the 'slow' responses and make sure that not many users experience bad performance.

This is why we will look at the 99th percentile of the response time from now on.

If you evaluated the 99th percentile of the previous simulation 2b, you would have seen that it is higher than 400 ms, which may not be acceptable for a Web service.
We will therefore use 300 ms as target value of the 99th percentile of the response time. That is, only 1% of users will see a worse response time.

Perform the simulation:

- Use a Web page arrival rate of 90 requests per second, as in case 2a.
- At the end of the file `simpy_batch.py`, compute and print the 99th percentile of the response time. You can use the function `numpy.percentile()` for this computation.
- Adapt the service rate $\mu$ to achieve a 99th percentile of 300 ms.



Case 3b: Batch arrivals, 99th percentile and double arrival rate
----------------------------------------------------------------

Now double the arrival rate of Web requests, which doubles the arrival rate of file requests, too.

Simulate the model to determine the required service rate such that the 99th percentile of the reponse time is again 300 ms.



Visualization of the response time distribution
----------------------------------------------

Visualizing the response time distribution can help to understand the performance of the system.

You can use the functions defined in the file `visualization/plots.py` to plot the response time distribution using different methods.

These functions expect a NumPy array with the response times as input. You can save the simulation results into a file and then read it for visualization.
