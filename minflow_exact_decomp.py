#! /usr/bin/env python3
#
# python libs
import time
import argparse
# local imports
import os
import sys
from flows.parser import read_instances
from flows.parse_gill_output import create_graph_file
from flows.parse_gill_output import create_truth_file
from flows.computation_utils import *
import pickle


# Override error message to show help message instead
class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.exit(2)


if __name__ == "__main__":

    overall_start_time = time.time()

    # set epsilon
    epsilon = 0.05
    # set random seed for perturbing edges
    seed = 1

    # define arguments
    parser = DefaultHelpParser()
    parser.add_argument('file', help='A .graph file containing the input graph(s).')
    parser.add_argument('output_file', help='An output filename.')
    args = parser.parse_args()

    # parse arguments
    graph_file = args.file
    output_file = args.output_file
    og_filename = os.path.basename(graph_file)
    filename = graph_file

    truth_file = graph_file.split(".")[0] + ".truth"

    print("Time before entering graph processing loop: {}".format(
            time.time()-overall_start_time))

    results = []

    # Iterate over every graph-instance inside the input file and solve
    print("At start of graph processing loop")
    print(graph_file)
    for graphdata, index in read_instances(graph_file):
        print("This index {}".format(index))
        graph_start_time = time.time()
        graph, graphname, graphnumber = graphdata
        print("Time to read in graph data: {}".format(
                            time.time() - graph_start_time))

        print("########################")
        print("Beginning exact flow decomposition for graph {}".format(
                    graphname))
        print("########################")
        # contract in-/out-degree 1 vertices
        start_time = time.time()
        reduced, mapping = graph.contracted()
        print("Time to contract graph: {}".format(time.time() - start_time))
        # reduced is the graph after contractions;
        if len(reduced) <= 1:
            print("Trivial. Skipping this input.\n")
            continue

        print("")

        # record size of graph
        n_input = len(graph)
        m_input = len(list(graph.edges()))


        # get flow
        start_time = time.time()
        graph.perturb_edges(epsilon, seed)
        graph.get_weight_from_minflow()

        start_time = time.time()
        graph.run_greedy_width()
        print("Time to run greedy width: {}".format(time.time()-start_time))

        # get initial solution size
        init_k_pred = len(graph.get_paths())

        time_to_complete_graph = time.time() - graph_start_time

        # write predicted paths to file
        print("\nWriting predicted paths to .predicted file.")
        predicted_filename = filename.replace(".graph", ".predicted")
        with open(predicted_filename, 'w') as f:
            f.write("# graph number = {} name = {}\n".format(graphnumber, graphname))
            paths = graph.get_paths()
            weights = graph.get_weights()
            for path, weight in zip(paths, weights):
                node_seq = [graph.source()]
                for arc in path:
                    node_seq.append(graph.arc_info[arc]['destin'])
                f.write(" ".join([str(x) for x in [weight] + node_seq]))
                f.write("\n")

        print("Finished instance.\n")

        # compute weighted jaccard
        wj_sim, k_gt, k_pred = compute_weighted_jaccard(predicted_filename, truth_file,
                                                        index)
        print("Weighted Jaccard Similarity is {}\n".format(wj_sim))
        results.append([str(wj_sim), str(k_gt), str(k_pred), str(init_k_pred)])
    print("Overall time: {}".format(time.time()-overall_start_time))

    #write results to file
    f = open(output_file, "w")
    for result in results:
        f.write(",".join(result) + "\n")
