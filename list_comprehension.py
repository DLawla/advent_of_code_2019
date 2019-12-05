# lo , hi = 145852 , 616942
# strings = [str(s) for s in xrange(lo, hi + 1)]
# nodecrs = [s for s in strings if s == ''.join(sorted(list(s)))]
# repeats = [str(i) * 2 for i in xrange(10)]
# results = [s for s in nodecrs if any(d in s for d in repeats)]
# print(len(results))

# Part 2:
# #!/usr/bin/python
# lo , hi = 145852 , 616942
# strings = [str(s) for s in xrange(lo, hi + 1)]
# nodecrs = [s for s in strings if s == ''.join(sorted(list(s)))]
# repeats = [(str(i) * 2, str(i) * 3) for i in xrange(10)]
# results = [s for s in nodecrs if any(d in s and not t in s for d, t in repeats)]
# print(len(results))
