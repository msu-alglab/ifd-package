#! /usr/bin/env python3
#
# python libs
import time
import argparse
# local imports
import os
import sys
from flows.parser import read_instances
import flows.computation_utils as utils
from flows.ifd import InexactFlowInstance
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
    parser.add_argument('file',
                        help='A .graph file containing the input graph(s).')
    parser.add_argument('confidence_filename',
                        help="Filename of confidence interval file")
    parser.add_argument('confidence_interval', help="Is this a conf int test?")
    parser.add_argument('input_style', help='An input style')
    parser.add_argument('output_file', help='An output filename.')
    parser.add_argument('wide', help='wide experiment or not')
    parser.add_argument('-s', '--source_sink',
                        help='source sink experiment or not', default='True')
    args = parser.parse_args()

    # parse arguments
    graph_file = args.file
    confidence_filename = "confidence_files/" + args.confidence_filename
    conf_interval = args.confidence_interval == 'conf_int_test'
    if conf_interval:
        confidence_level = float(args.confidence_filename.split("_")[0])
    output_file = args.output_file
    og_filename = os.path.basename(graph_file)
    input_style = args.input_style
    filename = graph_file
    wide_str = args.wide
    if wide_str == 'True':
        wide = True
    else:
        wide = False
    source_sink_string = args.source_sink
    if source_sink_string == 'True':
        source_sink = True
    else:
        source_sink = False

    # get dictionary of intervals from file
    if conf_interval:
        f = open(confidence_filename, "rb")
        interval_dict = pickle.load(f)

    # if this is a gill input, create Toboggan-style inputs
    if input_style == 'gill':
        # write .graph and .truth files from path file
        pass
        # todo: remove this option
    truth_file = graph_file.split(".")[0] + ".truth"

    print("Time before entering graph processing loop: {}".format(
            time.time()-overall_start_time))

    results = []

    # Iterate over every graph-instance inside the input file and solve
    print(graph_file)
    for graphdata, index in read_instances(graph_file):
        graph_start_time = time.time()
        graph, graphname, graphnumber = graphdata
        print("Time to read in graph data: {}".format(
                            time.time() - graph_start_time))

        print("########################")
        print("Beginning inexact flow decomposition for graph {}".format(
                    graphname))
        print("This graph is index {}".format(index))
        print("########################")
        # contract in-/out-degree 1 vertices
        # this is where we could make an InexactFlowInstance object
        start_time = time.time()
        ifd = InexactFlowInstance(graph, silent=False)
        if ifd.is_trivial():
            print("Trivial. Skipping this input.\n")
            continue
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

        # set up and find maxflow problem
        start_time = time.time()
        print("Perturbing edges to create a graph with errors.")
        graph.perturb_edges(epsilon, seed)
        if conf_interval:
            graph.get_interval_from_confidence_file(interval_dict)
        else:
            graph.get_interval_from_minflow(wide)
        if source_sink:
            print("Adding new source and sink.")
            graph.add_new_source_sink()
            print("Now, graph is:")
            graph.print_out()
        found_flow = graph.update_flow()
        print("After maxflow to find flow, graph is:")
        graph.print_out()
        print("\nMaxflow approach to find flow success? {}".format(found_flow))
        if not conf_interval:
            # we should always find a flow. exit if not.
            if not found_flow:
                graph.print_out()
                assert(found_flow)
        if found_flow:
            find_feasible_flow_time = time.time()-start_time
            print("Time to find initial flow: {}".
                  format(find_feasible_flow_time))

            # run heuristic 1
            start_time = time.time()
            if graph.get_num_zero_lower_bounds() > 0:
                print("\n>=1 edge wth lower bound 0. Running heuristic 1.")
                heuristic_1_updates = graph.run_heuristic_1()
            else:
                print("\n0 edges with lower bound 0, so skipping heuristic 1.")
                heuristic_1_updates = 0
            time_to_do_heuristic_1 = time.time() - start_time
            print("Time to run heuristic 1: {}".format(time_to_do_heuristic_1))

            start_time = time.time()
            graph.run_greedy_width()
            print("Time to run greedy width: {}".
                  format(time.time()-start_time))

            # get initial solution size
            init_k_pred = len(graph.get_paths())

            # run rebalancing + splice and merge
            print("\nStarting path rebalancing + splice/merge.")
            start_time = time.time()
            graph.path_splice()
            splice_time = time.time() - start_time
            print("Time to rebalance/splice paths: {}".format(splice_time))
            print("\nFinished rebalancing/splicing.")
            graph.print_paths()

            print("\nStarting pairwise rebalancing.")
            start_time = time.time()
            graph.pairwise_rebalance()
            pairwise_rebalancing_time = time.time() - start_time
            print("Time to do pairwise rebalancing: {}".format(
                                pairwise_rebalancing_time))
            print("\nFinished pairwise rebalancing.")
            graph.print_paths()

            print("\nStarting pairwise splicing.")
            start_time = time.time()
            graph.pairwise_splice()
            pairwise_splicing_time = time.time() - start_time
            print("Time to do pairwise splicing: {}".format(
                                        pairwise_splicing_time))
            print("\nFinished pairwise splicing.")
            graph.print_paths()

            # get metrics
            found_k = graph.get_k()
            splices = graph.get_splices()
            overlaps = graph.get_overlap_count()
            rebalances = graph.get_rebalances()
            pairwise_rebalances = graph.get_pairwise_rebalances()
            pairwise_splices = graph.get_pairwise_splices()
            zero_intervals = graph.count_paths_with_zero_intervals()

            # check that solution is valid
            start_time = time.time()
            graph.check_flow()
            graph.check_paths()
            graph.check_conservation_of_flow()
            check_time = time.time()-start_time
            print("Time to check that solution is valid: {}".
                  format(check_time))
        else:
            # set variables to None that did not get set
            init_k_pred = 0
            rebalances = 0
            splices = 0
            overlaps = 0
            pairwise_rebalances = 0
            pairwise_splices = 0
            zero_intervals = 0
            heuristic_1_updates = None
            found_k = None
            splice_time = None
            check_time = None
            num_not_in_interval = None
            time_to_do_heuristic_1 = None
            find_feasible_flow_time = None

        time_to_complete_graph = time.time() - graph_start_time

        # write predicted paths to file
        print("\nWriting predicted paths to .predicted file.")
        predicted_filename = filename.replace(".graph", ".predicted")
        with open(predicted_filename, 'w') as f:
            f.write("# graph number = {} name = {}\n".
                    format(graphnumber, graphname))
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
        wj_sim, k_gt, k_pred = utils.compute_weighted_jaccard(
            predicted_filename, truth_file, index)
        print("Weighted Jaccard Similarity is {}\n".format(wj_sim))

        results.append([str(wj_sim),
                        str(k_gt),
                        str(k_pred),
                        str(init_k_pred),
                        str(rebalances),
                        str(splices),
                        str(overlaps),
                        str(pairwise_rebalances),
                        str(pairwise_splices),
                        str(zero_intervals)])
    print("Overall time: {}".format(time.time()-overall_start_time))

    # write results to file
    f = open(output_file, "w")
    for result in results:
        f.write(",".join(result) + "\n")
