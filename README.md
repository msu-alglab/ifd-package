# ifd-experiments
Code to run experiments on Inexact Flow Decomposition for finding RNA
transcripts in splice graphs.

Data used in these experiments is available for download TODO.

There are three experiments that can be run. One uses confidence intervals to
determine the intervals on edges, one uses a minimum-cost flow to determine
intervals on edges, and the third removes known edges to sources and sinks,
considers all nodes as possible sources and sinks, and then uses confidence
intervals on edges.

To run an experiment, download all human data from
https://zenodo.org/record/1460998#.XbsQU-dKgWp in data/rnaseq/human and
put it in the data directory. Then, run experimental_pipeline.py to generate
results in the results folder. Finally, run analyze_output.py to aggregate
results and generate statistics.
