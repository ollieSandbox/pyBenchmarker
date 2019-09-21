##
# Native
##
from inspect import getargspec
from copy import deepcopy
from time import time
##
# Library
##
from .print_helper import PrintHelper
from .benchmark_result_set import BenchMarkResultSet
##
# Benchmarker Abstract class
#
# HOW TO USE:
#	- Create inheriting class. This is not a standard class
#  	  and must be extended or inherited from. SomeClassName(BenchMarkerBase)
#	- Always pass a number of iterations to constructor. You can replace the 
#	  constructor with whatever as long as it passes the number of iterations
# 	  to the super constructor by using this in your __init__
#		super().__init__(iterations)
#	- To benchmark a method simply add any method which takes one parameter
#	  which should be the a single evaluation's data. E.g:
#		isInRange(self, input), sortByKey(self, input) etc
#	  IMPORTANT: Methods MUST NOT include "__" or "BM"
#	  IMPORTANT: If the method requires a deep clone of the input data
#	  			 add "lazy" to the name
#				 TODO: Is lazy a reasonable name for everything here?
#
# MUTABLE method supported - currently labeled as "lazy"
#
# WARNING:	Methods cannot be standard named. E.g: "range"
##
class BenchMarkerBase():
	##
	# iterations:		Number of steps per benchmark
	##
	def __init__(self, iterations):
		self.iterations	= iterations
	##
	# ABSTRACT Generate test data
	#
	# This method should return the same number of entries as 
	# expected benchmark iterations.
	#
	# WARNING: Default behavior will reject anything that doesn't have
	# a data set which doesn't have BOTH a len() [__len__] method and#
	# an equal number of iterations expected and entries. To change this
	# override the BMdataVerify method
	##
	def generateData(self):
		raise "BenchMarkerBase::generateData must be overridden"
	##
	# Get list of methods for benchmarking
	#
	# This harasses the object definition and finds the methods the creator
	# wants to benchmark.
	#
	# NOTES:
	#	- Doesn't retrieve methods beginning with "BM"
	#	- Doesn't retrieve magic methods (anything "__")
	#	- Doesn't retrieve the abstract "generateData"
	#	- Doesn't retrieve the "benchmark" method"
	#
	# WARING!!!!!!
	#	- DO NOT OVERRIDE THIS METHOD
	##
	def BMgetBenchMarkMethods(self):
		return [func for func in dir(self.__class__) 
					if callable(getattr(self.__class__, func)) 
					and str(func) != "benchmark"
					and str(func) != "generateData"
					and str(func)[0:2] != "BM"
					and str(func)[0:2] != "__"]
	##
	# VIRTUAL: Verify data before running benchmarks
	#
	# This will check the data has a __len__ method and the 
	# number of data entries matches the iterations.
	#
	# Can be overridden so long as the method takes the data
	# as a parameter. 
	##
	def BMVerifyData(self, data):
		if "__len__" not in (dir(data)):
			print("ERROR: Data doesn't contain a __len__ method for verification")
			exit()
		if len(data) != self.iterations:
			print("ERROR: Data and iterations are not the same length")
			exit()
	##
	# FINAL: Verify methods only expect one (data parameter
	#
	# Currently MUST NOT be overridden though it could be in
	# the future.
	##
	def BMVerifyMethods(self, methods):
		##
		# Loop over methods List[object] and check arity
		##
		results 			= {}
		failedVerification	= False
		for method in methods:
			objMethod	= getattr(self, str(method))
			res			= len(getargspec(objMethod).args) - 1 == 1
			results[str(method)] 	= res
			if not res:
				failedVerification	= True
		PrintHelper.tableHash(results, title="BM Verify method arity")
		##
		# Crash and burn if verification failed. There's no graceful
		# exit possible.
		##
		if failedVerification:
			print("ERROR! One or more methods' arity is not 1")
			exit()
		return 
	##
	# FINAL: The method that does the actual benchmarking.
	#
	# Not to be confused with "benchmark" this method is 
	# invisible to you! Don't touch it and just trust it does
	# what it's meant to do, hopefully.
	##
	def BMBenchmark(self, methods, data):
		##
		# Benchmark each method
		##
		bmResultSet		= BenchMarkResultSet(data)
		for method in methods:
			##
			# Get actual instance method form this instance
			##
			objMethod	= getattr(self, str(method))
			##
			# Deep clone data if the method is "lazy" or mutates inputs rather
			# than producing safe outputs
			##
			inputData	= data if "lazy" not in str(method) else deepcopy(data)
			t 			= time()
			for entry in inputData:
				objMethod(entry)
			endTime 	= time() - t
			bmResultSet.addResult(str(method), endTime)
		return bmResultSet
	##
	# Main benchmark call
	#
	# This is where the magic happens. Construct a benchmark test
	# and kicks it off. Verifies (kind of) methods before going to
	# town on the benchmarking.
	#
	# NOTES:
	#	- Methods found dynamically
	#	- Other than iterations, your data can reference anything in
	#	  your constructor
	##
	def benchmark(self):
		##
		# Prep custom data and get methods
		##
		data			= self.generateData()
		methods			= self.BMgetBenchMarkMethods()
		##
		# Verify methods
		##
		self.BMVerifyMethods(methods)
		##
		# Do benchmarking
		##
		print("Benchmarking %s methods with %s iterations" %(str(len(methods)), str(self.iterations)))
		bmResultSet = self.BMBenchmark(methods, data)
		##
		# Print results
		##
		PrintHelper.tableHash(bmResultSet.results, sortKeys=True, title="Benchmark results")
