#!/usr/bin/env python3

from matplotlib import use
use("Agg")
from matplotlib.pyplot import savefig, plot, xlabel, ylabel, clf, legend, ylim,rc , tight_layout
import numpy as np
from csv import reader
from glob import glob
from math import floor
from re import search
from statistics import mean, median

rc("font", size=17, family="serif")
rc("text", usetex=True)

def sliding_window(iterable, window_length):
    buf = []
    for item in iter(iterable):
        buf.append(item)
        if len(buf) > window_length:
            buf.pop(0)
        yield iter(buf)

filenames = glob("query_output_*")
data_synthetic = dict()
data_real = dict()

for filename in filenames:
    periodicity = int(search("_T(?P<periodicity>[0-9]*)", filename).group("periodicity"))
    dataset = search("(?P<dataset>(synthetic|real))", filename).group("dataset")
    data = data_synthetic if dataset == "synthetic" else data_real if dataset == "real" else None
    with open(filename) as f:
        csv_reader = reader(f)
        next(csv_reader)
        ticks, timestamps, query_runtime, trav_index, trav_vol, trav_unprod = zip(*csv_reader)
        data[periodicity] = {
            "ticks": np.array(list(map(int, ticks))),
            "timestamps": np.array(list(map(int, timestamps))),
            "query_runtime": np.array(list(map(float, query_runtime))),
            "trav_index": np.array(list(map(float, trav_index))),
            "trav_vol": np.array(list(map(float, trav_vol))),
            "trav_unprod": np.array(list(map(float, trav_unprod)))
        }

for dataset, data in [("synthetic", data_synthetic), ("real", data_real)]:
    periods = np.array(sorted(list(data.keys())))

    xlabel("GC Period $T$ [s]")
    ylabel("Avg. Query Runtime [ms]")
    plot(periods/1000, [median(data[p]["query_runtime"]) for p in periods], linestyle="-", marker="o")
    ylim(ymax=20)
    tight_layout()
    savefig("periodicity_query_runtime_{}.pdf".format(dataset))
    savefig("periodicity_query_runtime_{}.eps".format(dataset))
    clf()

    xlabel("GC Period $T$ [s]")
    ylabel("Unproductive Nodes [$\\times 10^2$]")
    plot(periods/1000, [median(data[p]["trav_unprod"])/100 for p in periods], linestyle="-", marker="o")
    # ylim(ymax=20)
    tight_layout()
    savefig("periodicity_trav_unprod_{}.pdf".format(dataset))
    savefig("periodicity_trav_unprod_{}.eps".format(dataset))
    clf()

