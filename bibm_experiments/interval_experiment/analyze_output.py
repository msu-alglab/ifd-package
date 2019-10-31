import os
import pandas as pd

conf_files = [
    "0.70_confidence.pkl",
    "0.80_confidence.pkl",
    "0.85_confidence.pkl",
    "0.90_confidence.pkl",
    "0.95_confidence.pkl",
    "0.99_confidence.pkl"
    ]

dfs = []
for conf_file in conf_files:
    print("conf file is {}".format(conf_file))
    conf = conf_file.split("_")[0]
    this_conf_dfs = []
    for f in os.listdir("results"):
        # read in this file if it's an output file for this conf
        if conf in f:
            print(f)
            filename = "results/" + f
            data = pd.read_csv(filename,
                names=[conf+'jaccard',
                conf+'k_gt',
                conf+'pred',
                conf+"init_k_pred",
                conf+"num_rebalances",
                conf+"num_pw_rebalances",
                conf+"num_pw_splices",
                conf+"num_splices",
                conf+"num_overlaps",
                conf+"zero_intervals"])
            this_conf_dfs.append(data)
    conf_df = pd.concat(this_conf_dfs)
    conf_df = conf_df.reset_index(drop=True)
    dfs.append(conf_df)
data = pd.concat(dfs, axis=1)
total_graphs = data.shape[0]
props = data.groupby('0.80k_gt')[['0.80jaccard']].count()/total_graphs
props.columns = ["Prop. of total"]
print()

for conf_file in conf_files:
    conf = conf_file.split("_")[0]
    filtered_df = data[data[conf+'pred'] != 0]
    print("Analyzing {} conf.".format(conf))
    print("{} successes for {} proportion of total".format(
        filtered_df.shape[0],
        filtered_df.shape[0]/total_graphs))

    avg_jaccard = filtered_df[conf+'jaccard'].mean()
    avg_num_paths = filtered_df[conf+'pred'].mean()
    avg_init_k_pred = filtered_df[conf+'init_k_pred'].mean()
    avg_num_rebalances = filtered_df[conf+'num_rebalances'].mean()
    avg_num_pw_rebalances = filtered_df[conf+'num_pw_rebalances'].mean()
    avg_num_pw_splices = filtered_df[conf+'num_pw_splices'].mean()
    avg_num_splices = filtered_df[conf+'num_splices'].mean()
    avg_overlaps = filtered_df[conf+'num_overlaps'].mean()
    print("{} avg jac".format(avg_jaccard))
    print("{} avg num paths".format(avg_num_paths))
    print("{} avg init k pred".format(avg_init_k_pred))
    print("{} avg num rebalances".format(avg_num_rebalances))
    print("{} avg num pairwise rebalances".format(avg_num_pw_rebalances))
    print("{} avg num pairwise splices".format(avg_num_pw_splices))
    print("{} avg num splices".format(avg_num_splices))
    print("{} avg num overlaps".format(avg_overlaps))
#    print("by k:")
    # make a dataframe of all info
    means = filtered_df.groupby('0.80k_gt')[[conf+'jaccard',
        conf+'pred',
        conf+'init_k_pred',conf+'num_rebalances',conf+'num_pw_rebalances',
        conf+'num_pw_splices',
        conf+'num_splices',conf+'num_overlaps']].mean()
    counts = filtered_df.groupby('0.80k_gt')[[conf+'jaccard']].count()
    counts.columns = ["count"]
    counts["prop"] = counts["count"]/filtered_df.shape[0]
#    print(pd.concat([means, counts], axis=1))
    merged = props.merge(means, left_index=True, right_index=True, how='left')\
        .fillna(0)
    weighted_jac = sum([x*y for (x,y) in zip(merged['Prop. of total'],
        merged[conf+'jaccard'])])
    weighted_k = sum([x*y for (x,y) in zip(merged['Prop. of total'],
        merged[conf+'pred'])])
    weighted_init = sum([x*y for (x,y) in zip(merged['Prop. of total'],
        merged[conf+'init_k_pred'])])
    weighted_reb = sum([x*y for (x,y) in zip(merged['Prop. of total'],
        merged[conf+'num_rebalances'])])
    weighted_pw_reb = sum([x*y for (x,y) in zip(merged['Prop. of total'],
        merged[conf+'num_pw_rebalances'])])
    weighted_pw_spl = sum([x*y for (x,y) in zip(merged['Prop. of total'],
        merged[conf+'num_pw_splices'])])
    weighted_splices = sum([x*y for (x,y) in zip(merged['Prop. of total'],
        merged[conf+'num_splices'])])
    weighted_overlaps = sum([x*y for (x,y) in zip(merged['Prop. of total'],
        merged[conf+'num_overlaps'])])
    print('{} weighted jac'.format(weighted_jac))
    print('{} weighted pred'.format(weighted_k))
    print('{} weighted init pred'.format(weighted_init))
    print('{} weighted rebalances'.format(weighted_reb))
    print('{} weighted pw rebalances'.format(weighted_pw_reb))
    print('{} weighted pw splices'.format(weighted_pw_spl))
    print('{} weighted splices'.format(weighted_splices))
    print('{} weighted overlaps'.format(weighted_overlaps))
    print()
