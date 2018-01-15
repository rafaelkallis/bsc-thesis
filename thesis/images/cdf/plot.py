#!/usr/bin/env python3

from matplotlib import use
use("Agg")
from matplotlib.pyplot import savefig, plot, xlabel, ylabel, clf, legend, ylim, xscale, text, axhline, rc, tight_layout
import numpy as np
from csv import reader
from glob import glob
from math import floor, log
from re import search
from statistics import mean, median

rc("font", size=17, family="serif")
rc("text", usetex=True)

def memo(func):
    cache = dict()
    def _(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return _

harmonic_number = memo(lambda n,m: sum((1/(k**m)) for k in range(1,n+1)))
zipf_cdf = memo(lambda k,N,s: (harmonic_number(k,s) / harmonic_number(N,s)))

N_synthetic = 500000
N_real = 680000

skews = [0, 0.5, 1, 1.5, 2]

def log_range(start,stop):
    i = start
    while i < stop:
        yield i
        i = floor(i * 1.6) + 1
    yield stop

s_label = {
        0: "0",
        0.5: "\\frac{1}{2}",
        1: "1",
        1.5: "\\frac{3}{2}",
        2: "2"
    }

for s in skews:
    plot(list(log_range(1,N_synthetic)),[zipf_cdf(k,N_synthetic,s) for k in log_range(1,N_synthetic)],label="$s = {}$".format(s_label[s]))

xscale("log")
legend()
xlabel("Nodes")
ylabel("Zipf CDF")
axhline(0.8,linestyle=":")
tight_layout()
savefig("cdf_synthetic.pdf")
clf()

for s in skews:
    plot(list(log_range(1,N_real)),[zipf_cdf(k,N_real,s) for k in log_range(1,N_real)],label="$s = {}$".format(s_label[s]))

xscale("log")
legend()
xlabel("Nodes")
ylabel("Zipf CDF")
axhline(0.8,linestyle=":")
tight_layout()
savefig("cdf_real.pdf")
clf()
