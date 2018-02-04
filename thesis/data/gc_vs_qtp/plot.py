#!/usr/bin/env python3

from matplotlib import use
use("Agg")
from matplotlib.pyplot import savefig, plot, xlabel, ylabel, clf, legend, ylim, rc, tight_layout
import numpy as np
from csv import reader
from glob import glob
from math import floor
from re import search
from statistics import mean, median
from collections import defaultdict

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

data = {"synthetic": {"gc": dict(), "qtp": dict()}, "real": {"gc": dict(), "qtp": dict()}}

for filename in filenames:
    upt = int(search("(?P<upt>[0-9]+)", filename).group("upt"))
    dataset = search("(?P<dataset>(synthetic|real))", filename).group("dataset")
    func = search("(?P<func>(gc|qtp))", filename).group("func")
    
    with open(filename) as f:
        csv_reader = reader(f)
        next(csv_reader)
        ticks, timestamps, query_runtime, trav_index, trav_vol, trav_unprod = zip(*csv_reader)
        
        # ticks = np.array(list(map(int, ticks)))
        # timestamps = np.array(list(map(int, timestamps)))
        query_runtime = np.array(list(map(int, query_runtime)))
        # trav_index = np.array(list(map(float, trav_index)))
        # trav_vol = np.array(list(map(float, trav_vol)))
        # trav_unprod = np.array(list(map(float, trav_unprod)))

        data[dataset][func][upt] = query_runtime

        
for dataset in ["synthetic", "real"]:
    for func in ["gc", "qtp"]:
        X = sorted(data[dataset][func].keys())
        Y = [mean(data[dataset][func][x]) for x in X]

        plot(X,Y,label=func.upper(), linestyle="-",marker="o")

    xlabel("Updates per Query")
    ylabel("Avg. Query Runtime [ms]")
    ylim(ymax=80)
    legend()
    tight_layout()
    savefig("gc_vs_qtp_{}.pdf".format(dataset))
    savefig("gc_vs_qtp_{}.eps".format(dataset))
    clf()
    
    for func in ["gc", "qtp"]:
        keys = sorted(data[dataset][func].keys())
        X = [1/(len(data[dataset][func][k])/500) for k in keys]
        Y = [mean(data[dataset][func][k]) for k in keys]

        plot(X,Y,label=func.upper(), linestyle="-",marker="o")

    xlabel("Query Period [s]")
    ylabel("Avg. Query Runtime [ms]")
    ylim(ymax=80)
    legend()
    tight_layout()
    savefig("gc_vs_qtp_qps_{}.pdf".format(dataset))
    clf()

        # data[upt] = {
            # "ticks": np.array(list(map(int, ticks))),
            # "timestamps": np.array(list(map(int, timestamps))),
            # "query_runtime": np.array(list(map(float, query_runtime))),
            # "trav_index": np.array(list(map(float, trav_index))),
            # "trav_vol": np.array(list(map(float, trav_vol))),
            # "trav_unprod": np.array(list(map(float, trav_unprod)))
        # }

# for dataset, data in [("synthetic", data_synthetic), ("real", data_real)]:
    # xlabel("Update Operations [1k]")
    # ylabel("Avg. Query Runtime [ms]")
    # plot(data[5000]["ticks"]/100, [median(w) for w in sliding_window(data[5000]["query_runtime"],10)], label="5s")
    # plot(data[50000]["ticks"]/100, [median(w) for w in sliding_window(data[50000]["query_runtime"],10)], label="50s")
    # legend()
    # ylim(ymax=30)
    # savefig("query_runtime_periodicity_{}.pdf".format(dataset))
    # clf()

    # xlabel("Time [min]")
    # ylabel("Unproductive Nodes [$\\times 10^3$]")
    # plot(data[1]["ticks"]/100, [median(w) for w in sliding_window(data[1]["trav_unprod"]/1000,10)], label="1 update per query")
    # plot(data[10]["ticks"]/100, [median(w) for w in sliding_window(data[10]["trav_unprod"]/1000,10)], label="10 updates per query")
    # plot(data[1]["timestamps"]/60000, [median(w) for w in sliding_window(data[1]["trav_unprod"]/1000,10)], label="1  update per query")
    # plot(data[10]["timestamps"]/60000, [median(w) for w in sliding_window(data[10]["trav_unprod"]/1000,10)], label="10 updates per query") 
    # plot(data[20]["timestamps"]/60000, [median(w) for w in sliding_window(data[20]["trav_unprod"]/1000,10)], label="20 updates per query")
    # legend()
    # ylim(ymax=12)
    # tight_layout()
    # savefig("trav_unprod_nodes_upt_{}.pdf".format(dataset))
    # clf()

    # # first_tick = 250 
    # upts = np.array(sorted(list(data.keys())))

    # # xlabel("Updates per Query")
    # # ylabel("Avg. Query Runtime [ms]")
# # #    plot(periods, [median(data[p]["query_runtime"][995:1005]) for p in periods], linestyle="-", marker="o")
    # # plot(periods/1000, [mean(data[p]["query_runtime"][first_tick:]) for p in periods], linestyle="-", marker="o")
    # # ylim(ymax=34)
    # # savefig("periodicity_query_runtime_{}.pdf".format(dataset))
    # # clf()

    # xlabel("Updates per Query")
    # ylabel("Unproductive Nodes [$\\times 10^3$]")
# #    plot(periods, [median(data[p]["trav_unprod"][995:1005]/1000) for p in periods], linestyle="-", marker="o")
    # # plot(upts, [mean(data[utp]["trav_unprod"][695:705]/1000) for utp in upts], linestyle="-", marker="o")
    # plot(upts, [mean(data[utp]["trav_unprod"]/1000) for utp in upts], linestyle="-", marker="o")
    # ylim(ymax=6)
    # tight_layout()
    # savefig("upt_unprod_nodes_{}.pdf".format(dataset))
    # clf()
