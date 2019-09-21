##
# Benchmarking Result Set
#
# Currently just a placeholder for handling data used
# for benchmarking
#
# self.results:		Hash for method name and time spent (score I guess)
# self.data:		Anything. Presumably a list but anything's possible
##
class BenchMarkResultSet():
	##
	# data:		Whatever is appropriate for the Benchmarker
	##
	def __init__(self, data):
		self.results	= {}
		self.data		= data
	##
	# Add a result to the results
	#
	# name:		String name of score's method
	# t:		Whatever. Float in BenchMarkBase. you might override though
	##
	def addResult(self, name, t):
		self.results[name]	= t