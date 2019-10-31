import os
import pandas as pd

names=['minflow_jaccard',
       'minflow_gt',
       'minflow_pred',
       "minflow_init_k_pred",
       "minflow_rebalances",
       "minflow_pw_rebalances",
       "minflow_pw_splices",
       "minflow_splices",
       "minflow_overlaps",
       "zero_intervals"]

print("Wide=False")
dfs = []
for f in os.listdir("results/"):
    if 'inexact' in f:
        if f.split('inexact_')[1] == 'out.csv':
            print(f)
            filename = "results/" + f
            data = pd.read_csv(filename,
                names=names)
            dfs.append(data)
df = pd.concat(dfs, axis=1)
print(df.mean())

print("Wide=True")
dfs = []
for f in os.listdir("results/"):
    if 'inexact' in f:
        if f.split('inexact_')[1] == 'out_wide.csv':
            print(f)
            filename = "results/" + f
            data = pd.read_csv(filename,
                names=names)
            dfs.append(data)
df = pd.concat(dfs, axis=1)
print(df.mean())

print("Greedy Width")
dfs = []
for f in os.listdir("results/"):
    if 'gw_out' in f:
        print(f)
        filename = "results/" + f
        data = pd.read_csv(filename, names=['gw_jaccard','gw_gt','gw_pred',
                                         "gw_init_k_pred"])
        dfs.append(data)
df = pd.concat(dfs, axis=1)
print(df.mean())

