import math

class PermutationGenerator():
	"""Iterate through all permutations
	"""
	
	def __init__(self, n):
		self.total = math.factorial(n)
		self.a = range(0, n)
		self.numleft = self.total


	def hasmore(self):
		return self.numleft != 0


	def getNext (self):
			

		if self.numleft == self.total:
			self.numleft -= 1
			return self.a
			
		
		# Find largest index j with a[j] < a[j+1]
		j = len(self.a) - 2
		while self.a[j] > self.a[j+1]:
			j -= 1
					
		# Find index k such that a[k] is smallest integer
		# greater than a[j] to the right of a[j]
		k = len(self.a) - 1
		while self.a[j] > self.a[k]:
			k -= 1
		
		# Interchange a[j] and a[k]
		
		temp = self.a[k]
		self.a[k] = self.a[j]
		self.a[j] = temp
		
		# Put tail end of permutation after jth position in increasing order
		
		r = len(self.a) - 1
		s = j + 1
		
		while r > s:
			temp = self.a[s]
			self.a[s] = self.a[r]
			self.a[r] = temp
			r -= 1
			s += 1
		
		
		self.numleft -= 1

		return self.a;

