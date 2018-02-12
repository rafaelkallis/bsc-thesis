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
data = dict()

for filename in filenames:
    skew = float(search("_skew(?P<skew>[0-9.]*)$", filename).group("skew"))
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


skews = sorted(list(data.keys()))

xlabel("Skew $s$")
ylabel("Unproductive Nodes [$\\times 10^3$]")
plot(skews, [mean(data[skew]["trav_unprod"]/1000) for skew in skews], linestyle="-", marker="o")
ylim(ymax=2.5)
tight_layout()
savefig("skew_unprod_nodes.pdf")
savefig("skew_unprod_nodes.eps")
clf()
