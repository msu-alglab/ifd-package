def create_graph_file(filename):
    """Read in a file provided by Gill and write the .graph file expected
    by Catfish, Toboggan, and IFD solver"""
    edges = dict()
    vert_set = set()
    # read lines of file to get unique verts and edges and weights
    with open(filename) as f:
        f.readline()
        for line in f:
            # every path starts at 0 and ends at t
            path = ['0'] + line.split("c(")[1].split(")")[0].split(", ") \
                                                    + ['t']
            weight = int(line.split(";")[-1].strip())
            for i in range(len(path) - 1):
                f = path[i]
                to = path[i+1]
                vert_set.add(f)
                vert_set.add(to)
                if (f, to) in edges:
                    edges[(f, to)] += weight
                else:
                    edges[(f, to)] = weight
    # write edges and values to file
    graph_file = filename.split(".")[0] + ".graph"
    f = open(graph_file, "w")
    f.write("# graph number = 0 name = graph_from_gill_file\n")
    f.write("{}\n".format(len(vert_set)))
    # compute a value for t
    t = max([int(x) for x in vert_set - set(['t'])]) + 1
    for edge in edges:
        start = edge[0]
        destin = edge[1]
        # if this edge goes to t, replace with the t value
        if destin == 't':
            destin = t
        if edges[edge] >0 :
            f.write("{} {} {}\n".format(
                start,
                destin,
                edges[edge])
                )


def create_truth_file(filename):
    """Create a .truth file from Gill data."""
    paths = []
    weights = []
    vert_set = set()
    # read lines of file to get unique verts and edges and weights
    with open(filename) as f:
        f.readline()
        for line in f:
            path = ['0'] + line.split("c(")[1].split(")")[0].split(", ")
            weight = int(line.split(";")[-1].strip())
            for vert in path:
                vert_set.add(vert)
            if weight > 0:
                paths.append(path)
                weights.append(weight)
    # write edges and values to file
    t = max([int(x) for x in vert_set]) + 1
    print(t)
    # add t to all paths
    for path in paths:
        path.append(str(t))

    truth_file = filename.split(".")[0] + ".truth"
    f = open(truth_file, "w")
    f.write("# graph number = 0 name = graph_from_gill_file\n")
    for path, weight in zip(paths, weights):
        f.write("{} {}\n".format(
            weight, ' '.join(path))
            )
