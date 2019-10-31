import os
import pandas as pd
import argparse

# run mincost flow interval experiment

parser = argparse.ArgumentParser()
parser.add_argument('input_file')

args = parser.parse_args()
input_file = args.input_file

if not os.path.exists('results'):
        os.makedirs('results')

to_run = "python ../../inexact_flows.py data/" + input_file + " placeholder mincost" + \
    " not_gill results/" + input_file + "inexact_out.csv False -s False"
os.system(to_run)

to_run = "python ../../inexact_flows.py data/" + input_file + " placeholder mincost" + \
    " not_gill results/" + input_file + "inexact_out_wide.csv True -s False"
os.system(to_run)

to_run = "python ../../minflow_exact_decomp.py data/" + input_file + \
    " results/" + input_file + "gw_out.csv"
os.system(to_run)
