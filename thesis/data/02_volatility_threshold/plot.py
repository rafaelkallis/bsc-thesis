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
    tau = int(search("_tau(?P<tau>.*)_", filename).group("tau"))
    dataset = search("(?P<dataset>(synthetic|real))", filename).group("dataset")
    data = data_synthetic if dataset == "synthetic" else data_real if dataset == "real" else None
    with open(filename) as f:
        csv_reader = reader(f)
        next(csv_reader)
        ticks, timestamps, query_runtime, trav_index, trav_vol, trav_unprod = zip(*csv_reader)
        data[tau] = {
            "ticks": np.array(list(map(int, ticks))),
            "timestamps": np.array(list(map(int, timestamps))),
            "query_runtime": np.array(list(map(float, query_runtime))),
            "trav_index": np.array(list(map(float, trav_index))),
            "trav_vol": np.array(list(map(float, trav_vol))),
            "trav_unprod": np.array(list(map(float, trav_unprod)))
        }

for dataset, data in [("synthetic", data_synthetic), ("real", data_real)]:
    xlabel("Update Operations [1k]")
    ylabel("Query Runtime [ms]")
    plot(data[1]["ticks"]/100, [median(w) for w in sliding_window(data[1]["query_runtime"],10)], label="τ = 1")
    plot(data[5]["ticks"]/100, [median(w) for w in sliding_window(data[5]["query_runtime"],10)], label="τ = 5")
    plot(data[10]["ticks"]/100,[median(w) for w in sliding_window(data[10]["query_runtime"],10)], label="τ = 10")
    legend()
    ylim(ymax=300)
    savefig("query_runtime_taus_{}.pdf".format(dataset))
    clf()

    xlabel("Update Operations [1k]")
    ylabel("Traversed Unproductive Nodes [1k]")
    plot(data[1]["ticks"]/100, [median(w) for w in sliding_window(data[1]["trav_unprod"]/1000,10)], label="τ = 1")
    plot(data[5]["ticks"]/100, [median(w) for w in sliding_window(data[5]["trav_unprod"]/1000,10)], label="τ = 5")
    plot(data[10]["ticks"]/100, [median(w) for w in sliding_window(data[10]["trav_unprod"]/1000,10)], label="τ = 10")
    legend()
    ylim(ymax=60)
    savefig("trav_unprod_nodes_taus_{}.pdf".format(dataset))
    clf()

    taus = sorted(list(data.keys()))

    xlabel("Volatility Threshold τ")
    ylabel("Query Runtime [ms]")
    plot(taus, [median(data[tau]["query_runtime"][995:1005]) for tau in taus], linestyle="-", marker="o")
    ylim(ymax=190)
    savefig("tau_query_runtime_{}.pdf".format(dataset))
    clf()

    xlabel("Volatility Threshold τ")
    ylabel("Traversed Unproductive Nodes [1k]")
    plot(taus, [median(data[tau]["trav_unprod"][995:1005]/1000) for tau in taus], linestyle="-", marker="o")
    ylim(ymax=40)
    savefig("tau_unprod_nodes_{}.pdf".format(dataset))
    clf()
