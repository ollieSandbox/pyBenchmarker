from example_benchmarker import *
##
# Create new Benchmarker: Iterations, list length and list values range
##
benchmarker = ListDupRemoveBenchMark(2000, 1000, 10000)
benchmarker.benchmark()