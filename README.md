# pyBenchmarker
Generic benchmarking class. Simple and quick benchmarker creation. Support inline input data modifications (see "lazy" section)

This class is set up to figure out what methods the user wants to benchmark and runs benchmark test for each. Straightforward extension, just extned the base class, add a "generateData" method and any methods you want to benchmark.


Eg.

```
class SomeBenchMark(BenchMarkBase):
  ##
  # Abstract method must be overwritten at some point.
  #
  # output: Anything with a __len__ method defined
  ##
  def generateData(self):
    return[list(x) for x in range(self.iterations)]
   ##
   # Random example benchmark method. Will be collected by the preprocessing
   ##
  def allItemsAreOne(self, inputData):
    for x in inputData:
      if x is not 1:
        return False
    return True
   ##
   # Another random example benchmark method. Will be collected by the preprocessing
   ##
  def allItemsAreModTwo(self, inputData):
    for x in inputData:
      if 2 + x % 2 is not 0:
        return False
    return True
```
Or something to that effect. Check "example_benchmarker.py" for a better example

**Getting it running**:

Now you've set up a new class, just instantiate and call.

```
#Pass iteration count
bm = SomeBenchMark(1000)
bm.benchmark()
```

If you need additional instance properties just replace the __init__ and make sure to pass an iterations count to super().

**example_benchmarker.py"** has additional init parameters for the length of each iteration's data and the range of values to be randomly generated.

```
#Iteration count, iteration list length and upper limit for random ints.
bm = SomeBenchMark(1000, 100, 100)
bm.benchmark()
```

![Example](https://imgur.com/a/UJDnf9d)

**General notes**:

- If you don't want a method to be assessed or want to extend the general boilerplate functionality, prepend "BM" to function names.
- If you're going to modify the input data in the test inlcude "lazy" in the name. This will force a deep clone of the data.

**Lazy aka, safe inputs**:

Some methods such as "example_benchmarker.py"'s lazySubscripted and lazyEnumerate methods manipulate the input data. Unless it's primatives or immutable properties in a class, this would break the test data. Prevent this by including "lazy" in the method name to force a deep clone. Cloning is not by default prepartion performance. Cloning doesn't affect benchmark times.

**Disclaimer**:

Just wrote this for a laugh. If there's something wrong let me know and I'll sort it.

**Fun extra**:

Simple Print prettifier for hash to table and basic string padding. Nothing fancy but I find it useful.

Cheers,
Ollie.
