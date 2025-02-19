# Response time plots
import json
import matplotlib.pyplot as plt
import numpy as np

MAX_POINTS = 1_000_000


# ----------------------------------------------------------------------------
# Histogram plot
def histogram_plot(data, max_points=MAX_POINTS, num_bins=100,
                   title="Histogram", xlabel="Response time (s)",
                   filename='histogram.png'):
    d = data[:max_points]
    plt.hist(d, bins=num_bins, color='steelblue', edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.savefig(filename, bbox_inches="tight")
    plt.close()

# ----------------------------------------------------------------------------
# Scatter plot
def scatter_plot(data, max_points=MAX_POINTS,
                 title="Scatter plot", ylabel="Response time (s)",
                 filename='scatter.png'):
    d = data[:max_points]
    fig = plt.scatter(x=range(len(d)), y=d, s=1, color='steelblue')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.savefig(filename, bbox_inches="tight")
    plt.close()

# ----------------------------------------------------------------------------
# Percentile plot
def percentile_plot(data, max_points=MAX_POINTS, window=10_000,
                    title="Percentile plot", ylabel="Response time (s)",
                    filename='percentiles.png'):
    d = data[:max_points]
    windows = np.reshape(d, (-1, window))
    dmean = np.mean(windows, axis=1)
    dmedian = np.median(windows, axis=1)
    d95 = np.percentile(windows, 95, axis=1)
    d99 = np.percentile(windows, 99, axis=1)

    # Plot all series in a line plot
    plt.plot(dmean, label='Mean', color='steelblue', linestyle='-')
    plt.plot(dmedian, label='Median', color='steelblue', linestyle='--')
    plt.plot(d95, label='95th percentile', color='steelblue', linestyle='-.')
    plt.plot(d99, label='99th percentile', color='steelblue', linestyle=':')

    xticks = np.arange(0, max_points//window, 4)
    plt.xticks(ticks=xticks, labels=xticks * window, rotation=90)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.legend(loc='upper right')
    plt.savefig(filename, bbox_inches="tight")
    plt.close()

# ----------------------------------------------------------------------------
# Heatmap plot
def heatmap_plot(data, max_points=MAX_POINTS, x_points=20, y_points=40,
                 title="Heatmap plot", ylabel="Response time (s)",
                 filename='heatmap.png'):
    d = data[:max_points]
    window = max_points//x_points
    num_bins = y_points
    d_min = np.min(d)
    d_max = np.max(d)
    windows = np.reshape(d, (-1, window))
    histograms = np.array([np.histogram(window, bins=num_bins, range=(d_min, d_max))[0] for window in windows])
    bin_edges = np.histogram_bin_edges(data, bins=num_bins, range=(data.min(), data.max()))
    plt.imshow(histograms.T, aspect='auto', cmap='Reds', origin='lower')
    plt.colorbar(label='Number of values')
    xticks = np.arange(0, x_points, 2)
    plt.xticks(ticks=xticks, labels=xticks * window, rotation=90)
    yticks = np.arange(0, num_bins, 4)
    plt.yticks(ticks=yticks, labels=np.round(yticks*(d_max-d_min)/num_bins, 2))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.savefig(filename, bbox_inches="tight")
    plt.close()


