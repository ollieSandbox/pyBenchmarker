import collections 
##
# Some pretty print helpers
##
class PrintHelper():
	##
	# Print hash to formatted table
	#
	# hash:		Hash key->value
	# sortKeys:	Boolean sort keys by values?
	# title:	String title for table
	##
	@staticmethod
	def tableHash(hash, sortKeys=True, title=False):
		##
		# Do keys and determine padding sizes
		##
		hash 	= hash if not sortKeys else collections.OrderedDict(sorted(hash.items(), key=lambda kv: kv[1]))
		keyLen 	= 0
		valLen	= 0
		for key, val in hash.items():
			keyLen = len(key) if len(key) > keyLen else keyLen
			valLen = len(str(val)) if len(str(val)) > valLen else valLen
		totLen	= keyLen + valLen + 5
		##
		# Add title if requested
		##
		if title:
			print(__class__.padValue("", totLen + 2, filler="="))
			print(__class__.midPad(title, totLen, filler="#"))	
			print(__class__.padValue("", totLen + 2, filler="="))
		##
		# Print table
		##
		print(__class__.padValue("", totLen + 2, filler="-"))
		print("%s    %s" %(__class__.padValue("Header", keyLen), __class__.padValue("Time", keyLen)))
		print(__class__.padValue("", totLen + 2, filler="-"))
		for key, value in hash.items():
			print("%s    %s" %(__class__.padValue(key, keyLen), __class__.padValue(hash[key], keyLen)))
		print(__class__.padValue("", totLen + 2, filler="-"))
	##
	# Pad a string to a specific length
	#
	# value:	Anything (will be converted to String)
	# padSize:	Int expected length of output String
	# filler:	String padding character(s)
	##
	@staticmethod
	def padValue(value, padSize, filler=" "):
		value = str(value)
		while len(value) < padSize:
			value += filler
		return value
	##
	# Center-pad a string. (as padValue but center align)
	#
	# value:	Anything (will be converted to String)
	# padSize:	Int expected length of output String
	# filler:	String padding character(s)
	##
	@staticmethod
	def midPad(value, padSize, filler=" "):
		value	= " %s " %(str(value))
		while len(value) < padSize:
			value = "%s%s%s" %(filler, value, filler)
		return value