##
# Native
##
from random import randint
from itertools import groupby
##
# Library
##
from lib.benchmark_base import BenchMarkerBase
from lib.print_helper import PrintHelper
##
# EXAMPLE Benchmark class: Remove duplicate adjacent entries in a list
#
# Add methods which iterate over a list and check to see if an entry
# is identical "==" to its neighbor. Remove if it is.
## 
class ListDupRemoveBenchMark(BenchMarkerBase):
	##
	# iterations:		Int number of iterations (pass to super)
	# listLen:			Int number of items in each data entry list
	# rng:				Int Range limit for randint for random data
	#					list values. 0..rng
	##
	def __init__(self, iterations, listLen, rng):
		super().__init__(iterations)
		self.listLen	= listLen
		self.range		= rng
	##
	# OVERRIDDEN: Generate data for benchmarking
	#
	# Output:	List of Int Lists
	##
	def generateData(self):
		output 			= []
		for x in range(self.iterations):
			output.append([randint(0, self.range) for x in range(self.listLen)])
		return output
	##
	# Lambda type loop and check
	##
	def loop(self, input):
		return [v for i, v in enumerate(input) if i == 0 or v != input[i-1]]
	##
	# Enumerate iteration
	##
	def enumerate(self, input):
		previous_value = None
		new_lst = []
		for elem in input:
		   if elem != previous_value:
			   new_lst.append(elem)
			   previous_value = elem
		return new_lst
	##
	# Lazy enumeration:
	#
	# Unlike enumerate this tracks the entries which should be
	# removed's indices. If any items are flagged for removal
	# they are popped directly from the input List.
	##
	def lazyEnumerate(self, input):
		previous_value = None
		new_lst = []
		for i, elem in enumerate(input):
		   if elem != previous_value:
			   new_lst.append(i)
			   previous_value = elem
		if len(new_lst) > 0:
			i = len(new_lst) - 1
			while i > 0:
				input.pop(new_lst[i])
				i -= 1
		return input
	##
	# Subscripted access using while loop. Incremented with +=
	##
	def subscripted(self, input):
		previous_value 	= None
		new_lst 		= []
		l				= len(input)
		i 				= 0
		while i < l:
			v = input[i]
			if v != previous_value:
			   new_lst.append(v)
			   previous_value = v
			i += 1
		return new_lst
	##
	# Lazy subscripted: As subscripted but inline
	#
	# Unlike enumerate this tracks the entries which should be
	# removed's indices. If any items are flagged for removal
	# they are popped directly from the input List.
	##
	def lazySubscription(self, input):
		previous_value 	= None
		new_lst 		= []
		l				= len(input)
		i 				= 0
		while i < l:
			v =	input[i]
			if v == previous_value:
			   new_lst.append(i)
			   previous_value = v
			i += 1
		if len(new_lst) > 0:
			i = len(new_lst) - 1
			while i > 0:
				input.pop(new_lst[i])
				i -= 1
		return input
	##
	# Iterate using the range(x) to generate enumeration list
	##
	def ranged(self, input):
		previous_value 	= None
		new_lst 		= []
		for x in range(len(input)):
			v = input[x]
			if v != previous_value:
				new_lst.append(v)
				previous_value = v	
		return new_lst
	##
	# Itertools groupby removal
	##
	def itertools(self, input):
		return [i[0] for i in groupby(input)]	