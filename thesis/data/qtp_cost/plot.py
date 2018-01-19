#!/usr/bin/env python3

from matplotlib import use
use("Agg")
from matplotlib.pyplot import savefig, plot, xlabel, ylabel, clf, legend, axvline, ylim, text, rc, tight_layout
import numpy as np
from csv import reader
from glob import glob
from math import floor
from statistics import mean, median

rc("font", size=17, family="serif")
rc("text", usetex=True)

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
    xlabel("Update Operations [$\\times 10^3$]")
    ylabel("Avg. Query Runtime [ms]")
    # ylim(ymax=25)
    filename = max(glob("query_output*{}*".format(dataset)))
    with open(filename) as f:
            csv_reader = reader(f)
            next(csv_reader)
            ticks, timestamps, query_runtime, has_children_time, is_matching_time, is_volatile_time, write_time = zip(*csv_reader)
            ticks = np.array(list(map(int, ticks)))
            timestamps = np.array(list(map(int, timestamps)))
            query_runtime = np.array(list(map(float, query_runtime)))
            has_children_time = np.array(list(map(float, has_children_time)))/1000000
            is_matching_time = np.array(list(map(float, is_matching_time)))/1000000
            is_volatile_time= np.array(list(map(float, is_volatile_time)))/1000000
            write_time = np.array(list(map(float, write_time)))/1000000

            traversal_time = query_runtime - has_children_time - is_matching_time - is_volatile_time - write_time;

            traversal_time = np.array(list(map(float, traversal_time)))

            plot(
                    ticks/100, 
                    [median(window) for window in sliding_window(traversal_time,15)],
            )
            plot(
                    ticks/100, 
                    [median(window) for window in sliding_window(traversal_time+is_matching_time,15)],
            )
            plot(
                    ticks/100, 
                    [median(window) for window in sliding_window(traversal_time+is_matching_time+has_children_time,15)],
            )
            plot(
                    ticks/100, 
                    [median(window) for window in sliding_window(traversal_time+is_matching_time+has_children_time+is_volatile_time,15)],
            )
            plot(
                    ticks/100, 
                    [median(window) for window in sliding_window(traversal_time+is_matching_time+has_children_time+is_volatile_time+write_time,15)],
            )

            mean_runtime = mean(query_runtime[-20:])
            mean_write_time = mean(write_time[-20:])
            mean_is_vol_time = mean(is_volatile_time[-20:])
            mean_has_chd_time= mean(has_children_time[-20:])
            mean_is_matching_time = mean(is_matching_time[-20:])
            mean_trav_time = mean(traversal_time[-20:])
            print("""
                    Total:      {}
                    Write:      {}
                    isVolatile: {}
                    hasChildren:{}
                    isMatching: {}
                    postOrder:  {}
                    """.format(
                        mean(query_runtime[-20:]),
                        mean(write_time[-20:]),
                        mean(is_volatile_time[-20:]),
                        mean(has_children_time[-20:]),
                        mean(is_matching_time[-20:]),
                        mean(traversal_time[-20:]),
                        ))


    legend()
    tight_layout()
    savefig("qtp_cost_{}.pdf".format(dataset))
    clf()
