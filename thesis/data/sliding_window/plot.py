#!/usr/bin/env python3

from matplotlib import use
use("Agg")
from matplotlib.pyplot import savefig, plot, xlabel, ylabel, clf, legend, ylim, tight_layout, rc
import numpy as np
from csv import reader
from glob import glob
from math import floor
from re import search
from statistics import mean, median

rc("font", size=17, family="serif")
rc("text",usetex=True)

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
    L = int(search("_L(?P<L>.*)$", filename).group("L"))
    dataset = search("(?P<dataset>(synthetic|real))", filename).group("dataset")
    data = data_synthetic if dataset == "synthetic" else data_real if dataset == "real" else None
    with open(filename) as f:
        csv_reader = reader(f)
        next(csv_reader)
        ticks, timestamps, query_runtime, trav_index, trav_vol, trav_unprod = zip(*csv_reader)
        data[L] = {
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
    plot(data[10000]["ticks"]/100, [median(w) for w in sliding_window(data[10000]["query_runtime"],10)], label="L = 10s")
    plot(data[20000]["ticks"]/100, [median(w) for w in sliding_window(data[20000]["query_runtime"],10)], label="L = 20s")
    plot(data[30000]["ticks"]/100,[median(w) for w in sliding_window(data[30000]["query_runtime"],10)], label="L = 30s")
    legend()
    # ylim(ymax=300)
    savefig("query_runtime_Ls_{}.pdf".format(dataset))
    clf()

    xlabel("Update Operations [$\\times 10^3$]")
    ylabel("Unproductive Nodes [$\\times 10^3$]")
    plot(data[10000]["ticks"]/100, [median(w) for w in sliding_window(data[10000]["trav_unprod"]/1000,10)], label="$L=10s$")
    plot(data[20000]["ticks"]/100, [median(w) for w in sliding_window(data[20000]["trav_unprod"]/1000,10)], label="$L = 20s$")
    plot(data[30000]["ticks"]/100, [median(w) for w in sliding_window(data[30000]["trav_unprod"]/1000,10)], label="$L = 30s$")
    legend()
    ylim(ymax=7.5)
    tight_layout()
    savefig("trav_unprod_nodes_Ls_{}.pdf".format(dataset))
    clf()

    Ls = np.array(sorted(list(data.keys())))

    xlabel("Sliding Window of Length L [s]")
    ylabel("Avg. Query Runtime [ms]")
    # plot(Ls/1000, [median(data[L]["query_runtime"][995:1005]) for L in Ls], linestyle="-", marker="o")
    # ylim(ymax=190)
    savefig("L_query_runtime_{}.pdf".format(dataset))
    clf()

    xlabel("Sliding Window Length $L$ [s]")
    ylabel("Unproductive Nodes [$\\times 10^3$]")
    # plot(Ls/1000, [median(data[L]["trav_unprod"][995:1005]/1000) for L in Ls], linestyle="-", marker="o")
    # plot(Ls/1000, [mean(data[L]["trav_unprod"]/1000) for L in Ls], linestyle="-", marker="o")
    plot(Ls/1000, [median(data[L]["trav_unprod"]/1000) for L in Ls], linestyle="-", marker="o")
    ylim(ymax=5.1)
    tight_layout()
    savefig("L_unprod_nodes_{}.pdf".format(dataset))
    clf()
