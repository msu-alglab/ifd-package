import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_file')

args = parser.parse_args()
input_file = args.input_file

# run confidence interval experiments

conf_files = [
#    "0.70_confidence.pkl",
    "0.80_confidence.pkl",
#    "0.85_confidence.pkl",
#    "0.90_confidence.pkl",
    "0.95_confidence.pkl",
#    "0.99_confidence.pkl"
    ]

if not os.path.exists('results'):
        os.makedirs('results')

# run all conf level experiments
for conf_file in conf_files:
    print(conf_file)
    conf = conf_file.split("_")[0]
    to_run = "python ../../inexact_flows.py data/" + input_file + \
    " " + conf_file + \
    " conf_int_test not_gill " + "results/" + input_file + conf + "out.csv True"
    os.system(to_run)
