#!/usr/bin/env python3

from matplotlib import use, get_backend
use("AGG")
from matplotlib.pyplot import savefig, figure, plot, xlabel, ylabel, clf, legend, ylim, rc, tight_layout
import numpy as np
from math import floor
from statistics import mean, median

rc("font", size=17, family="serif")
rc("text", usetex=True)

fig = figure()
ax = fig.add_subplot(111)
ax.set_xlabel("Query Period [s]")
ax.set_ylabel("Unproductive Nodes")
ax.set_xticklabels([])
ax.set_yticklabels([])
fig.tight_layout()
fig.savefig("model_empty.eps")

ax.plot([0,10],[5,5],label="GC")
ax.legend()
fig.tight_layout()
fig.savefig("model_gc.eps")

ax.plot([0,10],[0,10],label="QTP")
ax.legend()
fig.tight_layout()
fig.savefig("model_gc_qtp.eps")

ax.plot([5.1,5.5],[4.8,4],"k-",linewidth=.5, alpha=.8)
ax.text(5.6,3.3, "$2 \\cdot T_{GC}$", alpha=.8)
fig.savefig("model_gc_qtp_equilibrium.eps")

X = np.arange(0,5,.001)
# X_queries_gc = np.arange(.5,4.5,1)
# Y_queries_gc = np.empty(5)
# Y_queries_gc.fill(1)
# X_queries_qtp = np.arange(0,5,.5)
# Y_queries_qtp = np.empty(10)
# Y_queries_qtp.fill(1)

def gc_saw(X):
    return [(x - floor(x)) for x in X]

def qtp_saw(X):
    return [(2*x - floor(2*x)) for x in X]

fig_saw = figure()
ax_gc = fig_saw.add_subplot(211)
ax_gc.set_title("GC")
# ax_gc.set_xlabel("Query Period [s]")
ax_gc.set_ylabel("\\footnotesize Unproductive Nodes")
ax_gc.set_xticklabels([])
ax_gc.set_yticklabels([])
ax_gc.plot(X, gc_saw(X))
ax_gc.plot([0,5],[.5,.5],"k-",linewidth=.5,alpha=.5,linestyle=":")
ax_gc.text(0,.5, "$u_{GC}$")
ax_qtp = fig_saw.add_subplot(212)
ax_qtp.set_title("QTP")
ax_qtp.set_xlabel("\\footnotesize Update Operations")
ax_qtp.set_ylabel("\\footnotesize Unproductive Nodes")
ax_qtp.set_xticklabels([])
ax_qtp.set_yticklabels([])
ax_qtp.set_ylim(top=2)
ax_qtp.plot(X, qtp_saw(X))
ax_qtp.plot([0,5],[1,1],"k-",linewidth=.5,alpha=.5,linestyle=":")
ax_qtp.text(0,1, "$u_{QTP}$")
fig_saw.tight_layout()
fig_saw.savefig("model_gc_qtp_saw.eps")
