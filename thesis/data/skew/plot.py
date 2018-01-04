#!/usr/bin/env python3

from matplotlib import use
use("Agg")
from matplotlib.pyplot import savefig, plot, xlabel, ylabel, clf, legend, ylim
import numpy as np
from csv import reader
from glob import glob
from math import floor
from re import search
from statistics import mean, median

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
    skew = float(search("_skew(?P<skew>[0-9.]*)_", filename).group("skew"))
    dataset = search("(?P<dataset>(synthetic|real))", filename).group("dataset")
    data = data_synthetic if dataset == "synthetic" else data_real if dataset == "real" else None
    with open(filename) as f:
        csv_reader = reader(f)
        next(csv_reader)
        ticks, timestamps, query_runtime, trav_index, trav_vol, trav_unprod = zip(*csv_reader)
        data[skew] = {
            "ticks": np.array(list(map(int, ticks))),
            "timestamps": np.array(list(map(int, timestamps))),
            "query_runtime": np.array(list(map(float, query_runtime))),
            "trav_index": np.array(list(map(float, trav_index))),
            "trav_vol": np.array(list(map(float, trav_vol))),
            "trav_unprod": np.array(list(map(float, trav_unprod)))
        }

for dataset, data in [("synthetic", data_synthetic), ("real", data_real)]:
    xlabel("Update Operations [1k]")
    ylabel("Avg. Query Runtime [ms]")
    plot(data[0]["ticks"]/100, [median(w) for w in sliding_window(data[0]["query_runtime"],10)], label="s = 0")
    plot(data[2]["ticks"]/100, [median(w) for w in sliding_window(data[2]["query_runtime"],10)], label="s = 2")
    plot(data[4]["ticks"]/100,[median(w) for w in sliding_window(data[4]["query_runtime"],10)], label="s = 4")
    legend()
    ylim(ymax=60)
    savefig("query_runtime_skews_{}.pdf".format(dataset))
    clf()

    xlabel("Update Operations [1k]")
    ylabel("Traversed Unproductive Nodes [1k]")
    plot(data[0]["ticks"]/100, [median(w) for w in sliding_window(data[0]["trav_unprod"]/1000,10)], label="s = 0")
    plot(data[2]["ticks"]/100, [median(w) for w in sliding_window(data[2]["trav_unprod"]/1000,10)], label="s = 2")
    plot(data[4]["ticks"]/100, [median(w) for w in sliding_window(data[4]["trav_unprod"]/1000,10)], label="s = 4")
    legend()
    ylim(ymax=9)
    savefig("trav_unprod_nodes_skews_{}.pdf".format(dataset))
    clf()

    skews = sorted(list(data.keys()))

    xlabel("Skew s")
    ylabel("Avg. Query Runtime [ms]")
    plot(skews, [median(data[skew]["query_runtime"][995:1005]) for skew in skews], linestyle="-", marker="o")
    ylim(ymax=35)
    savefig("skew_query_runtime_{}.pdf".format(dataset))
    clf()

    xlabel("Skew s")
    ylabel("Traversed Unproductive Nodes [1k]")
    plot(skews, [median(data[skew]["trav_unprod"][995:1005]/1000) for skew in skews], linestyle="-", marker="o")
    ylim(ymax=4.5)
    savefig("skew_unprod_nodes_{}.pdf".format(dataset))
    clf()
