#!/usr/bin/env python3

from matplotlib import use
use("Agg")
from matplotlib.pyplot import savefig, plot, xlabel, ylabel, clf, legend, axvline, ylim, text, rc, tight_layout, subplots_adjust
import numpy as np
from csv import reader
from glob import glob
from math import floor

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
    for gc_type in ["GC", "QTP"]:
        filename = max(glob("query_output_{}_{}".format(gc_type,dataset)))
        with open(filename) as f:
            csv_reader = reader(f)
            next(csv_reader)
            ticks, timestamps, query_runtime, trav_index, trav_vol, trav_unprod = zip(*csv_reader)

            ticks = np.array(list(map(int, ticks)))
            timestamps = np.array(list(map(int, timestamps)))
            query_runtime = np.array(list(map(float, query_runtime)))
            trav_index = np.array(list(map(float, trav_index)))
            trav_vol = np.array(list(map(float, trav_vol)))
            trav_unprod = np.array(list(map(float, trav_unprod)))

            milestones = np.array(list(tick_milestones(ticks, timestamps, 60000)))/100

            window = 20

            xlabel("Update Operations [$\\times 10^3$]")
            ylabel("Avg. Query Runtime [ms]")
            ylim(0,30)
            # plot((ticks/100)[:-window+1], np.convolve(query_runtime, np.ones(window), "valid"),".")
            # plot(ticks/100, list(map(percentile(50), sliding_window(query_runtime, 10))))
            plot(ticks/100, [np.percentile(list(window), 50) for window in sliding_window(query_runtime,10)])
            # plot(ticks/100, list(map(percentile(90), sliding_window(query_runtime, 30))))
            # plot(ticks/100, list(map(percentile(10), sliding_window(query_runtime, 30))))
            for m, t in milestones:
                axvline(t, linewidth=0.5, alpha=0.5,linestyle=":")
                text(t-.35, 35, "{} min".format(int(m*100)), rotation=90, color="C0",alpha=0.5)
            tight_layout()
            subplots_adjust(top=.85)
            savefig("query_runtime_{}_{}.pdf".format(gc_type, dataset))
            savefig("query_runtime_{}_{}.eps".format(gc_type, dataset))
            clf()

            xlabel("Update Operations [$\\times 10^3$]")
            ylabel("Index Nodes [$\\times 10^3$]")
            plot(ticks/100, trav_index/1000, "C7", label="Total")
            plot(ticks/100, trav_vol/1000, "C0", label="Volatile")
            plot(ticks/100, trav_unprod/1000, "C1", label="Unproductive")
            ylim(-.1, 4)
            for m, t in milestones:
                axvline(t, linewidth=0.5, alpha=0.5,linestyle=":")
                text(t-.35, 4.6, "{} min".format(int(m*100)), rotation=90, color="C0",alpha=0.5)
            legend()
            tight_layout()
            subplots_adjust(top=.85)
            savefig("trav_nodes_{}_{}.pdf".format(gc_type, dataset))
            savefig("trav_nodes_{}_{}.eps".format(gc_type, dataset))
            clf()
