#!/usr/bin/env python3

from matplotlib import use
use("Agg")
from matplotlib.pyplot import savefig, plot, xlabel, ylabel, clf, legend, axvline, ylim, text
import numpy as np
from csv import reader
from glob import glob
from math import floor
from statistics import mean, median

def tick_milestones(ticks, timestamps, interval):
    last_milestone = -1
    for tick, timestamp in zip(ticks, timestamps):
        current_milestone = floor(timestamp/interval)
        if current_milestone > last_milestone:
            yield current_milestone, tick
        last_milestone = current_milestone

def partition(iterable, partition_length):
    buf = []
    for item in iterable:
        buf.append(item)
        if len(buf) == partition_length:
            yield iter(buf)
            buf = []
    if len(buf) > 0:
        yield iter(buf)

def sliding_window(iterable, window_length):
    buf = []
    for item in iterable:
        buf.append(item)
        if len(buf) > window_length:
            buf.pop(0)
        yield iter(buf)

def percentile(perc):
    return lambda iterable: np.percentile(list(iterable), perc)

for dataset in ["synthetic", "real"]:
    xlabel("Update Operations [1k]")
    ylabel("Avg. Query Runtime [ms]")
    # ylim(0, 20)
    for gc_type in ["Default", "QTP"]:
        filename = max(glob("query_output_{}_{}".format(gc_type,dataset)))
        with open(filename) as f:
            csv_reader = reader(f)
            next(csv_reader)
            ticks, timestamps, query_runtime, trav_index, trav_vol, trav_unprod = zip(*csv_reader)

            ticks = np.array(list(map(int, ticks)))
            timestamps = np.array(list(map(int, timestamps)))
            query_runtime = np.array(list(map(float, query_runtime)))

            plot(
                    ticks/100, 
                    [median(window) for window in sliding_window(query_runtime,15)],
                    label=gc_type
            )
    legend()
    savefig("qtp_cost_{}.pdf".format(dataset))
    clf()
