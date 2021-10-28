## Inexact Flow Solver

The [original IFD repository](https://github.com/msu-alglab/ifd) contained code that was mixed up in the
experimental pipeline. In this repository, the IFD solver is pulled out into
its own class, `InexactFlowInstance`, in `flows/ifd.py`.

### Requirements

* Python 3
* `numpy`
* `ortools`, [Google's OR package](https://developers.google.com/optimization/install)

Both packages can be installed with `pip`.

### Running on a file

The script `run_ifd.py` will read a file of interval graphs and solve them. The
optional argument `--outfile` specifies a file to write size of solution and
time to solve for each instance. For example:

```
python run_ifd.py human_annotation_interval/1.graph --outfile out.txt
```
