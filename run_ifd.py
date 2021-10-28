#! /usr/bin/env python3
#
# python libs
import time
import argparse
# local imports
import sys
from flows.parser import read_instances
from flows.ifd import InexactFlowInstance


# Override error message to show help message instead
class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.exit(2)


if __name__ == "__main__":

    overall_start_time = time.time()

    # define arguments
    parser = DefaultHelpParser()
    parser.add_argument('infile', help='A file containing input graph(s).')
    parser.add_argument('--outfile', help='A filename to write stats.')
    args = parser.parse_args()

    # parse arguments
    graph_file = args.infile
    output_file = args.outfile

    results = []

    # Iterate over every graph-instance inside the input file and solve
    predicted_filename = graph_file.replace(".graph", ".predicted")
    with open(predicted_filename, 'w') as fp:
        if output_file:
            fo = open(output_file, 'w')
        for graphdata, index in read_instances(graph_file, exact=False):
            graph_start_time = time.time()
            graph, graphname, graphnumber = graphdata
            print("########################")
            print("Beginning inexact flow decomposition for graph {}".format(
                        graphname))
            print("This graph is index {}".format(index))
            print("########################")
            graph.print_out()
            # contract in-/out-degree 1 vertices
            start_time = time.time()
            ifd = InexactFlowInstance(graph, silent=False)
            if ifd.is_trivial():
                print("Trivial. Skipping this input.\n")
                if output_file:
                    fo.write("1,0\n")
                continue
            print("")

            ifd.solve()

            # write predicted paths to file
            print("\nWriting predicted paths to .predicted file.")
            fp.write(f"# graph number = {graphnumber} name = {graphname}\n")
            paths = ifd.graph.get_paths()
            weights = ifd.graph.get_weights()
            if output_file:
                graph_total_time = time.time() - graph_start_time
                fo.write(f"{len(paths)},{graph_total_time}\n")
            for path, weight in zip(paths, weights):
                node_seq = [graph.source()]
                for arc in path:
                    node_seq.append(graph.arc_info[arc]['destin'])
                fp.write(" ".join([str(x) for x in [weight] + node_seq]))
                fp.write("\n")

            print("Finished instance.\n")

    print("Overall time: {}".format(time.time()-overall_start_time))
    if output_file:
        fo.close()
