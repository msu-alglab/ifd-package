## Inexact Flow Solver

The [original IFD repository](https://github.com/msu-alglab/ifd) contained code that was mixed up in the
experimental pipeline. In this repository, the IFD solver is pulled out into
its own class, `InexactFlowInstance`, in `flows/ifd.py`.

The script `run_ifd.py` will read a file of interval graphs and solve them. For
example:

```
python run_ifd.py interval_testdata/toboggan_test.graph
```
